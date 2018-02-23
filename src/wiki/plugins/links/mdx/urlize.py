import re

import markdown

# Regular expression is meant to match the following pattern:
#
# [BEGIN][PROTOCOL]HOST[:PORT][/[PATH]][END]
#
# Everything except HOST is meant to be optional, as denoted by square
# brackets.
#
# Patter elements are as follows:
#
# BEGIN
#   String preceding the link. Can be empty, or any string that ends
#   in whitespace, '(', or '<'.
#
# PROTOCOL
#   Syntax defined in https://tools.ietf.org/html/rfc3986 - for
#   example: 'http://', 'https://', 'ftp://', or 'ftps://'.
#
# HOST
#   Host can be one of: IPv4 address, IPv6 address in full form, IPv6
#   address in shortened form (e.g. ::1 vs 0:....:0:1 or any
#   combination of), FQDN-like entry (dot-separated domain
#   components), or string 'localhost'.
#
# PORT
#   Port should be a numeric value. Keep in mind that it must be
#   preceded with the colon (':').
#
# PATH
#   Additional PATH, including any GET parameters that should be part
#   of the URL.
#
# END
#   String following the link. Can be empty, or any string that ends
#   in whitespace, ')', or '>'. If ')', then must match with '(' in
#   BEGIN. If '>', then must match with '<' in BEGIN.
#
# It should be noted that there are some inconsitencies with the below
# regex, mainly that:
#
# - No IPv4 or IPv6 address validation is performed.
# - Excessively long IPv6 addresses will end-up being matched if the
#   shortened form happens somewhere in the middle of host string.
#
# In order to make the regex easier to handle later on, the following
# named groups are provided:
#
# - begin (string coming before the link, including whitespace or
#   brackets).
# - url (entire URL that can be used, for example, as actual link for
#   href).
# - protocol (protocol, together with the trailing ://)
# - host (just the host part)
# - port (just the port number)
# - path (path, combined with any additional GET parameters)
# - end (string coming after the link, including whitespace or
#   brackets)
#
URLIZE_RE = (
    # Links must start at beginning of string, or be preceded with
    # whitespace, '(', or '<'.
    r'^(?P<begin>|.*?[\s\(\<])'

    r'(?P<url>'  # begin url group

    # Leading protocol specification.
    r'(?P<protocol>([A-Z][A-Z0-9+.-]*://|))'

    # Host identifier
    r'(?P<host>'  # begin host identifier group

    r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|'  # IPv4, match before FQDN
    r'\[?([A-F0-9]{1,4}:){7}([A-F0-9]{1,4})\]?|'  # IPv6, full form
    r'\[?:(:[A-F0-9]{1,4}){1,6}\]?|'  # IPv6, leading zeros removed
    r'([A-F0-9]{1,4}:){1,6}:([A-F0-9]{1,4}){1,6}|'  # IPv6, zeros in middle removed.
    r'\[?([A-F0-9]{1,4}:){1,6}:\]?|'  # IPv6, trailing zeros removed
    r'\[?::\]?|'  # IPv6, just "empty" address
    r'([A-Z0-9]([A-Z0-9-]{0,61}[A-Z0-9])?\.)+([A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # FQDN
    r'localhost'  # localhost
    r')'  # end host identifier group

    # Optional port
    r'(:(?P<port>[0-9]+))?'

    # Optional trailing slash with path and GET parameters.
    r'(/(?P<path>[^\s\[\(\]\)\<\>]*))?'

    r')'  # end url group

    # Links must stop at end of string, or be followed by a whitespace, ')', or '>'.
    r'(?P<end>[\s\)\>].*?|)$'
)


class UrlizePattern(markdown.inlinepatterns.Pattern):

    def getCompiledRegExp(self):
        """
        Return compiled regular expression for matching the URL
        patterns. We introduce case-insensitive matching in addition
        to standard matching flags added by parent class.
        """

        # Ensure links are matched only if they stand on their own to avoid bad matches etc.
        return re.compile(URLIZE_RE, re.DOTALL | re.UNICODE | re.IGNORECASE)

    def handleMatch(self, m):
        """
        Processes match found within the text.
        """

        protocol = m.group('protocol')

        url = m.group('url')
        text = url

        begin_url = m.group('begin')
        end_url = m.group('end')

        # If opening and ending character for URL are not the same,
        # return text unchanged.
        if begin_url:
            begin_delimeter = begin_url[-1]
        else:
            begin_delimeter = ''
        if end_url:
            end_delimeter = end_url[0]
        else:
            end_delimeter = ''

        if (
                begin_delimeter == '<' and end_delimeter != '>' or
                begin_delimeter == '(' and end_delimeter != ')' or
                end_delimeter == ')' and begin_delimeter != '(' or
                end_delimeter == '>' and begin_delimeter != '<'
        ):
            return url

        # If no supported protocol is specified, assume plaintext http
        # and add it to the url.
        if protocol == '':
            url = 'http://' + url

        # Convenience link to distinguish external links more easily.
        icon = markdown.util.etree.Element("span")
        icon.set('class', 'fa fa-external-link')

        # Link text.
        span_text = markdown.util.etree.Element("span")
        span_text.text = markdown.util.AtomicString(" " + text)

        # Set-up link itself.
        el = markdown.util.etree.Element("a")
        el.set('href', url)
        el.set('target', '_blank')
        el.append(icon)
        el.append(span_text)

        return el


class UrlizeExtension(markdown.Extension):

    """ Urlize Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace autolink with UrlizePattern """
        md.inlinePatterns['autolink'] = UrlizePattern(URLIZE_RE, md)


def makeExtension(configs=None):
    if configs is None:
        configs = {}
    return UrlizeExtension(configs=configs)
