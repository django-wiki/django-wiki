# -*- coding: utf-8 -*-
import difflib

from django.contrib import messages
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
from wiki.core import plugins_registry
from wiki.core.diff import simple_merge
from wiki.decorators import get_article, json_view
from django.core.urlresolvers import reverse
from django.db import transaction
from wiki.core.exceptions import NoRootURL
from django_notify.decorators import disable_notify

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
        if not self.request.user.is_anonymous:
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
                # TODO: Subscribe user to new article and send notifications that user was subscribed.
            messages.success(self.request, _(u"New article '%s' created.") % self.newpath.article.current_revision.title)
        
            transaction.commit()
        # TODO: Handle individual exceptions better and give good feedback.
        except Exception, e:
            transaction.rollback()
            if self.request.user.has_perm('wiki.moderator'):
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
        kwargs['editor'] = editors.editor
        return super(Create, self).get_context_data(**kwargs)
    

class Delete(FormView, ArticleMixin):
    
    form_class = forms.DeleteForm
    template_name="wiki/delete.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        urlpath = kwargs.get('urlpath', None)
        # Where to go after deletion... 
        self.next = request.GET.get('next', None)
        self.cannot_delete_root = False
        if not self.next:
            if urlpath and urlpath.parent:
                self.next = reverse('wiki:get', kwargs={'path': urlpath.parent.path})
            elif urlpath:
                self.cannot_delete_root = True
            else:
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
        if self.request.user.has_perm('wiki.moderator'):
            form.fields['purge'].widget = forms.forms.CheckboxInput()
        return form
    
    def get_form_kwargs(self):
        kwargs = FormView.get_form_kwargs(self)
        kwargs['article'] = self.article
        kwargs['has_children'] = bool(self.children_slice)
        return kwargs
    
    @disable_notify
    def delete_children(self, purge=False):
        if purge:
            for child in self.article.get_children(articles__article__current_revision__deleted=False):
                child.delete()
        else:
            for child in self.article.get_children(articles__article__current_revision__deleted=False):
                revision = models.ArticleRevision()
                revision.inherit_predecessor(child.article)
                revision.set_from_request(self.request)
                revision.automatic_log = _(u'Deleting children of "%s"') % self.article.current_revision.title
                revision.deleted = True
                child.article.add_revision(revision)
        
    def form_valid(self, form):
        cd = form.cleaned_data
        
        cannot_delete_children = False
        if self.children_slice and not self.request.user.has_perm('wiki.moderator'):
            cannot_delete_children = True

        if self.cannot_delete_root or cannot_delete_children:
            messages.error(self.request, _(u'This article cannot be deleted because it has children or is a root article.'))
            return redirect('wiki:get', article_id=self.article.id)
        
        # First, remove children
        self.delete_children(purge=cd['purge'])
        
        if self.request.user.has_perm('wiki.moderator') and cd['purge']:
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
        if self.children_slice and not self.request.user.has_perm('wiki.moderator'):
            cannot_delete_children = True
        
        kwargs['delete_form'] = kwargs.pop('form', None)
        kwargs['cannot_delete_root'] = self.cannot_delete_root
        kwargs['delete_children'] = self.children_slice[:20]
        kwargs['delete_children_more'] = len(self.children_slice) > 20
        kwargs['cannot_delete_children'] = cannot_delete_children
        return super(Delete, self).get_context_data(**kwargs)


class Edit(FormView, ArticleMixin):
    
    form_class = forms.EditForm
    template_name="wiki/edit.html"
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(Edit, self).dispatch(request, article, *args, **kwargs)
    
    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(self.article.current_revision, **self.get_form_kwargs())
    
    def form_valid(self, form):
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
        if self.urlpath:
            return redirect("wiki:get", path=self.urlpath.path)
        return redirect('wiki:get', article_id=self.article.id)
        
    
    def get_context_data(self, **kwargs):
        kwargs['edit_form'] = kwargs.pop('form', None)
        kwargs['editor'] = editors.editor
        kwargs['selected_tab'] = 'edit'
        return super(Edit, self).get_context_data(**kwargs)


# TODO: ...
class Source(ArticleMixin, TemplateView):
    pass


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


class Plugin(View):
    
    def dispatch(self, request, path=None, slug=None, **kwargs):
        kwargs['path'] = path
        for plugin in plugins_registry._cache.values():
            if getattr(plugin, 'slug', None) == slug:
                return plugin.article_view(request, **kwargs)

class Settings(ArticleMixin, TemplateView):
    
    permission_form_class = forms.PermissionsForm
    template_name="wiki/settings.html"
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(Settings, self).dispatch(request, article, *args, **kwargs)
    
    def get_form_classes(self,):
        """
        Return all settings forms that can be filled in
        """
        settings_forms = [F for F in plugins_registry._settings_forms]
        if (self.request.user.has_perm('wiki.assign') or 
            self.article.owner == self.request.user):
            settings_forms.append(self.permission_form_class)
        settings_forms.sort(key=lambda form: form.settings_order)
        for i in range(len(settings_forms)):
            setattr(settings_forms[i], 'action', 'form%d' % i)
        return settings_forms
    
    def post(self, *args, **kwargs):
        self.forms = []
        for Form in self.get_form_classes():
            if Form.action == self.request.GET.get('f', None):
                form = Form(self.article, self.request.user,self.request.POST)
                if form.is_valid():
                    form.save()
                    usermessage = form.get_usermessage()
                    if usermessage:
                        messages.success(self.request, usermessage)
                    if self.urlpath:
                        return redirect('wiki:settings', path=self.urlpath.path)
                    return redirect('wiki:settings', article_id=self.article.id)
            else:
                form = Form(self.article, self.request.user)
            self.forms.append(form)
        return super(Settings, self).get(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        self.forms = []
        for Form in self.get_form_classes():
            self.forms.append(Form(self.article, self.request.user))
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
@get_article(can_write=True)
def change_revision(request, article, revision_id=None, urlpath=None):
    revision = get_object_or_404(models.ArticleRevision, article=article, id=revision_id)
    article.current_revision = revision
    article.save()
    messages.success(request, _(u'The article %s is now set to display revision #%d') % (revision.title, revision.revision_number))
    if urlpath:
        return redirect("wiki:history", path=urlpath.path)
    else:
        return redirect('wiki:history', article_id=article.id)

# TODO: Throw in a class-based view
@get_article(can_read=True)
def preview(request, article, urlpath=None, template_file="wiki/preview_inline.html"):
    
    content = article.current_revision.content
    title = article.current_revision.title
    
    revision_id = request.GET.get('r', None)
    revision = None
    
    if request.method == 'POST':
        edit_form = forms.EditForm(article.current_revision, request.POST, preview=True)
        if edit_form.is_valid():
            title = edit_form.cleaned_data['title']
            content = edit_form.cleaned_data['content']
    
    elif revision_id:
        revision = get_object_or_404(models.ArticleRevision, article=article, id=revision_id)
        title = revision.title
        content = revision.content
    
    c = RequestContext(request, {'urlpath': urlpath,
                                 'article': article,
                                 'title': title,
                                 'revision': revision,
                                 'content': content})
    return render_to_response(template_file, c)

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
    return render_to_response(template_file, c)

# TODO: Should be a class-based view
def root_create(request):
    try:
        root = models.URLPath.root()
        if not root.article:
            root.delete()
            raise NoRootURL
        return redirect('wiki:get', path=root.path)
    except NoRootURL:
        pass
    if not request.user.has_perm('wiki.add_article'):
        return redirect(reverse("wiki:login") + "?next=" + reverse("wiki:root_create"))
    if request.method == 'POST':
        create_form = forms.CreateRootForm(request.POST)
        if create_form.is_valid():
            models.URLPath.create_root(title=create_form.cleaned_data["title"],
                                       content=create_form.cleaned_data["content"])
            return redirect("wiki:root")
    else:
        create_form = forms.CreateRootForm()
    
    c = RequestContext(request, {'create_form': create_form,
                                 'editor': editors.editor,})
    return render_to_response("wiki/article/create_root.html", c)

