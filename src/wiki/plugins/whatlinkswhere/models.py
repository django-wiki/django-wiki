""" Define a model for storing which article links to which other article
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


__all__ = ["InternalLink"]


class InternalLink(models.Model):
    """This model describes links between articles."""

    from_article = models.ForeignKey(
        "wiki.Article",
        on_delete=models.CASCADE,
        verbose_name=_("from_article"),
        related_name="links_from",
    )
    to_article = models.ForeignKey(
        "wiki.Article",
        on_delete=models.CASCADE,
        verbose_name=_("to_article"),
        related_name="links_to",
    )

    # Permission methods - you should override these, if they don't fit your
    # logic.
    def can_read(self, user):
        return self.from_article.can_read(user) and self.to_article.can_read(user)

    def can_write(self, user):
        return self.from_article.can_write(user) and self.to_article.can_write(user)

    def can_delete(self, user):
        return self.from_article.can_delete(user) and self.to_article.can_delete(user)

    def can_moderate(self, user):
        return self.from_article.can_moderate(user) and self.to_article.can_moderate(
            user
        )

    def purge(self):
        """Remove related contents completely, ie. media files."""
        pass

    def __str__(self):
        title = _("Article {:s} links to {:s}").format(
            self.from_article.current_revision.title,
            self.to_article.current_revision.title,
        )
        return str(title)

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        # Matches label of upcoming 0.1 release
        db_table = "wiki_whatlinkswhere_internallink"
