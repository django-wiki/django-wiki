from django.core.paginator import Paginator


class WikiPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        """
        :param side_pages: How many pages should be shown before and after the current page
        """
        self.side_pages = kwargs.pop('side_pages', 4)
        super().__init__(*args, **kwargs)

    def page(self, number):
        # Save last accessed page number for context-based lookup in page_range
        self.last_accessed_page_number = number
        return super().page(number)

    @property
    def page_range(self):
        left = max(self.last_accessed_page_number - self.side_pages, 2)
        right = min(self.last_accessed_page_number + self.side_pages + 1, self.num_pages)
        pages = []
        if self.num_pages > 0:
            pages = [1]
        if left > 2:
            pages += [0]
        pages += range(left, right)
        if right < self.num_pages:
            pages += [0]
        if self.num_pages > 1:
            pages += [self.num_pages]
        return pages
