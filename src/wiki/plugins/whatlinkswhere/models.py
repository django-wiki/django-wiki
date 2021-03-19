"""Define a model for storing which article links to which other article

Also define the function that stores links in that model, and connect it to the
ArticleRevision.post_save signal, so that links are always as up-to-date as
article revisions.

"""
from urllib.parse import urljoin
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

from django.db import models
from django.utils.translation import gettext_lazy as _
from wiki import models as wiki_models
from wiki.core.markdown import article_markdown


__all__ = ["InternalLink", "store_links"]


class InternalLink(models.Model):
    """This model describes links between articles."""

    from_url = models.ForeignKey(
        "wiki.URLPath",
        on_delete=models.CASCADE,
        verbose_name=_("from_url"),
        related_name="links_from",
    )
    to_url = models.ForeignKey(
        "wiki.URLPath",
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("to_url"),
        related_name="links_to",
    )
    to_nonexistant_url = models.CharField(
        max_length=512,
        null=True,
        verbose_name=_("nonexistant_url"),
        help_text=_("The target of this link is not in the wiki [yet]"),
    )

    # Permission methods - you should override these, if they don't fit your
    # logic.
    def can_read(self, user):
        return self.from_url.article.can_read(user) and (
            not self.to_url or self.to_url.article.can_read(user)
        )

    def __str__(self):
        title = _("Article {:s} links to {:s}").format(
            self.from_url.article.current_revision.title,
            self.to_url.article.current_revision.title
            if self.to_url
            else self.to_nonexistant_url,
        )
        return str(title)

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        # Matches label of upcoming 0.1 release
        db_table = "wiki_whatlinkswhere_internallink"


def store_link(from_urls, el, root):
    href = el.get("href")
    if not href:
        # Anchor, not link
        return

    try:
        url = urlparse(href)
    except ValueError:
        return
    if url.scheme or url.netloc:
        # External link
        return

    # Ensure that path ends with a slash
    target = urljoin(from_urls[0].path, url.path.rstrip("/") + "/")

    try:
        to_url = wiki_models.URLPath.get_by_path(target)
    except wiki_models.URLPath.DoesNotExist:
        # ‘red’ link to unwritten article.
        for from_url in from_urls:
            InternalLink.objects.create(
                from_url=from_url, to_nonexistant_url=target
            ).save()
        return

    # All other cases have been handled: We have an internal link, which
    # should be reflected in the database.
    for from_url in from_urls:
        InternalLink.objects.create(from_url=from_url, to_url=to_url).save()
    return


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

    from_urls = instance.article.urlpath_set.all()

    if not from_urls:
        # I have seen this happen in test cases made for the edit section and
        # the wiki path extension components. I think it was caused by the fact
        # that article revisions were created before their URLPath objects,
        # which I changed.
        return

    for url in from_urls:
        for link in InternalLink.objects.filter(
            to_nonexistant_url="/" + url.path
        ).all():
            link.to_nonexistant_url = None
            link.to_url = url
            link.save()

    for url in from_urls:
        InternalLink.objects.filter(from_url=url).delete()
    wiki_root = wiki_models.URLPath.get_by_path("")

    for el in html.iter():
        if el.tag != "a":
            continue
        store_link(from_urls, el, wiki_root)


# Whenever a new revision is created, update all links in there
models.signals.post_save.connect(
    store_links,
    sender=wiki_models.ArticleRevision,
)