import re

from django.urls import reverse
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree

from . import settings


class EditSectionExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "level": [settings.MAX_LEVEL, "Allow to edit sections until this level"],
            "headers": None,  # List of FindHeader, all headers with there positions
            "location": None,  # To be extracted header
            "header_id": None,  # Header text ID of the to be extracted header
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        ext = EditSectionProcessor(md)
        ext.config = self.config
        md.treeprocessors.add("editsection", ext, "_end")


def get_header_id(header):
    header_id = "".join(w[0] for w in re.findall(r"\w+", header))
    if not len(header_id):
        return "_"
    return header_id


class EditSectionProcessor(Treeprocessor):
    def locate_section(self, node):
        cur_pos = [0] * self.level
        last_level = 0
        cur_header = -1
        sec_level = -1
        sec_start = -1

        for child in node.getchildren():
            match = self.HEADER_RE.match(child.tag.lower())
            if not match:
                continue

            level = int(match.group(1))

            # Find current position in headers
            cur_header += 1
            while (
                cur_header < len(self.headers)
                and not self.headers[cur_header].sure_header
                and child.text != self.headers[cur_header].header
            ):
                cur_header += 1
            if cur_header >= len(self.headers):
                return None

            # End of the searched section found?
            if level <= sec_level:
                return sec_start, self.headers[cur_header].start

            for l in range(level, last_level):
                cur_pos[l] = 0
            cur_pos[level - 1] += 1
            last_level = level

            location = "-".join(map(str, cur_pos))
            if location != self.location:
                continue

            # Found section start. Check if the header id text is still correct.
            if get_header_id(child.text) != self.header_id:
                return None

            # Correct section start found. Search now for the section end.
            sec_level = level
            sec_start = self.headers[cur_header].start

        if sec_start >= 0:
            return sec_start, 9999999
        return None

    def add_links(self, node):
        cur_pos = [0] * self.level
        last_level = 0

        for child in node.getchildren():
            match = self.HEADER_RE.match(child.tag.lower())
            if not match:
                continue

            level = int(match.group(1))
            for l in range(level, last_level):
                cur_pos[l] = 0
            cur_pos[level - 1] += 1
            last_level = level
            location = "-".join(map(str, cur_pos))
            header_id = get_header_id(child.text)

            # Insert link to allow editing this section
            link = etree.SubElement(child, "a")
            link.text = settings.LINK_TEXT
            link.attrib["class"] = "article-edit-title-link"

            # Build the URL
            url_kwargs = self.md.article.get_url_kwargs()
            url_kwargs["location"] = location
            url_kwargs["header"] = header_id
            link.attrib["href"] = reverse("wiki:editsection", kwargs=url_kwargs)

    def run(self, root):
        self.level = self.config.get("level")[0]
        self.HEADER_RE = re.compile(
            "^h([" + "".join(map(str, range(1, self.level + 1))) + "])"
        )
        self.headers = self.config.get("headers")
        if self.headers:
            self.location = self.config.get("location")
            self.header_id = self.config.get("header_id")
            self.config["location"] = self.locate_section(root)
            self.config["headers"] = None
        else:
            self.add_links(root)
        return root
