from django import forms
from django.utils.translation import ugettext as _

class CreateRoot(forms.Form):
    
    title = forms.CharField(label=_(u'Title'), help_text=_(u'Initial title of the article. May be overridden with revision titles.'))
    content = forms.CharField(label=_(u'Type in some contents'),
                              help_text=_(u'This is just the initial contents of your article. After creating it, you can use more complex features like adding plugins, meta data, related articles etc...'),
                              required=False)
    
