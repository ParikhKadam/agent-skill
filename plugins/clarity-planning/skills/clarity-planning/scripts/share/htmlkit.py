"""HTML helpers: tables, cards, details, link and gloss passes."""
import re
from mdparse import esc, attr, inline, cell_status, chip, STATUS_WORDS, expand_ids, PIPE
import model

SKIP_LINK = {'a', 'pre', 'script', 'style', 'title', 'desc', 'button', 'textarea', 'option'}
SKIP_GLOSS = {'a', 'pre', 'svg', 'script', 'style', 'summary', 'h1', 'h2', 'h3', 'h4', 'abbr', 'code', 'button', 'i', 'title', 'th', 'dt', 'textarea', 'figcaption'}
TAG_RE = re.compile(r'(<[^>]+>)')
NAME_RE = re.compile(r'^<(/?)([a-zA-Z0-9]+)')


def walk_text(html, skip, fn):
    out = []
    depth = {}
    total = 0
    for tok in TAG_RE.split(html):
        if tok.startswith('<') and tok.endswith('>'):
            m = NAME_RE.match(tok)
            if m:
                name = m.group(2).lower()
                if name in skip and not tok.endswith('/>'):
                    if m.group(1):
                        if depth.get(name, 0) > 0:
                            depth[name] -= 1
                            total -= 1
                    else:
                        depth[name] = depth.get(name, 0) + 1
                        total += 1
            out.append(tok)
        else:
            out.append(tok if total > 0 or not tok else fn(tok))
    return ''.join(out)


DOC_FILE_IDS = {'open-questions': 'QUESTIONS', 'implementation-plan': 'PLAN', 'system-flow': 'FLOW-SYSTEM', 'user-flow': 'FLOW-USER',
                'facts-register': 'FACTS', 'existing-system': 'EXISTING', 'cross-cutting': 'CROSSCUT', 'change-log': 'CHANGELOG',
                'gates': 'GATES', 'brief': 'BRIEF', 'glossary': 'GLOSSARY'}
# Applied after the workspace's own rewrites: references that only make sense next to the markdown files or the workspace tool.
DEFAULT_REWRITES = [
    (r"`wsctl\.py [^`]*`", 'the workspace tool'),
    (r"`?(?:\d\d-[a-z-]+/)?(?:[a-z-]+/)?(%s)\.md`?" % '|'.join(DOC_FILE_IDS), lambda m: DOC_FILE_IDS[m.group(1)]),
]


class Rules:
    def __init__(self, rewrites):
        self.rw = [(re.compile(p), r) for p, r in list(rewrites) + DEFAULT_REWRITES]

    def prep(self, s):
        for p, r in self.rw:
            s = p.sub(r, s)
        return expand_ids(s)

    def inl(self, s):
        return inline(self.prep(s))

    def cell(self, s, status=False):
        s = self.prep(s)
        return cell_status(s) if status else inline(s)


def chips_html(*items):
    out = []
    for it in items:
        if not it:
            continue
        if isinstance(it, tuple):
            out.append(chip(it[0], it[1]))
        else:
            out.append(chip(it))
    return ''.join(out)


def details(summary, body, open_=False, cls='', sid=None):
    return '<details%s%s%s><summary>%s</summary><div class="dbody">%s</div></details>' % (
        ' open' if open_ else '', ' class="%s"' % cls if cls else '', ' id="%s"' % sid if sid else '', summary, body)


def table(R, head, rows, anchor_ids=None, chip_cols=(), cls='', id_col=True, cell_html=None, first_is_id=True):
    rows, _ = model.fix_rows(head, rows)
    h = ''.join('<th>%s</th>' % R.inl(x) for x in head)
    body = []
    for r in rows:
        key = model.clean(r[0])
        aid = ' id="%s"' % attr(key) if (anchor_ids is not None and key in anchor_ids) else ''
        tds = []
        for i, c in enumerate(r):
            if cell_html and (i in cell_html):
                tds.append('<td>%s</td>' % cell_html[i](c, r))
                continue
            klass = ' class="idc"' if i == 0 and first_is_id and re.match(r'^[A-Z]+(-[A-Za-z0-9]+)+$', model.clean(c)) else ''
            tds.append('<td%s>%s</td>' % (klass, R.cell(model.clean(c), status=(i in chip_cols))))
        body.append('<tr%s>%s</tr>' % (aid, ''.join(tds)))
    return '<div class="tw"><table%s><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (' class="%s"' % cls if cls else '', h, ''.join(body))


def blocks(R, bl, tab=None, skip_plain=False):
    """Render generic markdown blocks. tab(block) -> kwargs for table()."""
    out = []
    for b in bl:
        k = b[0]
        if k == 'p':
            out.append('<p>%s</p>' % R.inl(b[1]))
        elif k == 'ul':
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % R.inl(i) for i in b[1]))
        elif k == 'ol':
            out.append('<ol>%s</ol>' % ''.join('<li>%s</li>' % R.inl(i) for i in b[1]))
        elif k == 'table':
            kw = tab(b) if tab else {}
            out.append(table(R, b[1], b[2], **kw))
        elif k == 'code':
            out.append(code_block(b[2], b[1]))
        elif k == 'h':
            out.append('<h%d>%s</h%d>' % (min(b[1] + 1, 5), R.inl(b[2]), min(b[1] + 1, 5)))
    return ''.join(out)


def code_block(text, lang=''):
    return '<pre><code>%s</code></pre>' % esc(text)


def meta(doc):
    return '<span class="meta">%s · v%s</span>' % (doc.id, doc.version)
