"""Extract structured facts from the parsed documents (generic: tables and labelled bullets)."""
import re
from mdparse import expand_ids, PIPE

ID_RE = re.compile(r'^[A-Z]+(?:-[A-Za-z0-9]+)+$')


def clean(c):
    return c.replace(PIPE, '|').strip()


def table_by_header(doc, first_header):
    for b in doc.tables():
        if b[1] and clean(b[1][0]).lower() == first_header.lower():
            return b
    return None


def fix_rows(head, rows):
    """Repair rows that lost a cell because of an escaped pipe in the source (reported by the validator)."""
    out = []
    fixed = []
    n = len(head)
    for r in rows:
        r = list(r)
        if len(r) < n:
            for i, c in enumerate(r):
                if PIPE in c:
                    a, b = c.split(PIPE, 1)
                    r[i:i + 1] = [a.strip(), b.strip()]
                    fixed.append(r[0])
                    break
        while len(r) < n:
            r.append('')
        if len(r) > n:
            extra = [x for x in r[n:] if x.strip()]
            if extra:
                fixed.append('extra cells in row ' + r[0])
            r = r[:n]
        out.append(r)
    return out, fixed


def art_list(s):
    ids = set()
    for m in re.finditer(r'ART-(\d\d)\.\.(\d\d)', s):
        for n in range(int(m.group(1)), int(m.group(2)) + 1):
            ids.add('ART-%02d' % n)
    s = expand_ids(s)
    ids |= set(re.findall(r'ART-\d\d', s))
    return sorted(ids)


def components(docs, owner_tracks=None):
    """Component cards (kind: component). owner_tracks maps a lower-case owner prefix to a track letter."""
    out = []
    owner_tracks = owner_tracks or {}
    for d in docs.values():
        if d.fm.get('kind') != 'component':
            continue
        reads = writes = ''
        for b in d.sec('Inputs and output'):
            if b[0] == 'ul':
                for it in b[1]:
                    if it.startswith('Reads'):
                        reads = it
                    elif it.startswith('Writes'):
                        writes = it
        own = ''
        card_status = ''
        for b in d.blocks:
            if b[0] == 'p' and 'Status of this card' in b[1]:
                m = re.search(r'Status of this card: \*\*(\w+)\*\*', b[1])
                card_status = m.group(1) if m else ''
                m = re.match(r'Owner: ([^.]+)\.', b[1])
                own = m.group(1) if m else ''
                break
        side = ''
        for pref, tr in owner_tracks.items():
            if own.lower().startswith(pref.lower()):
                side = tr
                break
        out.append(dict(id=d.id, title=d.fm.get('title', d.id), owner=own, card_status=card_status,
                        reads=art_list(reads), writes=art_list(writes), reads_raw=reads, writes_raw=writes, side=side))
    return out


def _col(rec, *names):
    for n in names:
        if n in rec:
            return rec[n]
    return ''


def plan_slices(plan):
    """Slice rows of the plan: every table whose columns include ID and Slice. Phase and track are optional."""
    out = []
    if plan is None:
        return out
    phase = None
    ptitle = ''
    phased = any(b[0] == 'h' and b[1] == 3 and re.match(r'Phase (\d+): ', b[2]) for b in plan.blocks)
    for b in plan.blocks:
        if b[0] == 'h' and b[1] == 3:
            m = re.match(r'Phase (\d+): (.*)', b[2])
            if m:
                phase, ptitle = int(m.group(1)), m.group(2)
            else:
                phase = None
        if b[0] == 'table':
            head = [clean(h) for h in b[1]]
            if head[:1] != ['ID'] or 'Slice' not in head or (phased and phase is None):
                continue
            rows, _ = fix_rows(b[1], b[2])
            for r in rows:
                rec = dict(zip(head, [clean(x) for x in r]))
                out.append(dict(id=rec['ID'], track=rec.get('Track', ''), title=rec['Slice'],
                                exit=_col(rec, 'Exit check (written before the work)', 'Exit check'),
                                flag=rec.get('Flag or rollback', ''), owner=rec.get('Owner', ''), rests=rec.get('Rests on', ''),
                                phase=phase if phased else 1, phase_title=ptitle if phased else ''))
    return out


def phase_titles(plan):
    out = {}
    if plan is None:
        return out
    for b in plan.blocks:
        if b[0] == 'h' and b[1] == 3:
            m = re.match(r'Phase (\d+): (.*)', b[2])
            if m:
                out[int(m.group(1))] = m.group(2)
    return out


def _int(x, default=0):
    try:
        return int(re.match(r'\s*(\d+)', x).group(1))
    except Exception:
        return default


def risks(doc):
    t = table_by_header(doc, 'ID') if doc else None
    if not t:
        return []
    head = [clean(h) for h in t[1]]
    rows, _ = fix_rows(t[1], t[2])
    out = []
    for r in rows:
        rec = dict(zip(head, [clean(x) for x in r]))
        text = _col(rec, 'Assumption that could break the design', 'Assumption', 'Risk')
        plan = rec.get('Plan', '')
        imp, unc = _int(rec.get('Impact', '')), _int(rec.get('Uncertainty', ''))
        out.append(dict(id=rec['ID'], text=text, impact=imp, unc=unc, score=_int(rec.get('Score', ''), imp * unc), plan=plan,
                        status=rec.get('Status', ''), spikes=sorted(set(re.findall(r'S-\d{3}', plan + ' ' + text)))))
    return out


def gates(doc):
    t = table_by_header(doc, 'Layer') if doc else None
    if not t:
        return []
    head = [clean(h) for h in t[1]]
    out = []
    for r in fix_rows(t[1], t[2])[0]:
        rec = dict(zip(head, [clean(x) for x in r]))
        for k in ('Name', 'Status', 'Evidence', 'Notes'):
            rec.setdefault(k, '')
        out.append(rec)
    return out


def perm_matrix(doc):
    t = table_by_header(doc, 'Actor') if doc else None
    if not t:
        return None
    head = [clean(h) for h in t[1]]
    return head, [[clean(x) for x in r] for r in fix_rows(t[1], t[2])[0]]


def questions(doc):
    t = table_by_header(doc, 'ID') if doc else None
    if not t:
        return [], [], []
    head = [clean(h) for h in t[1]]
    rows, fixed = fix_rows(t[1], t[2])
    return head, rows, fixed


def split_sentences_notes(s):
    parts = []
    for seg in re.split(r';\s+', s):
        parts.extend(re.split(r'(?<=[a-z0-9\)])\.\s+(?=[A-Z])', seg))
    return [p.strip().rstrip('.') for p in parts if p.strip()]
