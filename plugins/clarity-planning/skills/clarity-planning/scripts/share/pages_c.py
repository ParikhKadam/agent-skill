"""Page builders, part 3: contracts."""
import re, json
from mdparse import esc, attr, inline, chip, expand_ids
import model, diagrams as D
from htmlkit import *
from pages_a import A, href, ID_ANY, words


def json_objects(text):
    dec = json.JSONDecoder()
    for cand in (text, '{' + text + '}'):
        try:
            return [json.loads(cand)]
        except Exception:
            pass
    objs, i, n = [], 0, len(text)
    while i < n:
        while i < n and text[i] in ' \n\t,':
            i += 1
        if i >= n:
            break
        try:
            o, j = dec.raw_decode(text, i)
            objs.append(o)
            i = j
        except Exception:
            nxt = text.find('\n', i)
            if nxt < 0:
                break
            i = nxt + 1
    return objs


def flatten(o, path='', out=None):
    out = out if out is not None else {}

    def add(p, t, ex):
        e = out.setdefault(p, [set(), None])
        e[0].add(t)
        if e[1] is None and ex is not None:
            e[1] = ex
    if isinstance(o, dict):
        for k, v in o.items():
            p = (path + '.' if path else '') + k
            if isinstance(v, (dict, list)):
                add(p, 'object' if isinstance(v, dict) else 'array', None)
                flatten(v, p, out)
            else:
                add(p, 'null' if v is None else type(v).__name__.replace('str', 'string').replace('int', 'number').replace('float', 'number').replace('bool', 'boolean'), v)
    elif isinstance(o, list):
        for v in o:
            if isinstance(v, (dict, list)):
                flatten(v, path + '[]', out)
            else:
                add(path + '[]', type(v).__name__.replace('str', 'string'), v)
    return out


def field_table(R, text, required, conditional):
    objs = json_objects(text)
    if not objs:
        return ''
    fl = {}
    for o in objs:
        flatten(o, '', fl)
    rows = []
    for p, (types, ex) in fl.items():
        t = ' or '.join(sorted(types))
        exs = '' if ex is None else json.dumps(ex)
        if len(exs) > 56:
            exs = exs[:53] + '...'
        note = ''
        if p in required:
            note = 'required'
        elif p in conditional:
            note = conditional[p]
        rows.append('<tr><td><code>%s</code></td><td>%s</td><td>%s</td><td>%s</td></tr>' % (esc(p), t, '<code>%s</code>' % esc(exs) if exs else '', esc(note)))
    return '<div class="tw"><table><thead><tr><th>Field</th><th>Type</th><th>Example value</th><th>Required</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(rows)


def req_sets(doc, cfg):
    """Required fields from the Rules bullet that starts '**Required:**'. Authored per-contract config (contracts.fields):
    required_until = a name in backticks after which fields are conditional; conditional = {path: note}; ignore = names that are not fields."""
    req, cond = set(), dict(cfg.get('conditional', {}))
    ignore = set(cfg.get('ignore', ['started', 'succeeded', 'failed']))
    for b in doc.sec('Rules'):
        if b[0] == 'ul':
            for it in b[1]:
                if it.startswith('**Required:**'):
                    head = it.split('**Per part:**')[0]
                    cut = head.find('`%s`' % cfg['required_until']) if cfg.get('required_until') else -1
                    for t in re.findall(r'`([^`]+)`', head):
                        pos = head.find('`%s`' % t)
                        if cut >= 0 and pos >= cut:
                            continue
                        if t not in ignore:
                            req.add(t)
    return req, cond


def ver_rows(R, first):
    out = ''
    for x in first.split(';'):
        x = x.strip()
        m = re.match(r'^(.*?)\s*(`[^`]+`|\d+)$', x)
        if m:
            lab, val = m.group(1), m.group(2)
        else:
            m = re.search(r'(`[^`]+`)', x)
            lab, val = ('API version' if 'API version' in x else x), (m.group(1) if m else '')
        out += '<tr><td>%s</td><td>%s</td></tr>' % (esc(lab[:1].upper() + lab[1:]), R.inl(val))
    return out


def build_contracts(C):
    R = C.R
    au = C.au
    cau = au.get('contracts', {})
    ks = C.of_kind('contract')
    if not ks:
        return None
    secs, out = [], []
    out.append(C.hero('contracts', 'Contracts', ''))
    # overview
    rows = ''
    for d in ks:
        rows += '<tr><td class="idc">%s</td><td>%s</td><td>%s%s</td><td>v%s</td></tr>' % (
            d.id, R.inl(d.fm.get('summary', '')), chip(d.status), '<span class="chip" data-s="pending">owner review pending</span>' if d.fm.get('owner_review') == 'pending' else '', d.version)
    ov = '<div class="tw"><table><thead><tr><th>Contract</th><th>What it carries</th><th>Status</th><th>Version</th></tr></thead><tbody>%s</tbody></table></div>' % rows
    if C.T('contracts_overview_note'):
        ov += '<p>%s</p>' % esc(C.T('contracts_overview_note'))
    secs.append(('ct-overview', C.nav('ct-overview', 'The contracts')))
    out.append(C.sec('ct-overview', 'The contracts', '', ov))
    cards = ''
    extra_secs = cau.get('extra_example_sections', [])
    for d in ks:
        k = d.id
        req, cond = req_sets(d, cau.get('fields', {}).get(k, {}))
        wire = cau.get('wire', {}).get(k)
        h = ('<article class="card k" id="%s"><h3>%s <span class="meta">%s · v%s</span></h3><p>%s%s</p><p>%s</p>' % (
            k, R.inl(d.fm.get('title', k)), k, d.version, chip(d.status),
            '<span class="chip" data-s="pending">owner review pending</span>' if d.fm.get('owner_review') == 'pending' else '', R.inl(d.fm.get('summary', ''))))
        if C.plain(d)[0]:
            h += '<div class="plain"><p>%s</p></div>' % R.inl(C.plain(d)[0])
        if d.sec('Parties and owners'):
            h += '<h4>Parties and owners</h4>%s' % blocks(R, d.sec('Parties and owners'))
        if wire:
            h += '<h4>On the wire</h4><dl class="kv">%s</dl>' % ''.join('<dt>%s</dt><dd>%s</dd>' % (a, b) for a, b in wire)
        pre = [b for b in d.sections[0][1] if not (b[0] == 'p' and b[1].startswith('**Versions:**'))]
        vp = [b[1] for b in d.sections[0][1] if b[0] == 'p' and b[1].startswith('**Versions:**')]
        if vp:
            txt = vp[0][len('**Versions:**'):].strip()
            first, _, note = txt.partition('. ')
            rows_v = ver_rows(R, first)
            h += '<h4>Versions</h4><div class="tw"><table><thead><tr><th>Kind</th><th>Value</th></tr></thead><tbody>%s</tbody></table></div><p class="small">%s</p>' % (rows_v, R.inl(note))
        if pre:
            h += details('Status note and review history', blocks(R, pre))
        if d.sec('All calls in one table'):
            h += '<h4>All calls in one table</h4>' + blocks(R, d.sec('All calls in one table'), tab=lambda b: dict(first_is_id=False))
        # examples
        for sec_name in d.sec_names():
            extra = [e for e in extra_secs if sec_name.startswith(e['prefix'])]
            if sec_name.startswith('Example') or extra:
                inner = ''
                for b in d.sec(sec_name):
                    if b[0] == 'code':
                        inner += '<div><button class="copy" data-act="copy">Copy</button><pre><code>%s</code></pre></div>' % esc(b[2])
                        if b[1] == 'json':
                            ft = field_table(R, b[2], req, cond)
                            if ft:
                                inner += details('Field table derived from this example', ft)
                    else:
                        inner += blocks(R, [b])
                label = sec_name
                chipx = ''
                if extra:
                    label = extra[0].get('label', sec_name)
                    if extra[0].get('chip'):
                        chipx = chip(*extra[0]['chip']) + ' '
                h += details('%s%s' % (chipx, esc(label)), inner, cls='ex')
        if d.sec('Rules'):
            h += '<h4>Rules</h4>' + details('Rules: required fields, idempotency, versioning, what is never sent', blocks(R, d.sec('Rules')), open_=True)
        chn = sorted([n for n in d.sec_names() if n.startswith('Changes in')], key=lambda n: -int(re.search(r'v(\d+)', n).group(1)) if re.search(r'v(\d+)', n) else 0)
        ch = ''.join('<h4>%s</h4>%s' % (n, blocks(R, d.sec(n))) for n in chn)
        if ch:
            h += details('What changed between versions (newest first)', ch)
        if d.sec('Stub'):
            h += details('Stub: how to build against it alone', blocks(R, d.sec('Stub')), open_=False)
        h += '</article>'
        cards += h
    secs.append(('ct-contracts', C.nav('ct-contracts', 'The contracts in full')))
    for d in ks:
        secs.append((d.id, d.fm.get('title', d.id)))
    out.append(C.sec('ct-contracts', 'The contracts in full', '', cards))
    # vocabulary: authored rows plus the code table of the contract that holds one
    V = cau.get('vocabulary', [])
    cr = ''
    codes = None
    src = C.doc(cau.get('codes_from', '')) if cau.get('codes_from') else None
    for d in ([src] if src else ks):
        found = [b for b in d.sec('Rules') if b[0] == 'table'] or [b for b in d.tables() if model.clean(b[1][0]) == 'Code']
        if found:
            codes = found[0]
            break
    if codes:
        for r in model.fix_rows(codes[1], codes[2])[0]:
            cr += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ('%s code' % model.clean(r[1]), R.inl(model.clean(r[0])), R.inl(model.clean(r[3])) + ' <span class="small">(set by %s)</span>' % esc(model.clean(r[2])), cau.get('codes_used_in', ''))
    if V or cr:
        vt = ''
        last = None
        for g, v, m, u in V:
            vt += '<tr><td>%s</td><td><code>%s</code></td><td>%s</td><td>%s</td></tr>' % (esc(g) if g != last else '', esc(v), R.inl(m), u)
            last = g
        vocab = ('<div class="tw"><table><thead><tr><th>Group</th><th>Value</th><th>Meaning</th><th>Used in</th></tr></thead><tbody>%s%s</tbody></table></div>' % (vt, cr) +
                 ('<p class="small">%s</p>' % cau['vocabulary_note'] if cau.get('vocabulary_note') else ''))
        secs.append(('ct-vocab', C.nav('ct-vocab', 'Shared vocabulary')))
        out.append(C.sec('ct-vocab', 'Shared vocabulary', '', vocab))
    if cau.get('keys_html'):
        secs.append(('ct-keys', C.nav('ct-keys', 'Keys and recipes')))
        out.append(C.sec('ct-keys', 'Keys and recipes', '', cau['keys_html']))
    if cau.get('inputs_html'):
        secs.append(('ct-inputs', C.nav('ct-inputs', 'Inputs per part')))
        out.append(C.sec('ct-inputs', 'Inputs per part', '', cau['inputs_html']))
    return secs, ''.join(out), [d.id for d in ks], []
