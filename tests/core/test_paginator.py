from django.test import TestCase
from wiki.core.paginator import WikiPaginator


class PaginatorTest(TestCase):
    """
    Test the WikiPaginator and it's page_range() function
    """

    def test_paginator(self):
        objects = [1]
        p = WikiPaginator(objects, 2, side_pages=2)
        self.assertEqual(p.num_pages, 1)

        p.page(1)
        self.assertEqual(p.page_range, [1])

        objects = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        p = WikiPaginator(objects, 2, side_pages=2)
        self.assertEqual(p.num_pages, 5)

        p.page(1)
        self.assertEqual(p.page_range, [1, 2, 3, 0, 5])

        p.page(3)
        self.assertEqual(p.page_range, [1, 2, 3, 4, 5])

        objects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        p = WikiPaginator(objects, 2, side_pages=2)
        self.assertEqual(p.num_pages, 9)

        p.page(1)
        self.assertEqual(p.page_range, [1, 2, 3, 0, 9])

        p.page(5)
        self.assertEqual(p.page_range, [1, 0, 3, 4, 5, 6, 7, 0, 9])

        p.page(8)
        self.assertEqual(p.page_range, [1, 0, 6, 7, 8, 9])
