from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext_lazy as _

import settings

from wiki.models.pluginbase import RevisionPlugin

if not "sorl.thumbnail" in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('wiki.plugins.images: needs sorl.thumbnail in INSTALLED_APPS')

class Image(RevisionPlugin):
    
    image = models.ImageField(upload_to=settings.IMAGE_PATH,
                              max_length=2000)
    
    
    
    def get_filename(self):
        if self.image:
            return self.image.path.split('/')[-1]
    
    class Meta:
        verbose_name = _(u'image')
        verbose_name_plural = _(u'images')
        app_label = settings.APP_LABEL
    
    def __unicode__(self):
        return _(u'Image: %s') % self.get_filename()
    