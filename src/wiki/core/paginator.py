from django.core.paginator import Paginator

class WikiPaginator(Paginator):

    def __init__(self, *args, side_pages=4, **kwargs):
        """
        :param side_pages: How many pages should be shown before and after the current page
        """
        self.side_pages = side_pages
        super(WikiPaginator, self).__init__(*args, **kwargs)

    def _get_page(self, *args, **kwargs):
        self.curPage = super(WikiPaginator, self)._get_page(*args, **kwargs)
        return self.curPage

    @property
    def page_range(self):
        left = max(self.curPage.number - self.side_pages, 2)
        right = min(self.curPage.number + self.side_pages+1, self.num_pages)
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
