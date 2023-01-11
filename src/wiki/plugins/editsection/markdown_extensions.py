import logging
import re
from xml.etree import ElementTree as etree

from django.urls import reverse
from markdown import Extension
from markdown.blockprocessors import HashHeaderProcessor
from markdown.blockprocessors import SetextHeaderProcessor
from markdown.treeprocessors import Treeprocessor
from wiki.core.markdown import add_to_registry
from wiki.plugins.macros.mdx.toc import wiki_slugify

from . import settings


logger = logging.getLogger("MARKDOWN")


class CustomHashHeaderProcessor(HashHeaderProcessor):
    """
    Custom HashHeaderProcessor. The only difference to the upstream
    processor is that we set the data-block-source attribute on any
    inserted header.
    """

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[: m.start()]  # All lines before header
            after = block[m.end() :]  # All lines after header
            if before:
                # As the header was not the first line of the block and the
                # lines before the header must be parsed first,
                # recursively parse this lines as a block.
                self.parser.parseBlocks(parent, [before])
            # Create header using named groups from RE
            h = etree.SubElement(parent, "h%d" % len(m.group("level")))
            h.text = m.group("header").strip()
            h.attrib["data-block-source"] = m.group().strip()
            if after:
                # Insert remaining lines as first block for future parsing.
                blocks.insert(0, after)
        else:  # pragma: no cover
            # This should never happen, but just in case...
            logger.warning("We've got a problem header: %r" % block)


class CustomSetextHeaderProcessor(SetextHeaderProcessor):
    """
    Custom SetextHeaderProcessor. The only difference to the upstream
    processor is that we set the data-block-source attribute on any
    inserted header.
    """

    def run(self, parent, blocks):
        lines = blocks.pop(0).split("\n")
        # Determine level. ``=`` is 1 and ``-`` is 2.
        if lines[1].startswith("="):
            level = 1
        else:
            level = 2
        h = etree.SubElement(parent, "h%d" % level)
        h.text = lines[0].strip()
        h.attrib["data-block-source"] = "\r\n".join(lines)
        if len(lines) > 2:
            # Block contains additional lines. Add to  master blocks for later.
            blocks.insert(0, "\n".join(lines[2:]))


class EditSectionExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "level": [settings.MAX_LEVEL, "Allow to edit sections until this level"]
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        # replace HashHeader/SetextHeader processors with our custom variants
        md.parser.blockprocessors.register(
            CustomHashHeaderProcessor(md.parser), "hashheader", 70
        )
        md.parser.blockprocessors.register(
            CustomSetextHeaderProcessor(md.parser), "setextheader", 60
        )
        # the tree processor adds the actual edit links
        add_to_registry(
            md.treeprocessors,
            "editsection",
            EditSectionProcessor(self.config, md),
            "_end",
        )


class EditSectionProcessor(Treeprocessor):
    """
    TreeProcessor adds the edit links for every header which has a data-block-source attribute
    """

    def __init__(self, config, md=None):
        self.config = config
        self.slugs = {}  # keep found slugs (to ensure uniqueness)
        self.source = None  # will be set in run()
        self.last_start = 0  # location of last inserted edit link
        super().__init__(md)

    def ensure_unique_id(self, node):
        """ensures that node has a unique id, preferring an already existing id"""
        if "id" in node.attrib:
            slug = node.attrib["id"]
        else:
            content = node.text.strip()
            slug = wiki_slugify(content, "-", unicode=True)
        candidate = slug
        i = 1
        while candidate in self.slugs:
            candidate = "{}_{}".format(slug, i)
            i += 1
        self.slugs[candidate] = True
        node.attrib["id"] = candidate
        return candidate

    def add_links(self, node):
        headers = []
        for child in list(node):
            match = self.HEADER_RE.match(child.tag.lower())
            if not match:
                continue
            level = match.group(1)

            if "data-block-source" in child.attrib:
                source_block = child.attrib["data-block-source"]
                del child.attrib["data-block-source"]
                # locate in document source
                start = self.source.find(source_block, self.last_start)
                if start == -1:
                    # not found in source, ignore
                    continue
                self.last_start = start + 1

                # ensure that the node has a unique id
                slug = self.ensure_unique_id(child)

                # Insert link to allow editing this section
                link = etree.SubElement(child, "a")
                link.text = settings.LINK_TEXT
                link.attrib["class"] = "article-edit-title-link"

                # Build the URL
                url_kwargs = self.md.article.get_url_kwargs()
                url_kwargs["header"] = child.attrib["id"]
                link.attrib["href"] = reverse("wiki:editsection", kwargs=url_kwargs)

                headers.append(
                    {
                        "slug": slug,
                        "position": start,
                        "level": level,
                        "source": source_block,
                    }
                )
        return headers

    def run(self, root):
        self.level = self.config.get("level")[0]
        self.article = self.md.article
        self.source = self.md.source
        self.HEADER_RE = re.compile(
            "^h([" + "".join(map(str, range(1, self.level + 1))) + "])"
        )
        headers = self.add_links(root)
        # store found headers at article, for use in edit view
        self.article._found_headers = headers
        return root
