from markdown.treeprocessors import Treeprocessor


class AnchorTagProcessor(Treeprocessor):
    """
    Custom treeprocessor to process the anchor tags in the HTML tree
    """

    def run(self, root):
        anchor_tags = root.findall('.//a')
        for a_tag in anchor_tags:
            if not self.is_href_valid(a_tag.get('href')):
                a_tag.set('href', '#')

    def is_href_valid(self, value):
        """
        After mark down, validate if the JS is present inside the value of anchor tag.
        """
        return not value.lower().startswith('javascript:')
