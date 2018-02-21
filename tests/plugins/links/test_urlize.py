import html
import markdown
from unittest import mock

import pytest

from wiki.plugins.links.mdx.urlize import makeExtension, UrlizeExtension


# Template accepts two strings - href value and link text value.
EXPECTED_LINK_TEMPLATE = (
    '<a href="%s" target="_blank">'
    '<span class="fa fa-external-link">'
    '</span>'
    '<span>'
    ' %s'
    '</span>'
    '</a>'
)

# Template accepts two strings - href value and link text value.
EXPECTED_PARAGRAPH_TEMPLATE = '<p>%s</p>' % EXPECTED_LINK_TEMPLATE


FIXTURE_POSITIVE_MATCHES = [
    # Test surrounding begin/end characters.
    (
        '(example.com)',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com', 'example.com')
    ),
    (
        '<example.com>',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com', 'example.com')
    ),

    # Test protocol specification.
    (
        'http://example.com',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com', 'http://example.com')
    ),
    (
        'https://example.com',
        EXPECTED_PARAGRAPH_TEMPLATE % ('https://example.com', 'https://example.com')
    ),
    (
        'ftp://example.com',
        EXPECTED_PARAGRAPH_TEMPLATE % ('ftp://example.com', 'ftp://example.com')
    ),
    (
        'ftps://example.com',
        EXPECTED_PARAGRAPH_TEMPLATE % ('ftps://example.com', 'ftps://example.com')
    ),
    (
        'example.com',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com', 'example.com')
    ),

    # Test various supported host variations.
    (
        '10.10.1.1',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://10.10.1.1', '10.10.1.1')
    ),
    (
        '1122:3344:5566:7788:9900:aabb:ccdd:eeff',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://1122:3344:5566:7788:9900:aabb:ccdd:eeff', '1122:3344:5566:7788:9900:aabb:ccdd:eeff')
    ),
    (
        '1122:3344:5566:7788:9900:AaBb:cCdD:EeFf',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://1122:3344:5566:7788:9900:AaBb:cCdD:EeFf', '1122:3344:5566:7788:9900:AaBb:cCdD:EeFf')
    ),
    (
        '::1',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://::1', '::1')
    ),
    (
        '1::2:3',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://1::2:3', '1::2:3')
    ),
    (
        '1::',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://1::', '1::')
    ),
    (
        '::',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://::', '::')
    ),
    (
        'example.com',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com', 'example.com')
    ),
    (
        'my.long.domain.example.com',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://my.long.domain.example.com', 'my.long.domain.example.com')
    ),
    (
        'localhost',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://localhost', 'localhost')
    ),

    # Test port section.
    (
        'localhost:8000',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://localhost:8000', 'localhost:8000')
    ),
    (
        '10.1.1.1:8000',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://10.1.1.1:8000', '10.1.1.1:8000')
    ),

    # Test trailing path specification.
    (
        'http://example.com/',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com/', 'http://example.com/')
    ),
    (
        'http://example.com/my/path',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com/my/path', 'http://example.com/my/path')
    ),
    (
        'http://example.com/my/path?param1=value1&param2=value2',
        EXPECTED_PARAGRAPH_TEMPLATE % ('http://example.com/my/path?param1=value1&amp;param2=value2', 'http://example.com/my/path?param1=value1&amp;param2=value2')
    ),

    # Link positioned somewhere within the text, but around whitespace boundary.
    (
        'This is link myhost.example.com',
        "<p>This is link " + EXPECTED_LINK_TEMPLATE % ('http://myhost.example.com', 'myhost.example.com') + "</p>"
    ),
    (
        'myhost.example.com is the link',
        "<p>" + EXPECTED_LINK_TEMPLATE % ('http://myhost.example.com', 'myhost.example.com') + " is the link</p>"
    ),
    (
        'I have best myhost.example.com link ever',
        "<p>I have best " + EXPECTED_LINK_TEMPLATE % ('http://myhost.example.com', 'myhost.example.com') + " link ever</p>"
    ),
    (
        'I have best\nmyhost.example.com link ever',
        "<p>I have best\n" + EXPECTED_LINK_TEMPLATE % ('http://myhost.example.com', 'myhost.example.com') + " link ever</p>"
    ),
]


FIXTURE_NEGATIVE_MATCHES = [
    # Incomplete FQDNs.
    (
        'example.',
        '<p>example.</p>'
    ),
    (
        '.example .com',
        '<p>.example .com</p>'
    ),

    # Invalid FQDNs.
    (
        'example-.com',
        '<p>example-.com</p>'
    ),
    (
        '-example.com',
        '<p>-example.com</p>'
    ),
    (
        'my.-example.com',
        '<p>my.-example.com</p>'
    ),
]


class TestUrlizeExtension:

    def setup_method(self):
        self.md = markdown.Markdown(extensions=[UrlizeExtension()])

    @pytest.mark.parametrize("markdown_text, expected_output", FIXTURE_POSITIVE_MATCHES)
    def test_positive_matches(self, markdown_text, expected_output):
        assert self.md.convert(markdown_text) == expected_output

    @pytest.mark.parametrize("markdown_text, expected_output", FIXTURE_NEGATIVE_MATCHES)
    def test_negative_matches(self, markdown_text, expected_output):
        assert self.md.convert(markdown_text) == expected_output

    def test_url_with_non_matching_begin_and_end_ignored(self):
        assert self.md.convert('(example.com>') == "<p>%s</p>" % html.escape('(example.com>')
        assert self.md.convert('<example.com)') == "<p>%s</p>" % html.escape('<example.com)')


def test_makeExtension_return_value():
    extension = makeExtension()

    assert isinstance(extension, UrlizeExtension)


@mock.patch('wiki.plugins.links.mdx.urlize.UrlizeExtension')
def test_makeExtension_initialises_using_passed_in_configuration(mock_UrlizeExtension):
    my_config = mock.Mock()
    makeExtension(my_config)

    mock_UrlizeExtension.assert_called_once_with(configs=my_config)
