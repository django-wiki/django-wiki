import json

from markdown.extensions.toc import slugify
from markdown.extensions.toc import TocExtension
from markdown.extensions.toc import TocTreeprocessor
from wiki.plugins.macros import settings

HEADER_ID_PREFIX = "wiki-toc-"


def process_toc_depth(toc_depth):
    if isinstance(toc_depth, str) and "-" in toc_depth:
        toc_top, toc_bottom = [int(x) for x in toc_depth.split("-")]
    else:
        toc_top = 1
        toc_bottom = int(toc_depth)
    return {"toc_top": toc_top, "toc_bottom": toc_bottom}


def process_value(org_val, new_val):
    try:
        if type(new_val) is str:
            new_val = new_val.lstrip("'").rstrip("'")
            if type(org_val) is not str:
                new_val = json.loads(new_val.lower())
        elif type(new_val) is not type(org_val):
            new_val = type(org_val)(new_val)
    except Exception:
        return org_val
    else:
        return new_val


def wiki_slugify(*args, **kwargs):
    return HEADER_ID_PREFIX + slugify(*args, **kwargs)


class WikiTreeProcessorClass(TocTreeprocessor):
    CACHED_KWARGS = dict()  # Used to cache arguments parsed by the MacroPattern
    # Used to map the keyword arguments to the Class Objects attribute name.
    TOC_CONFIG_VALUES = {
        "title": "title",
        "baselevel": "base_level",
        "separator": "sep",
        "anchorlink": "use_anchors",
        "anchorlink_class": "anchorlink_class",
        "permalink": "use_permalinks",
        "permalink_class": "permalink_class",
        "permalink_title": "permalink_title",
        "toc_depth": process_toc_depth,
        "toc_top": "toc_top",
        "toc_bottom": "toc_bottom",
    }

    def run(self, doc):
        # Necessary because self.title is set to a LazyObject via gettext_lazy
        if self.title:
            self.title = str(self.title)

        tmp_kwargs = dict()
        try:
            # Set config and save defaults to tmp
            for k, v in WikiTreeProcessorClass.CACHED_KWARGS.items():
                if k in WikiTreeProcessorClass.TOC_CONFIG_VALUES:
                    if callable(WikiTreeProcessorClass.TOC_CONFIG_VALUES[k]):
                        for tock, tocv in WikiTreeProcessorClass.TOC_CONFIG_VALUES[k](
                            v
                        ).items():
                            tmp_kwargs[tock] = getattr(
                                self, WikiTreeProcessorClass.TOC_CONFIG_VALUES[tock]
                            )
                            setattr(
                                self,
                                WikiTreeProcessorClass.TOC_CONFIG_VALUES[tock],
                                process_value(tmp_kwargs[tock], tocv),
                            )
                    else:
                        tmp_kwargs[
                            WikiTreeProcessorClass.TOC_CONFIG_VALUES[k]
                        ] = getattr(self, WikiTreeProcessorClass.TOC_CONFIG_VALUES[k])
                        setattr(
                            self,
                            WikiTreeProcessorClass.TOC_CONFIG_VALUES[k],
                            process_value(
                                tmp_kwargs[WikiTreeProcessorClass.TOC_CONFIG_VALUES[k]],
                                v,
                            ),
                        )
            super().run(doc)
        finally:
            # Use tmp to reset values
            for k, v in tmp_kwargs.items():
                if hasattr(self, k):
                    setattr(self, k, v)
            # Unset cached kwargs
            WikiTreeProcessorClass.CACHED_KWARGS = dict()


class WikiTocExtension(TocExtension):
    TreeProcessorClass = WikiTreeProcessorClass

    def __init__(self, **kwargs):
        kwargs.setdefault("slugify", wiki_slugify)
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        if "toc" in settings.METHODS:
            TocExtension.extendMarkdown(self, md)


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return WikiTocExtension(*args, **kwargs)
