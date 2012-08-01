from django import forms
from django.utils.translation import ugettext as _

class SubscriptionForm(forms.Form):
    
    settings_form_id = "notifications"
    settings_form_headline = _(u'Notifications')
    settings_order = 1
    settings_write_access = False
    
    def __init__(self, article, *args, **kwargs):
        
        self.article = article
        super(SubscriptionForm, self).__init__(*args, **kwargs)
    
    notify_edit = forms.BooleanField(required=False, label=_(u'Notify me on article edits'))
    receive_email = forms.BooleanField(required=False, label=_(u'Notify me directly by email'))
    
