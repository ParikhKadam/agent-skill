"""Generic markdown + front matter parsing for planning workspaces (standard library only)."""
import os, re, html

STATUS_WORDS = ["passed-with-conditions", "not-started", "in-progress", "agreed", "passed", "pending", "draft",
                "decided", "hypothesis", "measured", "doc", "inferred", "unknown", "invented", "answered",
                "open", "deferred", "accepted", "mitigated", "skipped", "dropped"]
EV_TITLES = {"M": "measured: checked live or by reading the code", "D": "documented: written in a document",
             "I": "inferred: a reasoned guess", "T": "needs a test: not yet checked by a test"}
PIPE = "\u241f"
# Set by the builder from the workspace's authored data (see references/share-pages.md).
CONFIG = {"src_prefixes": [], "guess_title": "starting guess"}


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def parse_front(text):
    m = re.match(r'^---\n(.*?)\n---\n?', text, re.S)
    fm = {}
    body = text
    if m:
        body = text[m.end():]
        for line in m.group(1).split('\n'):
            if ':' in line and not line.startswith(' '):
                k, v = line.split(':', 1)
                v = v.strip()
                if v.startswith('[') and v.endswith(']'):
                    v = [x.strip() for x in v[1:-1].split(',') if x.strip()]
                else:
                    v = v.strip('"\'')
                fm[k.strip()] = v
    return fm, body


def split_row(line):
    line = line.strip().replace('\\|', PIPE)
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip() for c in line.split('|')]


def is_sep(line):
    return bool(re.match(r'^\s*\|?\s*:?-{2,}', line)) and set(line.strip()) <= set('|:- ')


def parse_blocks(lines):
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        l = lines[i]
        if not l.strip():
            i += 1
            continue
        if l.startswith('```'):
            lang = l[3:].strip()
            j = i + 1
            buf = []
            while j < n and not lines[j].startswith('```'):
                buf.append(lines[j])
                j += 1
            blocks.append(('code', lang, '\n'.join(buf)))
            i = j + 1
            continue
        m = re.match(r'^(#{1,6})\s+(.*)', l)
        if m:
            blocks.append(('h', len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if l.lstrip().startswith('|'):
            tl = []
            while i < n and lines[i].lstrip().startswith('|'):
                tl.append(lines[i])
                i += 1
            if len(tl) >= 2 and is_sep(tl[1]):
                head = split_row(tl[0])
                rows = [split_row(x) for x in tl[2:]]
                blocks.append(('table', head, rows))
            else:
                rows = [split_row(x) for x in tl]
                if blocks and blocks[-1][0] == 'table':
                    blocks[-1][2].extend(rows)
                else:
                    blocks.append(('table', rows[0], rows[1:]))
            continue
        if re.match(r'^\s*[-*]\s+', l):
            items = []
            while i < n and (re.match(r'^\s*[-*]\s+', lines[i]) or (items and lines[i].startswith('  ') and lines[i].strip())):
                if re.match(r'^\s*[-*]\s+', lines[i]):
                    items.append(re.sub(r'^\s*[-*]\s+', '', lines[i]))
                else:
                    items[-1] += '\n' + lines[i].strip()
                i += 1
            blocks.append(('ul', items))
            continue
        if re.match(r'^\s*\d+\.\s+', l):
            items = []
            while i < n and (re.match(r'^\s*\d+\.\s+', lines[i]) or (items and lines[i].startswith('  ') and lines[i].strip())
                             or (items and not lines[i].strip() and i + 1 < n and re.match(r'^\s*\d+\.\s+', lines[i + 1]))):
                if re.match(r'^\s*\d+\.\s+', lines[i]):
                    items.append(re.sub(r'^\s*\d+\.\s+', '', lines[i]))
                elif lines[i].strip():
                    items[-1] += '\n' + lines[i].strip()
                i += 1
            blocks.append(('ol', items))
            continue
        buf = [l.strip()]
        i += 1
        while i < n and lines[i].strip() and not re.match(r'^(#{1,6}\s|```|\s*\||\s*[-*]\s+|\s*\d+\.\s+)', lines[i]):
            buf.append(lines[i].strip())
            i += 1
        blocks.append(('p', ' '.join(buf)))
    return blocks


class Doc:
    def __init__(self, path, root):
        self.path = path
        self.rel = os.path.relpath(path, root)
        text = open(path, encoding='utf-8').read()
        self.fm, body = parse_front(text)
        self.id = self.fm.get('id') or os.path.splitext(os.path.basename(path))[0]
        self.version = self.fm.get('version', '')
        self.status = self.fm.get('status', '')
        self.blocks = parse_blocks(body.split('\n'))
        self.title = ''
        self.sections = []  # (heading, blocks); first has heading None
        cur = (None, [])
        self.sections.append(cur)
        for b in self.blocks:
            if b[0] == 'h' and b[1] == 1 and not self.title:
                self.title = b[2]
                continue
            if b[0] == 'h' and b[1] == 2:
                cur = (b[2], [])
                self.sections.append(cur)
                continue
            cur[1].append(b)
        if not self.title:
            self.title = self.fm.get('title', self.id)

    def sec(self, name, prefix=False):
        for h, bl in self.sections:
            if h is None:
                continue
            if h == name or (prefix and h.startswith(name)) or h.lower() == name.lower():
                return bl
        return []

    def sec_names(self):
        return [h for h, _ in self.sections if h]

    def plain(self):
        for b in self.sec('In plain words'):
            if b[0] == 'p':
                return b[1]
        return ''

    def tables(self):
        return [b for b in self.blocks if b[0] == 'table']

    def codes(self):
        return [b for b in self.blocks if b[0] == 'code']


def load_workspace(root):
    docs = {}
    order = []
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d not in ('html', 'html-src') and not d.startswith('.'))
        for f in sorted(fn):
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root)
            if rel == 'INDEX.md' or rel.endswith('90-log/sessions.md') or rel.endswith('90-log\\sessions.md'):
                continue
            d = Doc(p, root)
            docs[d.id] = d
            order.append(d.id)
    return docs, order


# ---------- inline rendering -------------
def chip(status, text=None, extra=''):
    t = text or status
    return '<span class="chip" data-s="%s"%s>%s</span>' % (attr(status), extra, esc(t))


def ev_chip(k):
    return '<span class="ev" data-ev="%s" title="%s">%s</span>' % (k, attr(EV_TITLES[k]), k)


def inline(s, rules=None):
    s = s.replace(PIPE, '|')
    if rules:
        for pat, rep in rules:
            s = re.sub(pat, rep, s)
    s = esc(s)
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return '\x00%d\x00' % (len(codes) - 1)
    s = re.sub(r'`([^`]+)`', keep, s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'\[(M|D|I|T)\]', lambda m: ev_chip(m.group(1)), s)
    if CONFIG["src_prefixes"]:
        s = re.sub(r'\[((?:%s)[^\]]*)\]' % '|'.join(re.escape(x) for x in CONFIG["src_prefixes"]), r'<span class="src">[\1]</span>', s)
    s = re.sub(r'\(h\)', '<span class="chip chip-h" data-s="hypothesis" title="%s">(h) guess</span>' % attr(CONFIG["guess_title"]), s)
    s = re.sub(r'\x00(\d+)\x00', lambda m: '<code>' + codes[int(m.group(1))] + '</code>', s)
    s = s.replace('\n', '<br>')
    return s


def cell_status(raw, rules=None):
    raw = raw.replace(PIPE, '|').strip()
    m = re.match(r'^(' + '|'.join(STATUS_WORDS) + r')\b(.*)$', raw, re.S)
    if m:
        rest = m.group(2).strip()
        return chip(m.group(1)) + (' ' + inline(rest, rules) if rest else '')
    return inline(raw, rules)


def expand_ids(s):
    """Write id lists and ranges out in full so every id is a whole id that can be linked."""
    s = re.sub(r'\b([A-Z]+)-(\d+)\.\.(\d+)\b', lambda m: '%s-%s to %s-%s' % (m.group(1), m.group(2), m.group(1), m.group(3)), s)
    s = re.sub(r'\b([A-Z]+-\d+)\.\.([A-Z]+-\d+)\b', r'\1 to \2', s)

    def lst(m):
        txt = m.group(0)
        return txt[:6] + re.sub(r'(, | and )(\d\d)\b', lambda n: n.group(1) + 'ART-' + n.group(2), txt[6:])
    s = re.sub(r'\b(ART)-\d\d(?:(?:, | and )\d\d\b)+', lst, s)
    return s
