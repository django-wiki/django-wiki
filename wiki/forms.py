# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
import string
from datetime import timedelta
from itertools import chain

from django import forms
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import Resolver404, resolve
from django.forms.widgets import HiddenInput
from django.utils import timezone
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from six.moves import range
from wiki import models
from wiki.conf import settings
from wiki.core import permissions
from wiki.core.compat import get_user_model
from wiki.core.diff import simple_merge
from wiki.core.plugins.base import PluginSettingsFormMixin
from wiki.editors import getEditor

try:
    from django.utils.encoding import force_unicode
except ImportError:
    def force_unicode(x):
        return(x)


User = get_user_model()
Group = apps.get_model(settings.GROUP_MODEL)

# Due to deprecation of django.forms.util in Django 1.9
try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt


class SpamProtectionMixin():

    """Check a form for spam. Only works if properties 'request' and 'revision_model' are set."""

    revision_model = models.ArticleRevision

    # TODO: This method is too complex (C901)
    def check_spam(self):  # noqa
        """Check that user or IP address does not perform content edits that
        are not allowed.

        current_revision can be any object inheriting from models.BaseRevisionMixin
        """
        request = self.request
        user = None
        ip_address = None
        if request.user.is_authenticated():
            user = request.user
        else:
            ip_address = request.META.get('REMOTE_ADDR', None)

        if not (user or ip_address):
            raise forms.ValidationError(
                ugettext(
                    'Spam protection failed to find both a logged in user and an IP address.'))

        def check_interval(from_time, max_count, interval_name):
            from_time = timezone.now(
            ) - timedelta(minutes=settings.REVISIONS_MINUTES_LOOKBACK)
            revisions = self.revision_model.objects.filter(
                created__gte=from_time,
            )
            if user:
                revisions = revisions.filter(user=user)
            if ip_address:
                revisions = revisions.filter(ip_address=ip_address)
            revisions = revisions.count()
            if revisions >= max_count:
                raise forms.ValidationError(
                    ugettext('Spam protection: You are only allowed to create or edit %(revisions)d article(s) per %(interval_name)s.') % {
                        'revisions': max_count,
                        'interval_name': interval_name,
                    })

        if not settings.LOG_IPS_ANONYMOUS:
            return
        if request.user.has_perm('wiki.moderator'):
            return

        from_time = timezone.now() - timedelta(minutes=settings.REVISIONS_MINUTES_LOOKBACK)
        if request.user.is_authenticated():
            per_minute = settings.REVISIONS_PER_MINUTES
        else:
            per_minute = settings.REVISIONS_PER_MINUTES_ANONYMOUS
        check_interval(
            from_time,
            per_minute,
            _('minute') if settings.REVISIONS_MINUTES_LOOKBACK == 1 else (
                _('%d minutes') %
                settings.REVISIONS_MINUTES_LOOKBACK),
        )

        from_time = timezone.now() - timedelta(minutes=60)
        if request.user.is_authenticated():
            per_hour = settings.REVISIONS_PER_MINUTES
        else:
            per_hour = settings.REVISIONS_PER_MINUTES_ANONYMOUS
        check_interval(from_time, per_hour, _('hour'))


class CreateRootForm(forms.Form):

    title = forms.CharField(
        label=_('Title'),
        help_text=_(
            'Initial title of the article. May be overridden with revision titles.'))
    content = forms.CharField(
        label=_('Type in some contents'),
        help_text=_(
            'This is just the initial contents of your article. After creating it, you can use more complex features like adding plugins, meta data, related articles etc...'),
        required=False, widget=getEditor().get_widget())  # @UndefinedVariable


class EditForm(forms.Form, SpamProtectionMixin):

    title = forms.CharField(label=_('Title'),)
    content = forms.CharField(
        label=_('Contents'),
        required=False,
        widget=getEditor().get_widget())  # @UndefinedVariable

    summary = forms.CharField(
        label=_('Summary'),
        help_text=_(
            'Give a short reason for your edit, which will be stated in the revision log.'),
        required=False)

    current_revision = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput())

    def __init__(self, request, current_revision, *args, **kwargs):

        self.request = request
        self.no_clean = kwargs.pop('no_clean', False)
        self.preview = kwargs.pop('preview', False)
        self.initial_revision = current_revision
        self.presumed_revision = None
        if current_revision:
            initial = {'content': current_revision.content,
                       'title': current_revision.title,
                       'current_revision': current_revision.id}
            initial.update(kwargs.get('initial', {}))

            # Manipulate any data put in args[0] such that the current_revision
            # is reset to match the actual current revision.
            data = None
            if len(args) > 0:
                data = args[0]
                args = args[1:]
            if data is None:
                data = kwargs.get('data', None)
            if data:
                self.presumed_revision = data.get('current_revision', None)
                if not str(
                        self.presumed_revision) == str(
                        self.initial_revision.id):
                    newdata = {}
                    for k, v in list(data.items()):
                        newdata[k] = v
                    newdata['current_revision'] = self.initial_revision.id
                    newdata['content'] = simple_merge(
                        self.initial_revision.content,
                        data.get(
                            'content',
                            ""))
                    newdata['title'] = current_revision.title
                    kwargs['data'] = newdata
                else:
                    # Always pass as kwarg
                    kwargs['data'] = data

            kwargs['initial'] = initial

        super(EditForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title', None)
        title = (title or "").strip()
        if not title:
            raise forms.ValidationError(ugettext('Article is missing title or has an invalid title'))
        return title

    def clean(self):
        """Validates form data by checking for the following
        No new revisions have been created since user attempted to edit
        Revision title or content has changed
        """
        cd = self.cleaned_data
        if self.no_clean or self.preview:
            return cd
        if not str(self.initial_revision.id) == str(self.presumed_revision):
            raise forms.ValidationError(
                ugettext(
                    'While you were editing, someone else changed the revision. Your contents have been automatically merged with the new contents. Please review the text below.'))
        if ('title' in cd) and cd['title'] == self.initial_revision.title and cd[
                'content'] == self.initial_revision.content:
            raise forms.ValidationError(
                ugettext('No changes made. Nothing to save.'))
        self.check_spam()
        return cd


class SelectWidgetBootstrap(forms.Select):

    """
    http://twitter.github.com/bootstrap/components.html#buttonDropdowns
    Needs bootstrap and jquery
    """

    def __init__(self, attrs={}, choices=(), disabled=False):
        attrs['class'] = 'btn-group pull-left btn-group-form'
        self.disabled = disabled
        self.noscript_widget = forms.Select(attrs={}, choices=choices)
        super(SelectWidgetBootstrap, self).__init__(attrs, choices)

    def __setattr__(self, k, value):
        super(SelectWidgetBootstrap, self).__setattr__(k, value)
        if k != 'attrs' and k != 'disabled':
            self.noscript_widget.__setattr__(k, value)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [
            """<div%(attrs)s>"""
            """    <button class="btn btn-group-label%(disabled)s" type="button">%(label)s</button>"""
            """    <button class="btn btn-default dropdown-toggle%(disabled)s" type="button" data-toggle="dropdown">"""
            """        <span class="caret"></span>"""
            """    </button>"""
            """    <ul class="dropdown-menu">"""
            """        %(options)s"""
            """    </ul>"""
            """    <input type="hidden" name="%(name)s" value="" class="btn-group-value" />"""
            """</div>"""
            """<noscript>%(noscript)s</noscript>""" %
            {'attrs': flatatt(final_attrs),
             'options': self.render_options(choices, [value]),
             'label': _('Select an option'),
             'name': name, 'disabled': ' disabled' if self.disabled else '',
             'noscript': self.noscript_widget.render(
                 name, value, {},
                 choices)}]
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (
            option_value in selected_choices) and ' selected="selected"' or ''
        return '<li><a href="javascript:void(0)" data-value="%s"%s>%s</a></li>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(
                    '<li class="divider" label="%s"></li>' %
                    escape(
                        force_unicode(option_value)))
                for option in option_label:
                    output.append(
                        self.render_option(
                            selected_choices,
                            *option))
            else:
                output.append(
                    self.render_option(
                        selected_choices,
                        option_value,
                        option_label))
        return '\n'.join(output)

    class Media(forms.Media):

        js = ("wiki/js/forms.js",)


class TextInputPrepend(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.prepend = kwargs.pop('prepend', "")
        super(TextInputPrepend, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        html = super(TextInputPrepend, self).render(*args, **kwargs)
        return mark_safe(
            '<div class="input-group"><span class="input-group-addon">%s</span>%s</div>' %
            (self.prepend, html))


class CreateForm(forms.Form, SpamProtectionMixin):

    def __init__(self, request, urlpath_parent, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.request = request
        self.urlpath_parent = urlpath_parent

    title = forms.CharField(label=_('Title'),)
    slug = forms.SlugField(
        label=_('Slug'),
        help_text=_(
            "This will be the address where your article can be found. Use only alphanumeric characters and - or _. Note that you cannot change the slug after creating the article."),
        max_length=models.URLPath.SLUG_MAX_LENGTH)
    content = forms.CharField(
        label=_('Contents'),
        required=False,
        widget=getEditor().get_widget())  # @UndefinedVariable

    summary = forms.CharField(
        label=_('Summary'),
        help_text=_("Write a brief message for the article's history log."),
        required=False)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug.startswith("_"):
            raise forms.ValidationError(
                ugettext('A slug may not begin with an underscore.'))
        if slug == 'admin':
            raise forms.ValidationError(
                ugettext("'admin' is not a permitted slug name."))

        if settings.URL_CASE_SENSITIVE:
            already_existing_slug = models.URLPath.objects.filter(
                slug=slug,
                parent=self.urlpath_parent)
        else:
            slug = slug.lower()
            already_existing_slug = models.URLPath.objects.filter(
                slug__iexact=slug,
                parent=self.urlpath_parent)
        if already_existing_slug:
            already_urlpath = already_existing_slug[0]
            if already_urlpath.article and already_urlpath.article.current_revision.deleted:
                raise forms.ValidationError(
                    ugettext('A deleted article with slug "%s" already exists.') %
                    already_urlpath.slug)
            else:
                raise forms.ValidationError(
                    ugettext('A slug named "%s" already exists.') %
                    already_urlpath.slug)

        if settings.CHECK_SLUG_URL_AVAILABLE:
            try:
                # Fail validation if URL resolves to non-wiki app
                match = resolve(self.urlpath_parent.path + '/' + slug + '/')
                if match.app_name != 'wiki':
                    raise forms.ValidationError(
                        ugettext('This slug conflicts with an existing URL.'))
            except Resolver404:
                pass

        return slug

    def clean(self):
        self.check_spam()
        return self.cleaned_data


class DeleteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article')
        self.has_children = kwargs.pop('has_children')
        super(DeleteForm, self).__init__(*args, **kwargs)

    confirm = forms.BooleanField(required=False,
                                 label=_('Yes, I am sure'))
    purge = forms.BooleanField(
        widget=HiddenInput(),
        required=False, label=_('Purge'),
        help_text=_(
            'Purge the article: Completely remove it (and all its contents) with no undo. Purging is a good idea if you want to free the slug such that users can create new articles in its place.'))
    revision = forms.ModelChoiceField(models.ArticleRevision.objects.all(),
                                      widget=HiddenInput(), required=False)

    def clean(self):
        cd = self.cleaned_data
        if not cd['confirm']:
            raise forms.ValidationError(ugettext('You are not sure enough!'))
        if cd['revision'] != self.article.current_revision:
            raise forms.ValidationError(
                ugettext(
                    'While you tried to delete this article, it was modified. TAKE CARE!'))
        return cd


class PermissionsForm(PluginSettingsFormMixin, forms.ModelForm):

    locked = forms.BooleanField(
        label=_('Lock article'),
        help_text=_('Deny all users access to edit this article.'),
        required=False)

    settings_form_headline = _('Permissions')
    settings_order = 5
    settings_write_access = False

    owner_username = forms.CharField(
        required=False,
        label=_('Owner'),
        help_text=_('Enter the username of the owner.'))
    group = forms.ModelChoiceField(
        Group.objects.all(),
        empty_label=_('(none)'),
        label=_('Group'),
        required=False)
    if settings.USE_BOOTSTRAP_SELECT_WIDGET:
        group.widget = SelectWidgetBootstrap()

    recursive = forms.BooleanField(
        label=_('Inherit permissions'),
        help_text=_(
            'Check here to apply the above permissions (excluding group and owner of the article) recursively to articles below this one.'),
        required=False)

    recursive_owner = forms.BooleanField(
        label=_('Inherit owner'),
        help_text=_(
            'Check here to apply the ownership setting recursively to articles below this one.'),
        required=False)

    recursive_group = forms.BooleanField(
        label=_('Inherit group'),
        help_text=_(
            'Check here to apply the group setting recursively to articles below this one.'),
        required=False)

    def get_usermessage(self):
        if self.changed_data:
            return _('Permission settings for the article were updated.')
        else:
            return _(
                'Your permission settings were unchanged, so nothing saved.')

    def __init__(self, article, request, *args, **kwargs):
        self.article = article
        self.user = request.user
        self.request = request
        kwargs['instance'] = article
        kwargs['initial'] = {'locked': article.current_revision.locked}

        super(PermissionsForm, self).__init__(*args, **kwargs)

        self.can_change_groups = False
        self.can_assign = False

        if permissions.can_assign(article, request.user):
            self.can_assign = True
            self.can_change_groups = True
            self.fields['group'].queryset = Group.objects.all()
        elif permissions.can_assign_owner(article, request.user):
            self.fields['group'].queryset = Group.objects.filter(
                user=request.user)
            self.can_change_groups = True
        else:
            # Quick-fix...
            # Set the group dropdown to readonly and with the current
            # group as only selectable option
            self.fields['group'] = forms.ModelChoiceField(
                queryset=Group.objects.filter(
                    id=self.instance.group.id)
                if self.instance.group else Group.objects.none(),
                empty_label=_('(none)'),
                required=False, widget=SelectWidgetBootstrap(
                    disabled=True)
                if settings.USE_BOOTSTRAP_SELECT_WIDGET else forms.Select(
                    attrs={'disabled': True}))
            self.fields['group_read'].widget = forms.HiddenInput()
            self.fields['group_write'].widget = forms.HiddenInput()

        if not self.can_assign:
            self.fields['owner_username'].widget = forms.TextInput(
                attrs={
                    'readonly': 'true'})
            self.fields['recursive'].widget = forms.HiddenInput()
            self.fields['recursive_group'].widget = forms.HiddenInput()
            self.fields['recursive_owner'].widget = forms.HiddenInput()
            self.fields['locked'].widget = forms.HiddenInput()

        self.fields['owner_username'].initial = getattr(
            article.owner,
            User.USERNAME_FIELD) if article.owner else ""

    def clean_owner_username(self):
        if self.can_assign:
            username = self.cleaned_data['owner_username']
            if username:
                try:
                    kwargs = {User.USERNAME_FIELD: username}
                    user = User.objects.get(**kwargs)
                except User.DoesNotExist:
                    raise forms.ValidationError(
                        ugettext('No user with that username'))
            else:
                user = None
        else:
            user = self.article.owner
        return user

    def save(self, commit=True):
        article = super(PermissionsForm, self).save(commit=False)

        # Alter the owner according to the form field owner_username
        # TODO: Why not rename this field to 'owner' so this happens
        # automatically?
        article.owner = self.cleaned_data['owner_username']

        # Revert any changes to group permissions if the
        # current user is not allowed (see __init__)
        # TODO: Write clean methods for this instead!
        if not self.can_change_groups:
            article.group = self.article.group
            article.group_read = self.article.group_read
            article.group_write = self.article.group_write

        if self.can_assign:
            if self.cleaned_data['recursive']:
                article.set_permissions_recursive()
            if self.cleaned_data['recursive_owner']:
                article.set_owner_recursive()
            if self.cleaned_data['recursive_group']:
                article.set_group_recursive()
            if self.cleaned_data[
                    'locked'] and not article.current_revision.locked:
                revision = models.ArticleRevision()
                revision.inherit_predecessor(self.article)
                revision.set_from_request(self.request)
                revision.automatic_log = _('Article locked for editing')
                revision.locked = True
                self.article.add_revision(revision)
            elif not self.cleaned_data['locked'] and article.current_revision.locked:
                revision = models.ArticleRevision()
                revision.inherit_predecessor(self.article)
                revision.set_from_request(self.request)
                revision.automatic_log = _('Article unlocked for editing')
                revision.locked = False
                self.article.add_revision(revision)

        article.save()

    class Meta:
        model = models.Article
        fields = (
            'locked',
            'owner_username',
            'recursive_owner',
            'group',
            'recursive_group',
            'group_read',
            'group_write',
            'other_read',
            'other_write',
            'recursive')
        widgets = {}


class DirFilterForm(forms.Form):

    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Filter...'),
                'class': 'search-query form-control'}),
        required=False)


class SearchForm(forms.Form):

    q = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Search...'),
                'class': 'search-query'}),
        required=False)


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # Add honeypots
        self.honeypot_fieldnames = "address", "phone"
        self.honeypot_class = ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for __ in range(10))
        self.honeypot_jsfunction = 'f' + ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for __ in range(10))

        for fieldname in self.honeypot_fieldnames:
            self.fields[fieldname] = forms.CharField(
                widget=forms.TextInput(attrs={'class': self.honeypot_class}),
                required=False,
            )

    def clean(self):
        cd = super(UserCreationForm, self).clean()
        for fieldname in self.honeypot_fieldnames:
            if cd[fieldname]:
                raise forms.ValidationError(
                    "Thank you, non-human visitor. Please keep trying to fill in the form.")
        return cd

    class Meta:
        model = User
        fields = ("username", "email")

class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label="New password", widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(), required=False)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email']
