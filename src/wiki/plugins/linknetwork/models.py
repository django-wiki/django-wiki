"""Define a model for storing which article links to which other article

Also define the function that stores links in that model, and connect it to the
ArticleRevision.post_save signal, so that links are always as up-to-date as
article revisions.

"""
from urllib.parse import urljoin
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

from django.db import models
from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.utils.translation import gettext_lazy as _
from wiki import models as wiki_models
from wiki.core.exceptions import NoRootURL
from wiki.core.markdown import article_markdown
from wiki.decorators import which_article


__all__ = ["InternalLink", "store_links"]


class InternalLink(models.Model):
    """This model describes links between articles."""

    from_article = models.ForeignKey(
        "wiki.Article",
        on_delete=models.CASCADE,
        verbose_name=_("from_article"),
        related_name="links",
    )
    to_article = models.ForeignKey(
        "wiki.Article",
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("to_article"),
        related_name="incoming_links",
    )
    to_nonexistant_url = models.CharField(
        max_length=512,
        null=True,
        verbose_name=_("nonexistant_url"),
        help_text=_("The target of this link is not in the wiki [yet]"),
    )

    def __str__(self):
        return _("Article {:s} links to {:s}").format(
            self.from_article.current_revision.title,
            self.to_article.current_revision.title
            if self.to_article
            else self.to_nonexistant_url,
        )

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        # Matches label of upcoming 0.1 release
        db_table = "wiki_linknetwork_internallink"

    @classmethod
    def store_link(cls, from_url, from_article, el):
        href = el.get("href")
        try:
            assert href
            url = urlparse(href)
            # Ensure that path ends with a slash
            assert not url.scheme
            assert not url.netloc
            target = urljoin(from_url, url.path.rstrip("/") + "/")
            resolution = resolve(target)
            assert resolution.app_names == ["wiki"]
            article, destination = which_article(**resolution.kwargs)
            # All other cases have raised exceptions: We have an internal link,
            # which should be reflected in the database.
            return cls.objects.create(
                from_article=from_article, to_article=article
            ).save()
        except (AssertionError, TypeError, ValueError, Resolver404, NoRootURL):
            # No wiki-internal link
            return
        except (
            wiki_models.URLPath.DoesNotExist,
            wiki_models.Article.DoesNotExist,
        ):
            # ‘red’ link to unwritten article.
            return cls.objects.create(
                from_article=from_article, to_nonexistant_url=target
            ).save()


def store_links(instance, *args, **kwargs):
    try:
        html = ET.fromstring(
            "<body>{:s}</body>".format(
                article_markdown(instance.content, instance.article, False)
            )
        )
    except ET.ParseError:
        # There are some cases where markdown doesn't evaluate to clean html.
        # It would probably be worth checking *how* they fail, but for now we
        # should at least not DIE due to them.
        return

    url = instance.article.get_absolute_url()
    article = instance.article

    for link in InternalLink.objects.filter(to_nonexistant_url=url).all():
        link.to_nonexistant_url = None
        link.to_article = article
        link.save()

    InternalLink.objects.filter(from_article=article).delete()

    for el in html.iter():
        if el.tag != "a":
            continue
        InternalLink.store_link(url, article, el)


# Whenever a new revision is created, update all links in there
models.signals.post_save.connect(
    store_links,
    sender=wiki_models.ArticleRevision,
)
