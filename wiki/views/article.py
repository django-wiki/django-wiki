# -*- coding: utf-8 -*-
import difflib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from wiki.views.mixins import ArticleMixin
from wiki import editors, forms, models
from wiki.conf import settings
from wiki.core.plugins import registry as plugin_registry
from wiki.core.diff import simple_merge
from wiki.decorators import get_article, json_view
from django.core.urlresolvers import reverse
from django.db import transaction
from wiki.core.exceptions import NoRootURL
from wiki.core import permissions

class ArticleView(ArticleMixin, TemplateView):

    template_name="wiki/article.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(ArticleView, self).dispatch(request, article, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'view'
        return ArticleMixin.get_context_data(self, **kwargs)

class Create(FormView, ArticleMixin):
    
    form_class = forms.CreateForm
    template_name="wiki/create.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(Create, self).dispatch(request, article, *args, **kwargs)
    
    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        initial = kwargs.get('initial', {})
        initial['slug'] = self.request.GET.get('slug', None)
        kwargs['initial'] = initial
        form = form_class(self.urlpath, **kwargs)
        form.fields['slug'].widget = forms.TextInputPrepend(prepend='/'+self.urlpath.path)        
        return form
    
    @transaction.commit_manually
    def form_valid(self, form):
        user=None
        ip_address = None
        if not self.request.user.is_anonymous():
            user = self.request.user
            if settings.LOG_IPS_USERS:
                ip_address = self.request.META.get('REMOTE_ADDR', None)
        elif settings.LOG_IPS_ANONYMOUS:
            ip_address = self.request.META.get('REMOTE_ADDR', None)
        try:
            self.newpath = models.URLPath.create_article(
                self.urlpath,
                form.cleaned_data['slug'],
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                user_message=form.cleaned_data['summary'],
                user=user,
                ip_address=ip_address,
                article_kwargs={'owner': user,
                                'group': self.article.group,
                                'group_read': self.article.group_read,
                                'group_write': self.article.group_write,
                                'other_read': self.article.other_read,
                                'other_write': self.article.other_write,
                                })
            messages.success(self.request, _(u"New article '%s' created.") % self.newpath.article.current_revision.title)
        
            transaction.commit()
        # TODO: Handle individual exceptions better and give good feedback.
        except Exception, e:
            transaction.rollback()
            if self.request.user.is_superuser:
                messages.error(self.request, _(u"There was an error creating this article: %s") % str(e))
            else:
                messages.error(self.request, _(u"There was an error creating this article."))
            transaction.commit()
            return redirect('wiki:get', '')
            
        url = self.get_success_url()
        transaction.commit()
        return url
    
    def get_success_url(self):
        return redirect('wiki:get', self.newpath.path)
    
    def get_context_data(self, **kwargs):
        kwargs['parent_urlpath'] = self.urlpath
        kwargs['parent_article'] = self.article
        kwargs['create_form'] = kwargs.pop('form', None)
        kwargs['editor'] = editors.getEditor()
        return super(Create, self).get_context_data(**kwargs)
    

class Delete(FormView, ArticleMixin):
    
    form_class = forms.DeleteForm
    template_name="wiki/delete.html"
    
    @method_decorator(get_article(can_write=True, not_locked=True, can_delete=True))
    def dispatch(self, request, article, *args, **kwargs):
        return self.dispatch1(request, article, *args, **kwargs)
        
    def dispatch1(self, request, article, *args, **kwargs):
        """Deleted view needs to access this method without a decorator,
        therefore it is separate."""
        urlpath = kwargs.get('urlpath', None)
        # Where to go after deletion... 
        self.next = request.GET.get('next', None)
        self.cannot_delete_root = False
        if not self.next:
            if urlpath and urlpath.parent:
                self.next = reverse('wiki:get', kwargs={'path': urlpath.parent.path})
            elif urlpath:
                # We are a urlpath with no parent. This is the root
                self.cannot_delete_root = True
            else:
                # We have no urlpath. Get it if a urlpath exists
                for art_obj in article.articleforobject_set.filter(is_mptt=True):
                    if art_obj.content_object.parent:
                        self.next = reverse('wiki:get', kwargs={'article_id': art_obj.content_object.parent.article.id})
                    else:
                        self.cannot_delete_root = True
        
        return super(Delete, self).dispatch(request, article, *args, **kwargs)
    
    def get_initial(self):
        return {'revision': self.article.current_revision}
    
    def get_form(self, form_class):
        form = super(Delete, self).get_form(form_class)
        if self.article.can_moderate(self.request.user):
            form.fields['purge'].widget = forms.forms.CheckboxInput()
        return form
    
    def get_form_kwargs(self):
        kwargs = FormView.get_form_kwargs(self)
        kwargs['article'] = self.article
        kwargs['has_children'] = bool(self.children_slice)
        return kwargs
        
    def form_valid(self, form):
        cd = form.cleaned_data
        
        purge = cd['purge']
        
        #If we are purging, only moderators can delete articles with children
        cannot_delete_children = False
        can_moderate = self.article.can_moderate(self.request.user)
        if purge and self.children_slice and not can_moderate:
            cannot_delete_children = True

        if self.cannot_delete_root or cannot_delete_children:
            messages.error(self.request, _(u'This article cannot be deleted because it has children or is a root article.'))
            return redirect('wiki:get', article_id=self.article.id)
        

        if can_moderate and purge:
            # First, remove children
            if self.urlpath:
                self.urlpath.delete_subtree()
            else:
                self.article.delete()
            
            messages.success(self.request, _(u'This article together with all its contents are now completely gone! Thanks!'))
        else:
            revision = models.ArticleRevision()
            revision.inherit_predecessor(self.article)
            revision.set_from_request(self.request)
            revision.deleted = True
            self.article.add_revision(revision)
            messages.success(self.request, _(u'The article "%s" is now marked as deleted! Thanks for keeping the site free from unwanted material!') % revision.title)
        return self.get_success_url()
        
    def get_success_url(self):
        return redirect(self.next)
    
    def get_context_data(self, **kwargs):
        cannot_delete_children = False
        if self.children_slice and not self.article.can_moderate(self.request.user):
            cannot_delete_children = True
        
        kwargs['delete_form'] = kwargs.pop('form', None)
        kwargs['cannot_delete_root'] = self.cannot_delete_root
        kwargs['delete_children'] = self.children_slice[:20]
        kwargs['delete_children_more'] = len(self.children_slice) > 20
        kwargs['cannot_delete_children'] = cannot_delete_children
        return super(Delete, self).get_context_data(**kwargs)


class Edit(FormView, ArticleMixin):
    """Edit an article and process sidebar plugins."""
    
    form_class = forms.EditForm
    template_name="wiki/edit.html"
    
    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.sidebar_plugins = plugin_registry.get_sidebar()
        self.sidebar = []
        return super(Edit, self).dispatch(request, article, *args, **kwargs)
    
    def get_form(self, form_class):
        """
        Checks from querystring data that the edit form is actually being saved,
        otherwise removes the 'data' and 'files' kwargs from form initialisation.
        """
        kwargs = self.get_form_kwargs()
        if self.request.POST.get('save', '') != '1' and self.request.POST.get('preview') != '1':
            kwargs['data'] = None
            kwargs['files'] = None
            kwargs['no_clean'] = True
        return form_class(self.article.current_revision, **kwargs)
    
    def get_sidebar_form_classes(self):
        """Returns dictionary of form classes for the sidebar. If no form class is
        specified, puts None in dictionary. Keys in the dictionary are used
        to identify which form is being saved."""
        form_classes = {}
        for cnt, plugin in enumerate(self.sidebar_plugins):
            form_classes['form%d' % cnt] = (plugin, plugin.sidebar.get('form_class', None))
        return form_classes
    
    def get(self, request, *args, **kwargs):
        # Generate sidebar forms
        self.sidebar_forms = []
        for form_id, (plugin, Form) in self.get_sidebar_form_classes().items():
            if Form:
                form = Form(self.article, self.request.user)
                setattr(form, 'form_id', form_id)
            else:
                form = None
            self.sidebar.append((plugin, form))
        return super(Edit, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Generate sidebar forms
        self.sidebar_forms = []
        for form_id, (plugin, Form) in self.get_sidebar_form_classes().items():
            if Form:
                if form_id == self.request.GET.get('f', None):
                    form = Form(self.article, self.request, data=self.request.POST, files=self.request.FILES)
                    if form.is_valid():
                        form.save()
                        usermessage = form.get_usermessage()
                        if usermessage:
                            messages.success(self.request, usermessage)
                        else:
                            messages.success(self.request, _(u'Your changes were saved.'))
                        if self.urlpath:
                            return redirect('wiki:edit', path=self.urlpath.path)
                        return redirect('wiki:edit', article_id=self.article.id)
                else:
                    form = Form(self.article, self.request)
                setattr(form, 'form_id', form_id)
            else:
                form = None
            self.sidebar.append((plugin, form))
        return super(Edit, self).post(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Create a new article revision when the edit form is valid 
        (does not concern any sidebar forms!)."""
        revision = models.ArticleRevision()
        revision.inherit_predecessor(self.article)
        revision.title = form.cleaned_data['title']
        revision.content = form.cleaned_data['content']
        revision.user_message = form.cleaned_data['summary']
        revision.deleted = False
        revision.set_from_request(self.request)
        self.article.add_revision(revision)
        messages.success(self.request, _(u'A new revision of the article was succesfully added.'))
        return self.get_success_url()
    
    def get_success_url(self):
        """Go to the article view page when the article has been saved"""
        if self.urlpath:
            return redirect("wiki:get", path=self.urlpath.path)
        return redirect('wiki:get', article_id=self.article.id)
        
    def get_context_data(self, **kwargs):
        kwargs['edit_form'] = kwargs.pop('form', None)
        kwargs['editor'] = editors.getEditor()
        kwargs['selected_tab'] = 'edit'
        kwargs['sidebar'] = self.sidebar
        return super(Edit, self).get_context_data(**kwargs)


class Deleted(Delete):
    """Tell a user that an article has been deleted. If user has permissions,
    let user restore and possibly purge the deleted article and children."""
    
    template_name="wiki/deleted.html"
    form_class = forms.DeleteForm
    
    @method_decorator(get_article(can_read=True, deleted_contents=True))
    def dispatch(self, request, article, *args, **kwargs):
        
        self.urlpath = kwargs.get('urlpath', None)
        self.article = article
        
        if self.urlpath:
            deleted_ancestor = self.urlpath.first_deleted_ancestor()
            if deleted_ancestor is None:
                # No one is deleted!
                return redirect('wiki:get', path=self.urlpath.path)
            elif deleted_ancestor != self.urlpath:
                # An ancestor was deleted, so redirect to that deleted page
                return redirect('wiki:deleted', path=deleted_ancestor.path)
                
        else:
            if not article.current_revision.deleted:
                return redirect('wiki:get', article_id=article.id)
        
        # Restore
        if request.GET.get('restore', False):
            can_restore = not article.current_revision.locked and article.can_delete(request.user)
            can_restore = can_restore or article.can_moderate(request.user)
            
            if can_restore:
                revision = models.ArticleRevision()
                revision.inherit_predecessor(self.article)
                revision.set_from_request(request)
                revision.deleted = False
                revision.automatic_log = _('Restoring article')
                self.article.add_revision(revision)
                messages.success(request, _(u'The article "%s" and its children are now restored.') % revision.title)
                if self.urlpath:
                    return redirect('wiki:get', path=self.urlpath.path)
                else:
                    return redirect('wiki:get', article_id=article.id)
        
        return super(Deleted, self).dispatch1(request, article, *args, **kwargs)
    
    def get_initial(self):
        return {'revision': self.article.current_revision,
                'purge': True}

    def get_form(self, form_class):
        form = super(Delete, self).get_form(form_class)
        return form

    def get_context_data(self, **kwargs):
        kwargs['purge_form'] = kwargs.pop('form', None)
        return super(Delete, self).get_context_data(**kwargs)
    
class Source(ArticleMixin, TemplateView):

    template_name="wiki/source.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(Source, self).dispatch(request, article, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'source'
        return ArticleMixin.get_context_data(self, **kwargs)


class History(ListView, ArticleMixin):
    
    template_name="wiki/history.html"
    allow_empty = True
    context_object_name = 'revisions'
    paginate_by = 10
    
    def get_queryset(self):
        return models.ArticleRevision.objects.filter(article=self.article).order_by('-created')
    
    def get_context_data(self, **kwargs):
        # Is this a bit of a hack? Use better inheritance?
        kwargs_article = ArticleMixin.get_context_data(self, **kwargs)
        kwargs_listview = ListView.get_context_data(self, **kwargs)
        kwargs.update(kwargs_article)
        kwargs.update(kwargs_listview)
        kwargs['selected_tab'] = 'history'
        return kwargs
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(History, self).dispatch(request, article, *args, **kwargs)


class Dir(ListView, ArticleMixin):
    
    template_name="wiki/dir.html"
    allow_empty = True
    context_object_name = 'directory'
    model = models.URLPath
    paginate_by = 30
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.filter_form = forms.DirFilterForm(request.GET)
        if self.filter_form.is_valid():
            self.query = self.filter_form.cleaned_data['query']
        else:
            self.query = None
        return super(Dir, self).dispatch(request, article, *args, **kwargs)

    def get_queryset(self):
        children = self.urlpath.get_children().can_read(self.request.user)
        if self.query:
            children = children.filter(Q(article__current_revision__title__contains=self.query) |
                                       Q(slug__contains=self.query))
        if not self.article.can_moderate(self.request.user):
            children = children.active()
        children = children.select_related_common().order_by('article__current_revision__title')
        return children
    
    def get_context_data(self, **kwargs):
        kwargs_article = ArticleMixin.get_context_data(self, **kwargs)
        kwargs_listview = ListView.get_context_data(self, **kwargs)
        kwargs.update(kwargs_article)
        kwargs.update(kwargs_listview)
        kwargs['filter_query'] = self.query
        kwargs['filter_form'] = self.filter_form
        
        # Update each child's ancestor cache so the lookups don't have
        # to be repeated.
        updated_children = kwargs[self.context_object_name]
        for child in updated_children:
            child.set_cached_ancestors_from_parent(self.urlpath)
        kwargs[self.context_object_name] = updated_children

        return kwargs


class SearchView(ListView):
    
    template_name="wiki/search.html"
    paginate_by = 25
    context_object_name = "articles"
    
    def dispatch(self, request, *args, **kwargs):
        # Do not allow anonymous users to search if they cannot read content
        if request.user.is_anonymous and not settings.ANONYMOUS:
            return(settings.LOGIN_URL)
        self.search_form = forms.SearchForm(request.GET)
        if self.search_form.is_valid():
            self.query = self.search_form.cleaned_data['query']
        else:
            self.query = None
        return super(SearchView, self).dispatch(request, *args, **kwargs)
        
    def get_queryset(self):
        if not self.query:
            return models.Article.objects.get_empty_query_set()
        articles = models.Article.objects.filter(Q(current_revision__title__icontains=self.query) |
                                                 Q(current_revision__content__icontains=self.query))
        if not permissions.can_moderate(models.URLPath.root().article, self.request.user):
            articles = articles.active().can_read(self.request.user)
        return articles
    
    def get_context_data(self, **kwargs):
        kwargs = ListView.get_context_data(self, **kwargs)
        kwargs['search_form'] = self.search_form
        kwargs['search_query'] = self.query
        return kwargs
    
class Plugin(View):
    
    def dispatch(self, request, path=None, slug=None, **kwargs):
        kwargs['path'] = path
        for plugin in plugin_registry.get_plugins().values():
            if getattr(plugin, 'slug', None) == slug:
                return plugin.article_view(request, **kwargs)


class Settings(ArticleMixin, TemplateView):
    
    permission_form_class = forms.PermissionsForm
    template_name="wiki/settings.html"
    
    @method_decorator(login_required)
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(Settings, self).dispatch(request, article, *args, **kwargs)
    
    def get_form_classes(self,):
        """
        Return all settings forms that can be filled in
        """
        settings_forms = [F for F in plugin_registry.get_settings_forms()]
        if permissions.can_change_permissions(self.article, self.request.user):
            settings_forms.append(self.permission_form_class)
        settings_forms.sort(key=lambda form: form.settings_order)
        for i in range(len(settings_forms)):
            # TODO: Do not set an attribute on a form class - this
            # could be mixed up with a different instance
            # Use strategy from Edit view...
            setattr(settings_forms[i], 'action', 'form%d' % i)
        
        return settings_forms
    
    def post(self, *args, **kwargs):
        self.forms = []
        for Form in self.get_form_classes():
            if Form.action == self.request.GET.get('f', None):
                form = Form(self.article, self.request, self.request.POST)
                if form.is_valid():
                    form.save()
                    usermessage = form.get_usermessage()
                    if usermessage:
                        messages.success(self.request, usermessage)
                    if self.urlpath:
                        return redirect('wiki:settings', path=self.urlpath.path)
                    return redirect('wiki:settings', article_id=self.article.id)
            else:
                form = Form(self.article, self.request)
            self.forms.append(form)
        return super(Settings, self).get(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        self.forms = []
        
        # There is a bug where articles fetched with select_related have bad boolean field https://code.djangoproject.com/ticket/15040
        # We fetch a fresh new article for this reason
        new_article = models.Article.objects.get(id=self.article.id)
        
        for Form in self.get_form_classes():
            self.forms.append(Form(new_article, self.request))
        
        return super(Settings, self).get(*args, **kwargs)

    def get_success_url(self):
        if self.urlpath:
            return redirect('wiki:settings', path=self.urlpath.path)
        return redirect('wiki:settings', article_id=self.article.id)
    
    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'settings'
        kwargs['forms'] = self.forms
        return super(Settings, self).get_context_data(**kwargs)


# TODO: Throw in a class-based view
@get_article(can_write=True, not_locked=True)
def change_revision(request, article, revision_id=None, urlpath=None):
    revision = get_object_or_404(models.ArticleRevision, article=article, id=revision_id)
    article.current_revision = revision
    article.save()
    messages.success(request, _(u"The article %(title)s is now set to display revision #%(revision_number)d") % {'title':revision.title, 'revision_number': revision.revision_number,})

    if urlpath:
        return redirect("wiki:history", path=urlpath.path)
    else:
        return redirect('wiki:history', article_id=article.id)

class Preview(ArticleMixin, TemplateView):
    
    template_name="wiki/preview_inline.html"
    
    @method_decorator(get_article(can_read=True, deleted_contents=True))
    def dispatch(self, request, article, *args, **kwargs):
        revision_id = request.GET.get('r', None)
        self.title = None
        self.content = None
        self.preview = False
        if revision_id:
            self.revision = get_object_or_404(models.ArticleRevision, article=article, id=revision_id)
        else:
            self.revision = None
        return super(Preview, self).dispatch(request, article, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        edit_form = forms.EditForm(self.article.current_revision, request.POST, preview=True)
        if edit_form.is_valid():
            self.title = edit_form.cleaned_data['title']
            self.content = edit_form.cleaned_data['content']
            self.preview = True
        return super(Preview, self).get(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        if self.revision and not self.title:
            self.title = self.revision.title
        if self.revision and not self.content:
            self.content = self.revision.content
        return super(Preview, self).get( request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs['title'] = self.title
        kwargs['revision'] = self.revision
        kwargs['content'] = self.content
        kwargs['preview'] = self.preview
        return ArticleMixin.get_context_data(self, **kwargs)
    

@json_view
def diff(request, revision_id, other_revision_id=None):
    
    revision = get_object_or_404(models.ArticleRevision, id=revision_id)
    
    if not other_revision_id:
        other_revision = revision.previous_revision
    
    baseText = other_revision.content if other_revision else ""
    newText = revision.content
    
    differ = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK)
    diff = differ.compare(baseText.splitlines(1), newText.splitlines(1))
    
    other_changes = []
    
    if not other_revision or other_revision.title != revision.title:
        other_changes.append((_(u'New title'), revision.title))
    
    return dict(diff=list(diff), other_changes=other_changes)

# TODO: Throw in a class-based view
@get_article(can_write=True)
def merge(request, article, revision_id, urlpath=None, template_file="wiki/preview_inline.html", preview=False):
    
    revision = get_object_or_404(models.ArticleRevision, article=article, id=revision_id)
    
    current_text = article.current_revision.content if article.current_revision else ""
    new_text = revision.content
    
    content = simple_merge(current_text, new_text)
    
    # Save new revision
    if not preview:
        old_revision = article.current_revision
        new_revision = models.ArticleRevision()
        new_revision.inherit_predecessor(article)
        new_revision.deleted = False
        new_revision.locked = False
        new_revision.title=article.current_revision.title
        new_revision.content=content
        new_revision.automatic_log = (_(u'Merge between Revision #%(r1)d and Revision #%(r2)d') % 
                                      {'r1': revision.revision_number, 
                                       'r2': old_revision.revision_number})
        article.add_revision(new_revision, save=True)
        messages.success(request, _(u'A new revision was created: Merge between Revision #%(r1)d and Revision #%(r2)d') % 
                         {'r1': revision.revision_number,
                          'r2': old_revision.revision_number})
        if urlpath:
            return redirect('wiki:edit', path=urlpath.path)
        else:
            return redirect('wiki:edit', article_id=article.id)
        
    
    c = RequestContext(request, {'article': article,
                                 'title': article.current_revision.title,
                                 'revision': None,
                                 'merge1': revision,
                                 'merge2': article.current_revision,
                                 'merge': True,
                                 'content': content})
    return render_to_response(template_file, context_instance=c)

# TODO: Should be a class-based view
def root_create(request):
    try:
        root = models.URLPath.root()
        if not root.article:
            # TODO: This is too dangerous... let's say there is no root.article and we end up here,
            # then it might cascade to delete a lot of things on an existing installation.... / benjaoming
            root.delete()
            raise NoRootURL
        return redirect('wiki:get', path=root.path)
    except NoRootURL:
        pass
    if not request.user.is_superuser:
        return redirect(settings.LOGIN_URL + "?next=" + reverse("wiki:root_create"))
    if request.method == 'POST':
        create_form = forms.CreateRootForm(request.POST)
        if create_form.is_valid():
            models.URLPath.create_root(title=create_form.cleaned_data["title"],
                                       content=create_form.cleaned_data["content"])
            return redirect("wiki:root")
    else:
        create_form = forms.CreateRootForm()
    
    c = RequestContext(request, {'create_form': create_form,
                                 'editor': editors.getEditor(),})
    return render_to_response("wiki/article/create_root.html", context_instance=c)

