import re
import os

FIELD_RE = re.compile(
    r'\s*((?P<article>[-a-z0-9_./]+)/)?(?P<field>\w+?)\s*$'
)

def parse_input(article, val):
    m = FIELD_RE.match(val)
    if not m:
        return None

    path = article.get_absolute_url()
    if m.group('article'):
        path = os.path.normpath(os.path.join(path, m.group('article')))

    return path.strip('/') + '/', m.group('field')
