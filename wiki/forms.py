from django import forms
from django.utils.translation import ugettext as _

import editors
from django.utils.safestring import mark_safe

class CreateRoot(forms.Form):
    
    title = forms.CharField(label=_(u'Title'), help_text=_(u'Initial title of the article. May be overridden with revision titles.'))
    content = forms.CharField(label=_(u'Type in some contents'),
                              help_text=_(u'This is just the initial contents of your article. After creating it, you can use more complex features like adding plugins, meta data, related articles etc...'),
                              required=False, widget=editors.editor.get_widget())
    

class EditForm(forms.Form):
    
    title = forms.CharField(label=_(u'Title'),)
    content = forms.CharField(label=_(u'Contents'),
                              required=False, widget=editors.editor.get_widget())
    
    summary = forms.CharField(label=_(u'Summary'), help_text=_(u'Give a short reason for your edit, which will be stated in the revision log.'),
                              required=False)
    
    def __init__(self, instance, *args, **kwargs):
        
        self.preview = kwargs.pop('preview', False)
        if instance:
            initial = {'content': instance.content,
                       'title': instance.title,}
            initial.update(kwargs.get('initial', {}))
            kwargs['initial'] = initial
        
        self.instance = instance
        
        super(EditForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cd = self.cleaned_data
        if cd['title'] == self.instance.title and cd['content'] == self.instance.content:
            raise forms.ValidationError(_(u'No changes made. Nothing to save.'))
        return cd

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
        self.fields['slug'].widget = TextInputPrepend(prepend='/'+urlpath_parent.path)
    
    title = forms.CharField(label=_(u'Title'),)
    slug = forms.SlugField(label=_(u'Slug'), help_text=_(u"Use only alphanumeric characters and '-' or '_'."),)
    content = forms.CharField(label=_(u'Contents'),
                              required=False, widget=editors.editor.get_widget())
    
    summary = forms.CharField(label=_(u'Summary'), help_text=_(u"Write a brief message for the article's history log."),
                              required=False)
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug[0] == "_":
            raise forms.ValidationError(_(u'A slug may not begin with an underscore.'))
        return slug
