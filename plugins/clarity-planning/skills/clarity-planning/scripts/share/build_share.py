#!/usr/bin/env python3
"""Build the shareable HTML set from a planning workspace.

    python3 build_share.py <workspace> [--out <dir>]

Reads the markdown files (never edits them) and writes start-here.html, story.html, system.html, contracts.html,
decisions-and-risks.html, build-plan.html and everything.html into <workspace>/html (or --out). A page with no source
documents is left out. Authored data (diagram data, glosses, short titles, one-line summaries) is read from
<workspace>/html-src/authored.json; without it everything that can be generated from the markdown tables is still built.
See references/share-pages.md.
"""
import os, re, sys, json, datetime

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mdparse
from mdparse import load_workspace, esc
import style
from htmlkit import walk_text, SKIP_LINK, SKIP_GLOSS
from pages_a import Ctx, PAGES, build_start, words
from pages_b import build_story, build_system
from pages_c import build_contracts
from pages_d import build_decisions, build_plan

BUILDERS = {'start-here': build_start, 'story': build_story, 'system': build_system, 'contracts': build_contracts,
            'decisions-and-risks': build_decisions, 'build-plan': build_plan}
TITLES = {'start-here': 'Start here', 'story': 'Story: cases and user flow', 'system': 'System: parts, flows and rules', 'contracts': 'Contracts',
          'decisions-and-risks': 'Decisions and risks', 'build-plan': 'Build plan'}
ALL_PAGES = [p for p, _ in PAGES] + ['everything']
ID_MEANING = [('D', 'decision'), ('Q', 'question'), ('R', 'risk'), ('F', 'fact'), ('X', 'constraint'), ('S', 'spike'), ('K', 'contract'),
              ('C', 'component'), ('ART', 'stored result'), ('SL', 'slice'), ('CASE', 'example case')]


class AuthoredError(Exception):
    pass


def load_authored(ws):
    """<workspace>/html-src/authored.json: data only, never code. Returns ({}, note) when there is none."""
    p = os.path.join(ws, 'html-src', 'authored.json')
    if not os.path.exists(p):
        return {}, 'no html-src/authored.json: pages are built from the markdown tables only; authored diagrams show a placeholder'
    try:
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
    except ValueError as e:
        raise AuthoredError('html-src/authored.json is not valid JSON: %s' % e)
    if not isinstance(data, dict):
        raise AuthoredError('html-src/authored.json must hold one JSON object')
    return data, ''


def make_id_regex(reg_keys, doc_ids):
    """One pattern for every id the workspace defines (documents, table rows, slices, rules). Only defined ids are matched, so codes that
    merely look like ids (a supplier code S-208) stay plain text. Also returns the id prefixes (for the default id key)."""
    prefixes, exact = set(), set()
    for k in reg_keys:
        m = re.fullmatch(r'([A-Z]+)-[A-Z]?\d+', k)
        if m:
            prefixes.add(m.group(1))
        if k in doc_ids or re.fullmatch(r'[A-Z]+(?:-[A-Za-z0-9]+)+', k):
            exact.add(k)
    alts = [re.escape(x) for x in sorted(exact, key=lambda x: (-len(x), x))]
    return r'\b(?:%s)\b' % '|'.join(alts) if alts else r'(?!x)x', sorted(prefixes)


class Linker:
    def __init__(self, reg, page, combined, id_re, anchors):
        self.reg, self.page, self.combined, self.id_re, self.anchors = reg, page, combined, id_re, anchors
        self.unresolved = {}

    def target(self, i):
        if i not in self.reg:
            return None
        pg, anc = self.reg[i]
        if self.combined or pg == self.page:
            return '#' + anc
        return '%s.html#%s' % (pg, anc)

    def sub(self, text):
        def f(m):
            i = m.group(0)
            t = self.target(i)
            if not t:
                self.unresolved[i] = self.unresolved.get(i, 0) + 1
                return i
            return '<a class="id" href="%s">%s</a>' % (t, i)
        return self.id_re.sub(f, text)

    def run(self, html):
        return walk_text(html, SKIP_LINK, self.sub)

    def hrefs(self, html):
        """Resolve the page links the builders wrote; a link to a page or section that does not exist becomes plain text."""
        def f(m):
            page, tok, label = m.group(1), m.group(2), m.group(3)
            if page not in self.anchors or tok not in self.anchors[page]:
                return label
            if self.combined or page == self.page:
                return '<a href="#%s">%s</a>' % (tok, label)
            return '<a href="%s.html#%s">%s</a>' % (page, tok, label)
        return re.sub(r'<a href="@@href:([a-z\-]+):([A-Za-z0-9_\-]+)@@">(.*?)</a>', f, html)


def add_gloss(html, glosses, seen_log):
    done = set()
    for key, pat, text, src in glosses:
        rx = re.compile(pat, re.I)

        def fn(tok, rx=rx, key=key, text=text):
            if key in done:
                return tok
            m = rx.search(tok)
            if not m:
                return tok
            done.add(key)
            seen_log.append(key)
            return tok[:m.end()] + '<i class="gloss"> (%s)</i>' % esc(text) + tok[m.end():]
        html = walk_text(html, SKIP_GLOSS, fn)
    return html


def chrome(brand, pages, page, title, secs, body, combined, footer='', idkey=''):
    nav = ''.join('<a class="pg%s" href="%s.html">%s</a>' % (' on' if p == page else '', p, t) for p, t in pages)
    nav += '<a class="pg%s" href="everything.html">Everything</a>' % (' on' if page == 'everything' else '')
    if combined:
        sec = ''.join('<a class="sec" href="#part-%s">%s</a>' % (p, t) for p, t in pages) + '<a class="sec" href="#contents">Contents</a>'
        nav = ''.join('<a class="pg" href="%s.html">%s</a>' % (p, t) for p, t in pages) + '<a class="pg on" href="everything.html">Everything</a>'
    else:
        sec = ''.join('<a class="sec" href="#%s">%s</a>' % (i, esc(t)) for i, t in secs)
    tools = '<span class="sp"></span><button class="tool" data-act="expand">Expand all</button><button class="tool" data-act="collapse">Collapse all</button><button class="tool" data-act="theme">Light or dark</button>'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s | %s</title>'
            '<style>%s</style></head><body><header class="top"><div class="r1"><span class="brand">%s</span>%s%s</div><div class="r2">%s</div><div class="r3">Id key: %s</div></header>'
            '<main>%s</main>%s<script>%s</script></body></html>') % (esc(title), esc(brand), style.css(), esc(brand), nav, tools, sec, esc(idkey), body, footer, style.JS)


def footer_html(date, docs, ids, extra, combined_note=''):
    items = ', '.join('%s v%s' % (i, docs[i].version) for i in ids)
    ex = ''
    if extra:
        ex = '<p>This page also summarises: %s.</p>' % ', '.join(extra)
    return ('<footer><p>Generated on %s from %d planning documents.%s</p><details><summary>Documents covered, with their versions</summary><div class="dbody"><p>%s</p>%s</div></details></footer>'
            % (date, len(ids), combined_note, items, ex))


def build(ws, outdir, today=None):
    """Write the page set into outdir. Returns a report dict (pages, sizes, unresolved ids, missing authored items, notes, glosses)."""
    os.makedirs(outdir, exist_ok=True)
    docs, order = load_workspace(ws)
    authored, au_note = load_authored(ws)
    mdparse.CONFIG['src_prefixes'] = list(authored.get('source_tag_prefixes', []))
    mdparse.CONFIG['guess_title'] = authored.get('guess_title', 'starting guess')
    C = Ctx(docs, order, authored)
    date = today or datetime.date.today().isoformat()
    brand = authored.get('brand') or (docs['BRIEF'].title if 'BRIEF' in docs else '') or os.path.basename(os.path.abspath(ws)).replace('-', ' ')
    # pass 1: which pages have a source, and the counts the section texts use
    active = []
    for p, t in PAGES:
        if BUILDERS[p](C) is not None:
            active.append((p, t))
    C.count.setdefault('n_open', 0)
    C.notes, C.missing, C.absent = [], [], []
    built = {}
    for p, _ in active:
        built[p] = BUILDERS[p](C)
    notes = list(C.notes)
    # an id links only where its anchor exists in the page that should hold it
    anchors = {p: set(re.findall(r'\bid="([^"]+)"', built[p][1])) for p, _ in active}
    anchors_all = set().union(*anchors.values()) if anchors else set()
    reg = {i: v for i, v in C.reg.items() if v[0] in anchors and v[1] in anchors[v[0]]}
    pat, prefixes = make_id_regex(C.reg.keys(), set(docs))
    id_re = re.compile(pat)
    comp_docs = any(k.startswith('C-') for k in docs)
    idkey = authored.get('id_key') or ' · '.join('%s %s' % kv for kv in ID_MEANING if kv[0] in prefixes or (kv[0] == 'C' and comp_docs))
    glosses = authored.get('glosses', [])
    report = {'pages': [p for p, _ in active], 'unresolved': {}, 'gloss': {}, 'sizes': {}, 'notes': notes, 'missing': sorted(set(C.missing)),
              'absent': sorted(set(C.absent)), 'authored_note': au_note, 'has_authored': bool(authored), 'id_pattern': pat}
    if au_note:
        report['notes'].append(au_note)
    cov_all = []
    for p, t in active:
        secs, body, cov, extra = built[p]
        cov_all += cov
        lk = Linker(reg, p, False, id_re, anchors)
        seen = []
        h = add_gloss(body, glosses, seen)
        h = lk.run(h)
        h = lk.hrefs(h)
        foot = lk.run(footer_html(date, docs, cov, extra))
        page = chrome(brand, active, p, TITLES[p], secs, h, False, footer=foot, idkey=idkey)
        with open(os.path.join(outdir, p + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        report['unresolved'][p] = lk.unresolved
        report['gloss'][p] = seen
        report['sizes'][p] = len(page.encode('utf-8'))
    # everything
    parts, toc = [], []
    for p, t in active:
        secs, body, cov, extra = built[p]
        parts.append('<div class="part" id="part-%s">%s</div>' % (p, body))
        toc.append('<li><span class="pt"><a href="#part-%s">%s</a></span><ul>%s</ul></li>' % (p, t, ''.join('<li><a href="#%s">%s</a></li>' % (i, esc(tt)) for i, tt in secs)))
    n = words(len(active))
    tochtml = ('<section class="sec" id="contents"><h2>Contents of all %s pages</h2><p class="sowhat">One page with everything, for searching and printing. The %s pages are also available one by one.</p><ul class="toc">%s</ul></section>'
               % (n, n, ''.join(toc)))
    anchors_every = {p: anchors_all for p in ALL_PAGES}
    lk = Linker(reg, 'everything', True, id_re, anchors_every)
    seen = []
    h = add_gloss(tochtml + ''.join(parts), glosses, seen)
    h = lk.run(h)
    h = lk.hrefs(h)
    foot = lk.run(footer_html(date, docs, cov_all, [], ' All %s pages are included, in reading order.' % n))
    page = chrome(brand, active, 'everything', 'Everything on one page', [], h, True, footer=foot, idkey=idkey)
    with open(os.path.join(outdir, 'everything.html'), 'w', encoding='utf-8') as f:
        f.write(page)
    report['unresolved']['everything'] = lk.unresolved
    report['gloss']['everything'] = seen
    report['sizes']['everything'] = len(page.encode('utf-8'))
    # a page that is no longer generated must not linger
    for p in ALL_PAGES:
        if p not in report['pages'] and p != 'everything':
            stale = os.path.join(outdir, p + '.html')
            if os.path.exists(stale):
                os.remove(stale)
    return report


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
        args = [a for a in args if a != out]
    ws = args[0] if args else sys.exit(__doc__)
    outdir = out if '--out' in sys.argv else os.path.join(ws, 'html')
    try:
        report = build(ws, outdir)
    except AuthoredError as e:
        sys.exit('error: %s' % e)
    for k, v in report['sizes'].items():
        print('%-24s %8d bytes' % (k + '.html', v))
    unres = {i: n for p in report['unresolved'] for i, n in report['unresolved'][p].items()}
    print('unresolved ids:', unres or 'none')
    if report['missing']:
        print('authored diagrams not written yet (placeholders shown):', ', '.join(report['missing']))
    if report['absent']:
        print('authored items not written yet (left out):', '; '.join(report['absent']))
    if report['authored_note']:
        print('note:', report['authored_note'])


if __name__ == '__main__':
    main()
