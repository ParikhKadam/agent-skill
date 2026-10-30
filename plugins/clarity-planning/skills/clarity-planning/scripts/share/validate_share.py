#!/usr/bin/env python3
"""Author-side checks for the generated HTML set.

    python3 validate_share.py <workspace> [--out <dir>]

Prints a report and exits 1 when any check FAILs. Checks: the pages are present and up to date with the markdown, every
document is shown once, every anchor and link resolves, every id is a link, no banned content (paths, tool commands, front
matter, external loads), and the structure (header, footer with date and document count, collapsed details, print and dark CSS).
Authored diagrams that are missing are listed as WARN, not FAIL. Pages with no source documents are N/A.
"""
import os, re, sys, json, collections, tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_share
from build_share import ALL_PAGES, load_authored
from mdparse import load_workspace
from htmlkit import walk_text
import diagrams

NA_WHY = {'story': 'no cases, user flow or glossary', 'system': 'no artifacts, components, system flow, cross-cutting, constraints, facts or existing-system documents',
          'contracts': 'no contract (kind: contract) documents', 'decisions-and-risks': 'no decisions, spikes, questions or risks',
          'build-plan': 'no plan, slice, gates or change-log documents', 'start-here': 'always built'}
DATE_RE = re.compile(r'Generated on \d{4}-\d\d-\d\d')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
        args = [a for a in args if a != out]
    if not args:
        sys.exit(__doc__)
    ws = args[0]
    out = out if '--out' in sys.argv else os.path.join(ws, 'html')
    rep, fail = [], [0]

    def P(s=''):
        rep.append(s)
        print(s)

    def bad(s):
        fail[0] += 1
        P('FAIL: ' + s)

    docs, order = load_workspace(ws)
    try:
        authored, au_note = load_authored(ws)
        with tempfile.TemporaryDirectory() as tmp:
            report = build_share.build(ws, tmp)
            fresh = {p: open(os.path.join(tmp, p + '.html'), encoding='utf-8').read() for p in report['pages'] + ['everything']}
    except build_share.AuthoredError as e:
        P('FAIL: %s' % e)
        P('RESULT: 1 FAILURES')
        sys.exit(1)
    pages = report['pages']
    id_re = re.compile(report['id_pattern'])
    P('== authored data')
    P(au_note or 'html-src/authored.json read')
    for p in ALL_PAGES[:-1]:
        if p not in pages:
            P('N/A: %s.html not built: %s' % (p, NA_WHY[p]))
    if report['missing']:
        P('WARN: authored diagrams not written yet (a placeholder is shown): %s' % ', '.join(report['missing']))
    if report['absent']:
        P('WARN: authored items not written yet (left out): %s' % '; '.join(report['absent']))
    files = {}
    P('== files and freshness')
    for p in pages + ['everything']:
        path = os.path.join(out, p + '.html')
        if not os.path.exists(path):
            bad('%s.html is missing: run wsctl.py html' % p)
            continue
        files[p] = open(path, encoding='utf-8').read()
        if DATE_RE.sub('', files[p]) != DATE_RE.sub('', fresh[p]):
            bad('%s.html is out of date with the markdown or authored data: run wsctl.py html' % p)
    for p in ALL_PAGES[:-1]:
        if p not in pages and os.path.exists(os.path.join(out, p + '.html')):
            bad('%s.html exists but has no source documents any more: run wsctl.py html' % p)
    if not files:
        P('RESULT: %d FAILURES' % fail[0])
        sys.exit(1)
    P('== sizes')
    for p, t in files.items():
        P('%-26s %8.1f KB' % (p + '.html', len(t.encode()) / 1024))
    content = [p for p in pages if p in files]
    P('== document coverage (each md doc has an anchor in exactly one content file)')
    for i in docs:
        homes = [p for p in content if re.search(r'id="%s"' % re.escape(i), files[p])]
        if len(homes) != 1:
            bad('%s found in %s' % (i, homes))
    P('documents checked: %d' % len(docs))
    P('== anchors and links')
    for p, t in files.items():
        ids = re.findall(r'\bid="([^"]+)"', t)
        dup = [k for k, n in collections.Counter(ids).items() if n > 1]
        if dup:
            bad('%s duplicate ids: %s' % (p, dup[:10]))
        idset = set(ids)
        n = 0
        for m in re.finditer(r'href="([^"]*)"', t):
            h = m.group(1)
            n += 1
            if h.startswith('http') or h.startswith('//'):
                bad('%s external link %s' % (p, h))
                continue
            pg, _, fr = h.partition('#')
            if pg and not os.path.exists(os.path.join(out, pg)):
                bad('%s link to missing file %s' % (p, pg))
                continue
            if fr:
                tgt = idset if not pg or pg == p + '.html' else set(re.findall(r'\bid="([^"]+)"', files.get(pg[:-5], '')))
                if fr not in tgt:
                    bad('%s dangling link %s' % (p, h))
        P('%-26s links checked: %d' % (p, n))
    P('== ids mentioned without a link (outside tags, code blocks, titles)')
    SK = {'a', 'pre', 'title', 'desc', 'script', 'style', 'button'}
    for p, t in files.items():
        body = t[t.index('<body'):]
        un = collections.Counter()

        def fn(tok):
            for m in id_re.finditer(tok):
                un[m.group(0)] += 1
            return tok
        walk_text(body, SK, fn)
        if un:
            bad('%s unlinked ids: %s' % (p, dict(un)))
        else:
            P('%-26s all ids linked' % p)
    P('== banned content')
    pats = {'absolute path': r'(/home/|/tmp/|C:\\\\|/Users/)', 'see md': r'\bsee [`\w./-]*\.md\b', 'workspace file name': r'\b(open-questions|implementation-plan|system-flow|user-flow|facts-register|existing-system|cross-cutting|INDEX|sessions|change-log|gates)\.md\b',
            'front matter': r'\n---\nid:', 'wsctl': r'wsctl', 'scratchpad': r'scratchpad', 'read_sets': r'read_sets', 'generated banner': r'(do not edit by hand|Generated by `)',
            'external src': r'<(script|link|img)[^>]+(src|href)=["\']https?:', 'external url': r'https?://', 'plain md link': r'\]\([^)]+\.md\)'}
    for p, t in files.items():
        t = t.replace(diagrams.PLACEHOLDER, '')
        for k, rx in pats.items():
            m = re.findall(rx, t)
            if m:
                bad('%s contains %s (%d) e.g. %s' % (p, k, len(m), m[0]))
    P('== structure')
    for p, t in files.items():
        for need, rx in (('sticky table of contents', r'<header class="top">'), ('footer', r'<footer>.*Generated on \d{4}-\d\d-\d\d from \d+ planning documents'), ('details blocks', r'<details'), ('print css', r'@media print'), ('dark theme', r'prefers-color-scheme:dark')):
            if not re.search(rx, t, re.S):
                if need == 'details blocks':
                    P('note: %s has no collapsed details (nothing long enough to collapse)' % p)
                else:
                    bad('%s missing %s' % (p, need))
        heads = re.findall(r'<h([1-4])[^>]*>(.*?)</h\1>', t, re.S)
        for lvl, h in heads:
            txt = re.sub(r'<[^>]+>', '', h).strip()
            if not txt:
                bad('%s empty heading' % p)
            if id_re.fullmatch(txt):
                bad('%s heading is only an id: %s' % (p, txt))
        if re.search(r'hidden[ >]', t) and 'until-found' not in t:
            P('note: %s has hidden attributes' % p)
        P('%-26s headings %d, details %d, tables %d, pre %d, figures %d' % (p, len(heads), t.count('<details'), t.count('<table'), t.count('<pre'), t.count('<figure')))
    P('== counts: markdown versus output (content pages)')
    md_tables = sum(len(d.tables()) for d in docs.values())
    md_code = sum(len(d.codes()) for d in docs.values())
    out_tables = sum(files[p].count('<table') for p in content)
    out_code = sum(files[p].count('<pre') for p in content)
    P('tables: md %d, output %d (output adds generated tables and drops repeated md tables that are re-rendered)' % (md_tables, out_tables))
    P('code blocks: md %d, output %d' % (md_code, out_code))
    allids = set(m.group(0) for m in id_re.finditer(' '.join(re.sub(r'<[^>]+>', ' ', files[p]) for p in content)))
    mdtext = ' '.join(b[1] if isinstance(b[1], str) else ' '.join(map(str, b[1:])) for d in docs.values() for b in d.blocks)
    mdids = set(m.group(0) for m in id_re.finditer(mdtext))
    P('distinct ids in md text: %d; in output: %d; in md but not output: %s' % (len(mdids), len(allids), sorted(mdids - allids)[:20]))
    P('== glosses used (first use per page)')
    for p, g in report['gloss'].items():
        P('%-26s %s' % (p, ', '.join(g)))
    P('== "the user" rewrites (whitelist): every occurrence changed, 60 characters either side')
    UR = [(re.compile(pt), rp) for pt, rp in authored.get('rewrites', []) if 'user' in pt]
    tot = 0
    remain = {}
    for d in docs.values():
        raw = open(d.path, encoding='utf-8').read().split('\n---\n', 2)[-1]
        units = []
        for ln in raw.split('\n'):
            units.extend([c.strip() for c in ln.split('|')] if ln.lstrip().startswith('|') else [ln])
        for u in units:
            cur = u
            for rx, rp in UR:
                for m in list(rx.finditer(cur)):
                    a_, b_ = max(0, m.start() - 60), min(len(cur), m.end() + 60)
                    P('%s: ...%s[%s -> %s]%s...' % (d.rel, cur[a_:m.start()], m.group(0), rx.sub(rp, m.group(0)), cur[m.end():b_]))
                    tot += 1
                cur = rx.sub(rp, cur)
            remain[d.rel] = remain.get(d.rel, 0) + len(re.findall(r'(?i)\bthe user\b', cur))
    P('changed occurrences: %d' % tot)
    P('remaining plain "the user" per file (left as written, meaning an end user or unclear):')
    for k, v_ in sorted(remain.items()):
        if v_:
            P('  %s: %d' % (k, v_))
    P('== source notes')
    for n in report.get('notes', []):
        P(n)
    P('RESULT: %s' % ('PASS' if not fail[0] else '%d FAILURES' % fail[0]))
    sys.exit(1 if fail[0] else 0)


if __name__ == '__main__':
    main()
