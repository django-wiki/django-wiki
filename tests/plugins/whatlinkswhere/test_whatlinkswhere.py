from django.urls import reverse
from wiki.models import URLPath

from ...base import ArticleWebTestUtils
from ...base import DjangoClientTestBase
from ...base import RequireRootArticleMixin


class WhatLinksWhereTests(
    RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase
):
    def test_whatlinkshere(self):
        URLPath.create_urlpath(
            URLPath.root(),
            "page1",
            title="Page 1",
            content="""[page2](page2)[page3](page2)""",
        )
        URLPath.create_urlpath(
            URLPath.root(), "page2", title="Page 2", content="""[page3](page3)"""
        )
        URLPath.create_urlpath(
            URLPath.root(), "page3", title="Page 3", content="""[page1](page1)"""
        )

        url = reverse("wiki:whatlinkswhere", kwargs={"path": ""})
        url.render()
