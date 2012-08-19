from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView

from wiki.decorators import get_article
from wiki.plugins.images import models
from wiki.views.mixins import ArticleMixin

class ImageView(ArticleMixin, ListView):
    
    template_name = 'wiki/plugins/images/index.html'
    allow_empty = True
    context_object_name = 'images'
    paginate_by = 10
    
    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        return super(ImageView, self).dispatch(request, article, *args, **kwargs)
    
    def get_queryset(self):
        if (self.request.user.has_perm('wiki.moderator') or
            self.article.owner == self.request.user):
            images = models.Image.objects.filter(article=self.article)
        else:
            images = models.Image.objects.filter(article=self.article,
                                                 current_revision__deleted=False)            
        images.select_related()
        return images
    
    def get_context_data(self, **kwargs):
        kwargs.update(ArticleMixin.get_context_data(self, **kwargs))
        return ListView.get_context_data(self, **kwargs)

class DeleteView(ArticleMixin, RedirectView):
    
    permanent = False
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.image = get_object_or_404(models.Image, article=article,
                                       id=kwargs.get('image_id', None))
        self.restore = kwargs.get('restore', False)
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)
    
    def get_redirect_url(self, **kwargs):
        
        new_revision = models.ImageRevision()
        new_revision.inherit_predecessor(self.image)
        new_revision.set_from_request(self.request)
        new_revision.deleted = not self.restore
        new_revision.save()
        self.image.current_revision = new_revision
        self.image.save()
        if self.restore:
            messages.info(self.request, _('%s has been marked as deleted') % new_revision.get_filename())
        else:
            messages.info(self.request, _('%s has been restored') % new_revision.get_filename())
        if self.urlpath:
            return reverse('wiki:images_index', kwargs={'path': self.urlpath.path})
        return reverse('wiki:images_index', kwargs={'article_id': self.article.id})

class RevisionChangeView(ArticleMixin, RedirectView):

    permanent = False
    
    @method_decorator(get_article(can_write=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.image = get_object_or_404(models.Image, article=article,
                                       id=kwargs.get('image_id', None))
        self.revision = get_object_or_404(models.ImageRevision, plugin__article=article,
                                       id=kwargs.get('rev_id', None))
        return ArticleMixin.dispatch(self, request, article, *args, **kwargs)
    
    def get_redirect_url(self, **kwargs):
        
        self.image.current_revision = self.revision
        self.image.save()
        messages.info(self.request, _('%(file)s has been changed to revision #%(revision)d') %
                      {'file': self.image.current_revision.imagerevision.get_filename(),
                       'revision': self.revision.revision_number})
        if self.urlpath:
            return reverse('wiki:images_index', kwargs={'path': self.urlpath.path})
        return reverse('wiki:images_index', kwargs={'article_id': self.article.id})
