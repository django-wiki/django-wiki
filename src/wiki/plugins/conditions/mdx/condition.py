import markdown
import re

class ConditionExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('dw-conditions', ConditionPreprocessor(md), '>html_block')


COND_RE = re.compile(
    r'(?P<prefix>.*?)\[\s*if\s+(?P<cond>(group|user))\s+in\s+(?P<args>\w+((,|\s)+\w+)?)\s*\](?P<suffix>.*)$',
    re.IGNORECASE
)

CONDEND_RE = re.compile(r'(?P<prefix>.*?)\[\s*endif\s*\](?P<suffix>.*)$', re.IGNORECASE)

class ConditionPreprocessor(markdown.preprocessors.Preprocessor):

    def run(self, lines):
        block = dict(prev=None, cond=True, out=list())

        for line in lines:
            while True:
                m = CONDEND_RE.match(line)
                if m and block['prev']:
                    block['out'].append(m.group('prefix'))

                    if block['cond']:
                        block['prev']['out'].extend(block['out'])

                    block = block['prev']
                    line = m.group('suffix')
                    continue

                m = COND_RE.match(line)
                if m:
                    block['out'].append(m.group('prefix'))

                    args = m.group('args').replace(",", " ").split()

                    if self.markdown.user is None:
                        cond = False
                    elif m.group('cond') == 'group':
                        cond = self.markdown.user.groups.filter(name__in=args).exists()
                    elif m.group('cond') == 'user':
                        cond = self.markdown.user.username in args
                    else:
                        cond = False

                    block = dict(prev=block, cond=cond, out=list())

                    line = m.group('suffix')
                    continue

                block['out'].append(line)
                break

        while block['prev']:
            if block['cond']:
                block['prev']['out'].extend(block['out'])
            block = block['prev']

        return block['out']
