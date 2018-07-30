import difflib
import logging
from urllib.parse import urljoin

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, ngettext
from django.views.generic import DetailView
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.decorators.clickjacking import xframe_options_sameorigin
from wiki import editors, forms, models
from wiki.conf import settings
from wiki.core import permissions
from wiki.core.diff import simple_merge
from wiki.core.exceptions import NoRootURL
from wiki.core.paginator import WikiPaginator
from wiki.core.plugins import registry as plugin_registry
from wiki.core.utils import object_to_json_response
from wiki.decorators import get_article
from wiki.views.mixins import ArticleMixin

log = logging.getLogger(__name__)


class ArticleView(ArticleMixin, TemplateView):

    template_name = "wiki/view.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super().dispatch(request, article, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'view'
        return ArticleMixin.get_context_data(self, **kwargs)


class Create(FormView, ArticleMixin):

    form_class = forms.CreateForm
    template_name = "wiki/create.html"

    @method_decorator(get_article(can_write=True, can_create=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super().dispatch(request, article, *args, **kwargs)

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        initial = kwargs.get('initial', {})
        initial['slug'] = self.request.GET.get('slug', None)
        kwargs['initial'] = initial
        form = form_class(self.request, self.urlpath, **kwargs)
        form.fields['slug'].widget = forms.TextInputPrepend(
            prepend='/' + self.urlpath.path,
            attrs={
                # Make patterns force lowercase if we are case insensitive to bless the user with a
                # bit of strictness, anyways
                'pattern': '[a-z0-9_-]+' if not settings.URL_CASE_SENSITIVE else '[a-zA-Z0-9_-]+',
                'title': 'Lowercase letters, numbers, hyphens and underscores' if not settings.URL_CASE_SENSITIVE else 'Letters, numbers, hyphens and underscores',
            }
        )
        return form

    def form_valid(self, form):
        try:
            self.newpath = models.URLPath._create_urlpath_from_request(
                self.request,
                self.article,
                self.urlpath,
                form.cleaned_data['slug'],
                form.cleaned_data['title'],
                form.cleaned_data['content'],
                form.cleaned_data['summary']
            )
            messages.success(
                self.request,
                _("New article '%s' created.") %
                self.newpath.article.current_revision.title)
        # TODO: Handle individual exceptions better and give good feedback.
        except Exception as e:
            log.exception("Exception creating article.")
            if self.request.user.is_superuser:
                messages.error(
                    self.request,
                    _("There was an error creating this article: %s") %
                    str(e))
            else:
                messages.error(self.request, _("There was an error creating this article."))
            return redirect('wiki:get', '')

        return self.get_success_url()

    def get_success_url(self):
        return redirect('wiki:get', self.newpath.path)

    def get_context_data(self, **kwargs):
        c = ArticleMixin.get_context_data(self, **kwargs)
        # Needed since Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in c:
            c['form'] = self.get_form()
        c['parent_urlpath'] = self.urlpath
        c['parent_article'] = self.article
        c['create_form'] = c.pop('form', None)
        c['editor'] = editors.getEditor()
        return c


class Delete(FormView, ArticleMixin):

    form_class = forms.DeleteForm
    template_name = "wiki/delete.html"

    @method_decorator(
        get_article(
            can_write=True,
            not_locked=True,
            can_delete=True))
    def dispatch(self, request, article, *args, **kwargs):
        return self.dispatch1(request, article, *args, **kwargs)

    def dispatch1(self, request, article, *args, **kwargs):
        """Deleted view needs to access this method without a decorator,
        therefore it is separate."""
        urlpath = kwargs.get('urlpath', None)
        # Where to go after deletion...
        self.next = ""
        self.cannot_delete_root = False
        if urlpath and urlpath.parent:
            self.next = reverse(
                'wiki:get',
                kwargs={
                    'path': urlpath.parent.path})
        elif urlpath:
            # We are a urlpath with no parent. This is the root
            self.cannot_delete_root = True
        else:
            # We have no urlpath. Get it if a urlpath exists
            for art_obj in article.articleforobject_set.filter(is_mptt=True):
                if art_obj.content_object.parent:
                    self.next = reverse(
                        'wiki:get', kwargs={
                            'article_id': art_obj.content_object.parent.article.id})
                else:
                    self.cannot_delete_root = True

        return super().dispatch(request, article, *args, **kwargs)

    def get_initial(self):
        return {'revision': self.article.current_revision}

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
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

        # If we are purging, only moderators can delete articles with children
        cannot_delete_children = False
        can_moderate = self.article.can_moderate(self.request.user)
        if purge and self.children_slice and not can_moderate:
            cannot_delete_children = True

        if self.cannot_delete_root or cannot_delete_children:
            messages.error(
                self.request,
                _('This article cannot be deleted because it has children or is a root article.'))
            return redirect('wiki:get', article_id=self.article.id)

        if can_moderate and purge:
            # First, remove children
            if self.urlpath:
                self.urlpath.delete_subtree()
            self.article.delete()
            messages.success(
                self.request,
                _('This article together with all its contents are now completely gone! Thanks!'))
        else:
            revision = models.ArticleRevision()
            revision.inherit_predecessor(self.article)
            revision.set_from_request(self.request)
            revision.deleted = True
            self.article.add_revision(revision)
            messages.success(
                self.request,
                _('The article "%s" is now marked as deleted! Thanks for keeping the site free from unwanted material!') %
                revision.title)
        return self.get_success_url()

    def get_success_url(self):
        return redirect(self.next)

    def get_context_data(self, **kwargs):
        cannot_delete_children = False
        if self.children_slice and not self.article.can_moderate(
                self.request.user):
            cannot_delete_children = True

        # Needed since Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['delete_form'] = kwargs.pop('form', None)
        kwargs['cannot_delete_root'] = self.cannot_delete_root
        kwargs['delete_children'] = self.children_slice[:20]
        kwargs['delete_children_more'] = len(self.children_slice) > 20
        kwargs['cannot_delete_children'] = cannot_delete_children
        return super().get_context_data(**kwargs)


class Edit(ArticleMixin, FormView):

    """Edit an article and process sidebar plugins."""

    form_class = forms.EditForm
    template_name = "wiki/edit.html"

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.sidebar_plugins = plugin_registry.get_sidebar()
        self.sidebar = []
        return super().dispatch(request, article, *args, **kwargs)

    def get_initial(self):
        initial = FormView.get_initial(self)

        for field_name in ['title', 'content']:
            session_key = 'unsaved_article_%s_%d' % (
                field_name, self.article.id)
            if session_key in self.request.session:
                content = self.request.session[session_key]
                initial[field_name] = content
                del self.request.session[session_key]
        return initial

    def get_form(self, form_class=None):
        """
        Checks from querystring data that the edit form is actually being saved,
        otherwise removes the 'data' and 'files' kwargs from form initialisation.
        """
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        if self.request.POST.get(
                'save',
                '') != '1' and self.request.POST.get('preview') != '1':
            kwargs['data'] = None
            kwargs['files'] = None
            kwargs['no_clean'] = True
        return form_class(self.request, self.article.current_revision, **kwargs)

    def get_sidebar_form_classes(self):
        """Returns dictionary of form classes for the sidebar. If no form class is
        specified, puts None in dictionary. Keys in the dictionary are used
        to identify which form is being saved."""
        form_classes = {}
        for cnt, plugin in enumerate(self.sidebar_plugins):
            form_classes[
                'form%d' %
                cnt] = (
                plugin,
                plugin.sidebar.get(
                    'form_class',
                    None))
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
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Generate sidebar forms
        self.sidebar_forms = []
        for form_id, (plugin, Form) in self.get_sidebar_form_classes().items():
            if Form:
                if form_id == self.request.GET.get('f', None):
                    form = Form(
                        self.article,
                        self.request,
                        data=self.request.POST,
                        files=self.request.FILES)
                    if form.is_valid():
                        form.save()
                        usermessage = form.get_usermessage()
                        if usermessage:
                            messages.success(self.request, usermessage)
                        else:
                            messages.success(
                                self.request,
                                _('Your changes were saved.'))

                        title = form.cleaned_data['unsaved_article_title']
                        content = form.cleaned_data['unsaved_article_content']

                        if title != self.article.current_revision.title or content != self.article.current_revision.content:
                            request.session[
                                'unsaved_article_title_%d' %
                                self.article.id] = title
                            request.session[
                                'unsaved_article_content_%d' %
                                self.article.id] = content
                            messages.warning(
                                request,
                                _('Please note that your article text has not yet been saved!'))

                        if self.urlpath:
                            return redirect(
                                'wiki:edit',
                                path=self.urlpath.path)
                        return redirect(
                            'wiki:edit',
                            article_id=self.article.id)

                else:
                    form = Form(self.article, self.request)
                setattr(form, 'form_id', form_id)
            else:
                form = None
            self.sidebar.append((plugin, form))
        return super().post(request, *args, **kwargs)

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
        messages.success(
            self.request,
            _('A new revision of the article was successfully added.'))
        return self.get_success_url()

    def get_success_url(self):
        """Go to the article view page when the article has been saved"""
        if self.urlpath:
            return redirect("wiki:get", path=self.urlpath.path)
        return redirect('wiki:get', article_id=self.article.id)

    def get_context_data(self, **kwargs):
        # Needed for Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['edit_form'] = kwargs['form']
        kwargs['editor'] = editors.getEditor()
        kwargs['selected_tab'] = 'edit'
        kwargs['sidebar'] = self.sidebar
        return super().get_context_data(**kwargs)


class Move(ArticleMixin, FormView):

    form_class = forms.MoveForm
    template_name = "wiki/move.html"

    @method_decorator(login_required)
    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super().dispatch(request, article, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['root_path'] = models.URLPath.root()

        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form):
        if not self.urlpath.parent:
            messages.error(
                self.request,
                _('This article cannot be moved because it is a root article.')
            )
            return redirect('wiki:get', article_id=self.article.id)

        dest_path = get_object_or_404(
            models.URLPath,
            pk=form.cleaned_data['destination']
        )
        tmp_path = dest_path

        while tmp_path.parent:
            if tmp_path == self.urlpath:
                messages.error(
                    self.request,
                    _('This article cannot be moved to a child of itself.')
                )
                return redirect('wiki:move', article_id=self.article.id)
            tmp_path = tmp_path.parent

        # Clear cache to update article lists (Old links)
        for ancestor in self.article.ancestor_objects():
            ancestor.article.clear_cache()

        # Save the old path for later
        old_path = self.urlpath.path

        self.urlpath.parent = dest_path
        self.urlpath.slug = form.cleaned_data['slug']
        self.urlpath.save()

        # Reload url path form database
        self.urlpath = models.URLPath.objects.get(pk=self.urlpath.pk)

        # Use a copy of ourself (to avoid cache) and update article links again
        for ancestor in models.Article.objects.get(pk=self.article.pk).ancestor_objects():
            ancestor.article.clear_cache()

        # Create a redirect page for every moved article
        # /old-slug
        # /old-slug/child
        # /old-slug/child/grand-child
        if form.cleaned_data['redirect']:

            # NB! Includes self!
            descendants = list(self.urlpath.get_descendants(
                include_self=True).order_by("level"))

            root_len = len(descendants[0].path)

            for descendant in descendants:
                # Without this descendant.get_ancestors() and as a result
                # descendant.path is wrong after the first create_article() due
                # to path caching
                descendant.refresh_from_db()
                dst_path = descendant.path
                src_path = urljoin(old_path, dst_path[root_len:])
                src_len = len(src_path)
                pos = src_path.rfind("/", 0, src_len - 1)
                slug = src_path[pos + 1:src_len - 1]
                parent_urlpath = models.URLPath.get_by_path(src_path[0:max(pos, 0)])

                link = "[wiki:/{path}](wiki:/{path})".format(path=dst_path)
                urlpath_new = models.URLPath._create_urlpath_from_request(
                    self.request,
                    self.article,
                    parent_urlpath,
                    slug,
                    _("Moved: {title}").format(title=descendant.article),
                    _("Article moved to {link}").format(link=link),
                    _("Created redirect (auto)"),
                )
                urlpath_new.moved_to = descendant
                urlpath_new.save()

            messages.success(
                self.request,
                ngettext(
                    "Article successfully moved! Created {n} redirect.",
                    "Article successfully moved! Created {n} redirects.",
                    len(descendants)
                ).format(
                    n=len(descendants)
                )
            )

        else:
            messages.success(self.request, _('Article successfully moved!'))
        return redirect("wiki:get", path=self.urlpath.path)


class Deleted(Delete):

    """Tell a user that an article has been deleted. If user has permissions,
    let user restore and possibly purge the deleted article and children."""

    template_name = "wiki/deleted.html"
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
            can_restore = not article.current_revision.locked and article.can_delete(
                request.user)
            can_restore = can_restore or article.can_moderate(request.user)

            if can_restore:
                revision = models.ArticleRevision()
                revision.inherit_predecessor(self.article)
                revision.set_from_request(request)
                revision.deleted = False
                revision.automatic_log = _('Restoring article')
                self.article.add_revision(revision)
                messages.success(
                    request,
                    _('The article "%s" and its children are now restored.') %
                    revision.title)
                if self.urlpath:
                    return redirect('wiki:get', path=self.urlpath.path)
                else:
                    return redirect('wiki:get', article_id=article.id)

        return super().dispatch1(request, article, *args, **kwargs)

    def get_initial(self):
        return {'revision': self.article.current_revision,
                'purge': True}

    def get_context_data(self, **kwargs):
        # Needed since Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['purge_form'] = kwargs.pop('form', None)
        return super(Delete, self).get_context_data(**kwargs)


class Source(ArticleMixin, TemplateView):

    template_name = "wiki/source.html"

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super().dispatch(request, article, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'source'
        return ArticleMixin.get_context_data(self, **kwargs)


class History(ListView, ArticleMixin):

    template_name = "wiki/history.html"
    allow_empty = True
    context_object_name = 'revisions'
    paginator_class = WikiPaginator
    paginate_by = 10

    def get_queryset(self):
        return models.ArticleRevision.objects.filter(
            article=self.article).order_by('-created')

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
        return super().dispatch(request, article, *args, **kwargs)


class Dir(ListView, ArticleMixin):

    template_name = "wiki/dir.html"
    allow_empty = True
    context_object_name = 'directory'
    model = models.URLPath
    paginator_class = WikiPaginator
    paginate_by = 30

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.filter_form = forms.DirFilterForm(request.GET)
        if self.filter_form.is_valid():
            self.query = self.filter_form.cleaned_data['query']
        else:
            self.query = None
        return super().dispatch(request, article, *args, **kwargs)

    def get_queryset(self):
        children = self.urlpath.get_children().can_read(self.request.user)
        if self.query:
            children = children.filter(
                Q(article__current_revision__title__contains=self.query) |
                Q(slug__contains=self.query))
        if not self.article.can_moderate(self.request.user):
            children = children.active()
        children = children.select_related_common().order_by(
            'article__current_revision__title')
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

    template_name = "wiki/search.html"
    paginator_class = WikiPaginator
    paginate_by = 25
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        self.urlpath = None
        # Do not allow anonymous users to search if they cannot read content
        if request.user.is_anonymous and not settings.ANONYMOUS:
            return redirect(settings.LOGIN_URL)
        self.search_form = forms.SearchForm(request.GET)
        if self.search_form.is_valid():
            self.query = self.search_form.cleaned_data['q']
        else:
            self.query = None
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if not self.query:
            return models.Article.objects.none().order_by('-current_revision__created')
        articles = models.Article.objects
        path = self.kwargs.get('path', None)
        if path:
            try:
                self.urlpath = models.URLPath.get_by_path(path)
                article_ids = self.urlpath.get_descendants(
                    include_self=True).values_list('article_id')
                articles = articles.filter(id__in=article_ids)
            except (NoRootURL, models.URLPath.DoesNotExist):
                raise Http404
        articles = articles.filter(
            Q(current_revision__title__icontains=self.query) |
            Q(current_revision__content__icontains=self.query))
        if not permissions.can_moderate(
                models.URLPath.root().article,
                self.request.user):
            articles = articles.active().can_read(self.request.user)
        return articles.order_by('-current_revision__created')

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['search_form'] = self.search_form
        kwargs['search_query'] = self.query
        kwargs['urlpath'] = self.urlpath
        return kwargs


class Plugin(View):

    def dispatch(self, request, path=None, slug=None, **kwargs):
        kwargs['path'] = path
        for plugin in list(plugin_registry.get_plugins().values()):
            if getattr(plugin, 'slug', None) == slug:
                return plugin.article_view(request, **kwargs)
        raise Http404()


class Settings(ArticleMixin, TemplateView):

    permission_form_class = forms.PermissionsForm
    template_name = "wiki/settings.html"

    @method_decorator(login_required)
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super().dispatch(request, article, *args, **kwargs)

    def get_form_classes(self,):
        """
        Return all settings forms that can be filled in
        """
        settings_forms = []
        if permissions.can_change_permissions(self.article, self.request.user):
            settings_forms.append(self.permission_form_class)
        plugin_forms = [F for F in plugin_registry.get_settings_forms()]
        plugin_forms.sort(key=lambda form: form.settings_order)
        settings_forms += plugin_forms
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
                        return redirect(
                            'wiki:settings',
                            path=self.urlpath.path)
                    return redirect(
                        'wiki:settings',
                        article_id=self.article.id)
            else:
                form = Form(self.article, self.request)
            self.forms.append(form)
        return super().get(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.forms = []

        # There is a bug where articles fetched with select_related have bad boolean field https://code.djangoproject.com/ticket/15040
        # We fetch a fresh new article for this reason
        new_article = models.Article.objects.get(id=self.article.id)

        for Form in self.get_form_classes():
            self.forms.append(Form(new_article, self.request))

        return super().get(*args, **kwargs)

    def get_success_url(self):
        if self.urlpath:
            return redirect('wiki:settings', path=self.urlpath.path)
        return redirect('wiki:settings', article_id=self.article.id)

    def get_context_data(self, **kwargs):
        kwargs['selected_tab'] = 'settings'
        kwargs['forms'] = self.forms
        return super().get_context_data(**kwargs)


class ChangeRevisionView(RedirectView):

    permanent = False

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.article = article
        self.urlpath = kwargs.pop('kwargs', False)
        self.change_revision()

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        if self.urlpath:
            return reverse("wiki:history", kwargs={'path': self.urlpath.path})
        else:
            return reverse('wiki:history', kwargs={'article_id': self.article.id})

    def change_revision(self):
        revision = get_object_or_404(
            models.ArticleRevision,
            article=self.article,
            id=self.kwargs['revision_id'])
        self.article.current_revision = revision
        self.article.save()
        messages.success(
            self.request,
            _("The article %(title)s is now set to display revision #%(revision_number)d") % {
                'title': revision.title,
                'revision_number': revision.revision_number,
            })


class Preview(ArticleMixin, TemplateView):

    template_name = "wiki/preview_inline.html"

    @method_decorator(xframe_options_sameorigin)
    @method_decorator(get_article(can_read=True, deleted_contents=True))
    def dispatch(self, request, article, *args, **kwargs):
        revision_id = request.GET.get('r', None)
        self.title = None
        self.content = None
        self.preview = False
        if revision_id:
            try:
                revision_id = int(revision_id)
            except ValueError:
                # ValueError only happens because someone put garbage in the
                # querystring
                raise Http404()
            self.revision = get_object_or_404(
                models.ArticleRevision,
                article=article,
                id=revision_id
            )
        else:
            self.revision = None
        return super().dispatch(request, article, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        edit_form = forms.EditForm(request, self.article.current_revision, request.POST, preview=True)
        if edit_form.is_valid():
            self.title = edit_form.cleaned_data['title']
            self.content = edit_form.cleaned_data['content']
            self.preview = True
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.revision and not self.title:
            self.title = self.revision.title
        if self.revision and not self.content:
            self.content = self.revision.content
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.title
        kwargs['revision'] = self.revision
        kwargs['content'] = self.content
        kwargs['preview'] = self.preview
        return ArticleMixin.get_context_data(self, **kwargs)


class DiffView(DetailView):
    model = models.ArticleRevision
    pk_url_kwarg = 'revision_id'

    def render_to_response(self, context, **response_kwargs):
        revision = self.get_object()
        other_revision = revision.previous_revision

        baseText = other_revision.content if other_revision is not None else ""
        newText = revision.content

        differ = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK)
        diff = differ.compare(
            baseText.splitlines(keepends=True), newText.splitlines(keepends=True)
        )
        other_changes = []

        if not other_revision or other_revision.title != revision.title:
            other_changes.append((_('New title'), revision.title))

        return object_to_json_response(
            {'diff': list(diff), 'other_changes': other_changes}
        )


class MergeView(View):
    preview = False
    template_name = "wiki/preview_inline.html"
    template_error_name = "wiki/error.html"
    urlpath = None

    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, revision_id, *args, **kwargs):
        return super().dispatch(request, article, revision_id, *args, **kwargs)

    def get(self, request, article, revision_id, *args, **kwargs):
        revision = get_object_or_404(
            models.ArticleRevision,
            article=article,
            id=revision_id)

        current_text = article.current_revision.content if article.current_revision else ""
        new_text = revision.content

        content = simple_merge(current_text, new_text)

        # Save new revision
        if not self.preview:
            old_revision = article.current_revision

            if revision.deleted:
                c = {
                    'error_msg': _('You cannot merge with a deleted revision'),
                    'article': article,
                    'urlpath': self.urlpath
                }
                return render(request, self.template_error_name, context=c)

            new_revision = models.ArticleRevision()
            new_revision.inherit_predecessor(article)
            new_revision.deleted = False
            new_revision.locked = False
            new_revision.title = article.current_revision.title
            new_revision.content = content
            new_revision.automatic_log = (
                _('Merge between revision #%(r1)d and revision #%(r2)d') % {
                    'r1': revision.revision_number,
                    'r2': old_revision.revision_number})
            article.add_revision(new_revision, save=True)

            old_revision.simpleplugin_set.all().update(
                article_revision=new_revision)
            revision.simpleplugin_set.all().update(article_revision=new_revision)

            messages.success(
                request,
                _('A new revision was created: Merge between revision #%(r1)d and revision #%(r2)d') % {
                    'r1': revision.revision_number,
                    'r2': old_revision.revision_number})
            if self.urlpath:
                return redirect('wiki:edit', path=self.urlpath.path)
            else:
                return redirect('wiki:edit', article_id=article.id)

        c = {
            'article': article,
            'title': article.current_revision.title,
            'revision': None,
            'merge1': revision,
            'merge2': article.current_revision,
            'merge': True,
            'content': content
        }
        return render(request, self.template_name, c)


class CreateRootView(FormView):
    form_class = forms.CreateRootForm
    template_name = 'wiki/create_root.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return redirect("wiki:root_missing")

        try:
            root = models.URLPath.root()
        except NoRootURL:
            pass
        else:
            if root.article:
                return redirect('wiki:get', path=root.path)

            # TODO: This is too dangerous... let's say there is no root.article and we end up here,
            # then it might cascade to delete a lot of things on an existing
            # installation.... / benjaoming
            root.delete()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        models.URLPath.create_root(
            title=form.cleaned_data["title"],
            content=form.cleaned_data["content"],
            request=self.request
        )
        return redirect("wiki:root")

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['editor'] = editors.getEditor()
        # Needed since Django 1.9 because get_context_data is no longer called
        # with the form instance
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs


class MissingRootView(TemplateView):
    template_name = 'wiki/root_missing.html'
