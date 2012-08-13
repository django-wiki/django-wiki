from django.db import models
from django.utils.translation import ugettext_lazy as _

import settings

from wiki.models.pluginbase import RevisionPlugin

class Image(RevisionPlugin):
    
    image = models.ImageField(upload_to=settings.IMAGE_PATH)
    
    caption = models.CharField(max_length=2056, null=True, blank=True)
    
    def render_caption(self):
        """Returns a rendered version of the caption. Should only use a
        subset of the rendering machine."""
        pass
    
    class Meta:
        verbose_name = _(u'image')
        verbose_name_plural = _(u'images')
