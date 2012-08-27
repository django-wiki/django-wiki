# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape

from itertools import chain

from wiki import models
from wiki.conf import settings
from wiki.editors import getEditor
from wiki.core.diff import simple_merge
from django.forms.widgets import HiddenInput
from wiki.core.plugins.base import PluginSettingsFormMixin
from django.contrib.auth.models import User
from wiki.core import permissions

class SpamProtectionMixin():
    
    def check_spam(self, current_revision, request):
        """Check that user or IP address does not perform content edits that
        are not allowed.
        
        current_revision can be any object inheriting from models.BaseRevisionMixin 
        """
        ipaddress = request.META.get('REMOTE_ADDR', None)
        if not ipaddress == "127.0.0.1":
            raise forms.ValidationError(_('Only localhost... muahahaha'))
        # TODO: Finish this stuff and integrate it in forms....


class CreateRootForm(forms.Form):
    
    title = forms.CharField(label=_(u'Title'), help_text=_(u'Initial title of the article. May be overridden with revision titles.'))
    content = forms.CharField(label=_(u'Type in some contents'),
                              help_text=_(u'This is just the initial contents of your article. After creating it, you can use more complex features like adding plugins, meta data, related articles etc...'),
                              required=False, widget=getEditor().get_widget()) #@UndefinedVariable
    

class EditForm(forms.Form):
    
    title = forms.CharField(label=_(u'Title'),)
    content = forms.CharField(label=_(u'Contents'),
                              required=False, widget=getEditor().get_widget()) #@UndefinedVariable
    
    summary = forms.CharField(label=_(u'Summary'), help_text=_(u'Give a short reason for your edit, which will be stated in the revision log.'),
                              required=False)
    
    current_revision = forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    def __init__(self, current_revision, *args, **kwargs):
        
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
            if not data:
                data = kwargs.get('data', None)
            if data:
                self.presumed_revision = data.get('current_revision', None)
                if not str(self.presumed_revision) == str(self.initial_revision.id):
                    newdata = {}
                    for k,v in data.items():
                        newdata[k] = v
                    newdata['current_revision'] = self.initial_revision.id
                    newdata['content'] = simple_merge(self.initial_revision.content,
                                                      data.get('content', ""))
                    newdata['title'] = current_revision.title
                    kwargs['data'] = newdata
                
            kwargs['initial'] = initial
        
        super(EditForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cd = self.cleaned_data
        if self.no_clean or self.preview:
            return cd
        if not str(self.initial_revision.id) == str(self.presumed_revision):
            raise forms.ValidationError(_(u'While you were editing, someone else changed the revision. Your contents have been automatically merged with the new contents. Please review the text below.'))
        if cd['title'] == self.initial_revision.title and cd['content'] == self.initial_revision.content:
            raise forms.ValidationError(_(u'No changes made. Nothing to save.'))
        return cd


class SelectWidgetBootstrap(forms.Select):
    """
    http://twitter.github.com/bootstrap/components.html#buttonDropdowns
    Needs bootstrap and jquery
    """
    js = ("""
    <script type="text/javascript">
        function setBtnGroupVal(elem) {
            btngroup = $(elem).parents('.btn-group');
            selected_a = btngroup.find('a[selected]');
            if (selected_a.length > 0) {
                val = selected_a.attr('data-value');
                label = selected_a.html();
            } else {
                btngroup.find('a').first().attr('selected', 'selected');
                setBtnGroupVal(elem);
            }
            btngroup.find('input').val(val);
            btngroup.find('.btn-group-label').html(label);
        }
        $(document).ready(function() {
            $('.btn-group-form input').each(function() {
                setBtnGroupVal(this);
            });
            $('.btn-group-form li a').click(function() {
                $(this).parent().siblings().find('a').attr('selected', false);
                $(this).attr('selected', true);
                setBtnGroupVal(this);
            });
        })
    </script>
    """)
    def __init__(self, attrs={'class': 'btn-group pull-left btn-group-form'}, choices=()):
        self.noscript_widget = forms.Select(attrs={}, choices=choices)
        super(SelectWidgetBootstrap, self).__init__(attrs, choices)
    
    def __setattr__(self, k, value):
        super(SelectWidgetBootstrap, self).__setattr__(k, value)
        if k != 'attrs':
            self.noscript_widget.__setattr__(k, value)
    
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = ["""<div%(attrs)s>"""
                  """    <button class="btn btn-group-label" type="button">%(label)s</button>"""
                  """    <button class="btn dropdown-toggle" type="button" data-toggle="dropdown">"""
                  """        <span class="caret"></span>"""
                  """    </button>"""
                  """    <ul class="dropdown-menu">"""
                  """        %(options)s"""
                  """    </ul>"""
                  """    <input type="hidden" name="%(name)s" value="" class="btn-group-value" />"""
                  """</div>"""
                  """%(js)s"""
                  """<noscript>%(noscript)s</noscript>"""
                   % {'attrs': flatatt(final_attrs),
                      'options':self.render_options(choices, [value]),
                      'label': _(u'Select an option'),
                      'name': name,
                      'js': SelectWidgetBootstrap.js,
                      'noscript': self.noscript_widget.render(name, value, {}, choices)} ]
        return mark_safe(u'\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        return u'<li><a href="javascript:void(0)" data-value="%s"%s>%s</a></li>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<li class="divider" label="%s"></li>' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)
    

class TextInputPrepend(forms.TextInput):
    
    def __init__(self, *args, **kwargs):
        self.prepend = kwargs.pop('prepend', "")
        super(TextInputPrepend, self).__init__(*args, **kwargs)
    
    def render(self, *args, **kwargs):
        html = super(TextInputPrepend, self).render(*args, **kwargs)
        return mark_safe('<div class="input-prepend"><span class="add-on">%s</span>%s</div>' % (self.prepend, html))
    

class CreateForm(forms.Form):
    
    def __init__(self, urlpath_parent, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.urlpath_parent = urlpath_parent
    
    title = forms.CharField(label=_(u'Title'),)
    slug = forms.SlugField(label=_(u'Slug'), help_text=_(u"This will be the address where your article can be found. Use only alphanumeric characters and - or _. Note that you cannot change the slug after creating the article."),)
    content = forms.CharField(label=_(u'Contents'),
                              required=False, widget=getEditor().get_widget()) #@UndefinedVariable
    
    summary = forms.CharField(label=_(u'Summary'), help_text=_(u"Write a brief message for the article's history log."),
                              required=False)
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug.startswith("_"):
            raise forms.ValidationError(_(u'A slug may not begin with an underscore.'))
        
        if settings.URL_CASE_SENSITIVE:
            already_existing_slug = models.URLPath.objects.filter(slug=slug, parent=self.urlpath_parent)
        else:
            already_existing_slug = models.URLPath.objects.filter(slug__iexact=slug, parent=self.urlpath_parent)
        if already_existing_slug:
            already_urlpath = already_existing_slug[0]
            if already_urlpath.article and already_urlpath.article.current_revision.deleted:
                raise forms.ValidationError(_(u'A deleted article with slug "%s" already exists.') % already_urlpath.slug)
            else:
                raise forms.ValidationError(_(u'A slug named "%s" already exists.') % already_urlpath.slug)
        
        return slug


class DeleteForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article')
        self.has_children = kwargs.pop('has_children')
        super(DeleteForm, self).__init__(*args, **kwargs)
    
    confirm = forms.BooleanField(required=False,
                                 label=_(u'Yes, I am sure'))
    purge = forms.BooleanField(widget=HiddenInput(), required=False,
                               label=_(u'Purge'),
                               help_text=_(u'Purge the article: Completely remove it (and all its contents) with no undo. Purging is a good idea if you want to free the slug such that users can create new articles in its place.'))
    revision = forms.ModelChoiceField(models.ArticleRevision.objects.all(),
                                      widget=HiddenInput(), required=False)
    
    def clean(self):
        cd = self.cleaned_data
        if not cd['confirm']:
            raise forms.ValidationError(_(u'You are not sure enough!'))
        if cd['revision'] != self.article.current_revision:
            raise forms.ValidationError(_(u'While you tried to delete this article, it was modified. TAKE CARE!'))
        return cd


class PermissionsForm(PluginSettingsFormMixin, forms.ModelForm):
    
    locked = forms.BooleanField(label=_(u'Lock article'), help_text=_(u'Deny all users access to edit this article.'),
                                required=False)

    settings_form_headline = _(u'Permissions')
    settings_order = 5
    settings_write_access = False

    owner_username = forms.CharField(required=False, label=_(u'Owner'),
                                     help_text=_(u'Enter the username of the owner.'))
    group = forms.ModelChoiceField(models.Group.objects.all(), empty_label=_(u'(none)'),
                                     required=False)
    if settings.USE_BOOTSTRAP_SELECT_WIDGET:
        group.widget= SelectWidgetBootstrap()
    
    recursive = forms.BooleanField(label=_(u'Inherit permissions'), help_text=_(u'Check here to apply the above permissions recursively to articles under this one.'),
                                   required=False)
    
    def get_usermessage(self):
        if self.changed_data:
            return _('Permission settings for the article were updated.')
        else:
            return _('Your permission settings were unchanged, so nothing saved.')
    
    def __init__(self, article, request, *args, **kwargs):
        self.article = article
        self.user = request.user
        self.request = request
        kwargs['instance'] = article
        kwargs['initial'] = {'locked': article.current_revision.locked}
        super(PermissionsForm, self).__init__(*args, **kwargs)
        
        self.can_change_groups = False
        self.can_assign = False
        
        print "checking can_assing", permissions.can_assign(article, request.user), request.user.is_staff
        if permissions.can_assign(article, request.user):
            self.can_assign = True
            self.fields['group'].queryset = models.Group.objects.all()
        elif permissions.can_assign_owner(article, request.user):
            self.fields['group'].queryset = models.Group.objects.filter(user=request.user)
            self.can_change_groups = True
        else:
            self.fields['group'].widget = forms.HiddenInput()
            self.fields['group_read'].widget = forms.HiddenInput()
            self.fields['group_write'].widget = forms.HiddenInput()
            
        if not self.can_assign:
            self.fields['owner_username'].widget = forms.HiddenInput()
            self.fields['recursive'].widget = forms.HiddenInput()
            self.fields['locked'].widget = forms.HiddenInput()
        
        self.fields['owner_username'].initial = article.owner.username if article.owner else ""
    
    def clean_owner_username(self):
        if self.can_assign:
            username = self.cleaned_data['owner_username']
            if username:
                try:
                    user = User.objects.get(username=username)
                except models.User.DoesNotExist:
                    raise forms.ValidationError(_(u'No user with that username'))
            else:
                user = None
        else:
            user = self.article.owner
        return user
    
    def save(self, commit=True):
        article = super(PermissionsForm, self).save(commit=False)
        article.owner = self.cleaned_data['owner_username']
        if not self.can_change_groups:
            article.group = self.article.group
            article.group_read = self.article.group_read
            article.group_write = self.article.group_write
        
        if self.can_assign:
            if self.cleaned_data['recursive']:
                article.set_permissions_recursive()
            if self.cleaned_data['locked'] and not article.current_revision.locked:
                revision = models.ArticleRevision()
                revision.inherit_predecessor(self.article)
                revision.set_from_request(self.request)
                revision.automatic_log = _(u'Article locked for editing')
                revision.locked = True
                self.article.add_revision(revision)
            elif not self.cleaned_data['locked'] and article.current_revision.locked:
                revision = models.ArticleRevision()
                revision.inherit_predecessor(self.article)
                revision.set_from_request(self.request)
                revision.automatic_log = _(u'Article unlocked for editing')
                revision.locked = False
                self.article.add_revision(revision)                
        
        article.save()
    
    class Meta:
        model = models.Article
        fields = ('locked', 'owner_username', 'group', 'group_read', 'group_write', 'other_read', 'other_write',
                  'recursive')

class DirFilterForm(forms.Form):
    
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _(u'Filter...'),
                                                          'class': 'search-query'}), required=False)

class SearchForm(forms.Form):
    
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _(u'Search...'),
                                                          'class': 'search-query'}), required=False)
