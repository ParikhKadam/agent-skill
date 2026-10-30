"""Page builders, part 4: decisions and risks, build plan."""
import re
from mdparse import esc, attr, inline, chip, expand_ids
import model, diagrams as D
from htmlkit import *
from pages_a import A, href, ID_ANY, words, qkey
from pages_b import sub


def basis_chip(b):
    return '<span class="chip" data-s="doc" title="basis of the decision">basis: %s</span>' % esc(b) if b else ''


def build_decisions(C):
    R = C.R
    au = C.au
    decs, spikes = C.of_kind('decision'), C.of_kind('spike')
    qd, rd = C.doc('QUESTIONS'), C.doc('RISKS')
    if not (decs or spikes or (qd and C.q) or C.risks):
        return None
    secs, out, cov = [], [], []
    C.count['n_decisions'] = len(decs)
    out.append(C.hero('decisions-and-risks', 'Decisions, questions and risks', ''))
    # decisions
    if decs:
        body = ''
        for d in decs:
            i = d.id
            cov.append(i)
            chips = chip(d.status) + chip(d.fm.get('confidence', '')) + basis_chip(d.fm.get('basis'))
            h = '<article class="card k" id="%s"><h3>%s <span class="meta">%s · v%s</span></h3><p>%s</p>' % (i, R.inl(d.fm.get('title', i)), i, d.version, chips)
            pre = [b for b in d.sections[0][1] if b[0] == 'p']
            note = [b for b in pre if not re.match(r'^Confidence: \w+\. Basis: [\w-]+\.$', b[1])]
            ch = d.sec('Choice') or d.sec('Choices')
            chname = 'Choice' if d.sec('Choice') else 'Choices'
            if ch:
                h += '<h4>%s</h4>' % chname
                tb = [b for b in ch if b[0] == 'table']
                if chname == 'Choices' and tb:
                    h += details('The %d small choices' % len(tb[0][2]), blocks(R, ch, tab=lambda b: dict(chip_cols={2}, first_is_id=False)), open_=True)
                else:
                    h += blocks(R, ch)
            if C.plain(d)[0]:
                h += '<div class="plain"><p>%s</p></div>' % R.inl(C.plain(d)[0])
            rest = ''
            if note:
                rest += '<h4>Status and history</h4>' + blocks(R, note)
            for name in ['Alternatives considered', 'Why this one', 'What would change this', 'What it reopens or affects']:
                bl = d.sec(name)
                if bl:
                    rest += '<h4>%s</h4>' % name + blocks(R, bl, tab=lambda b: dict(first_is_id=False))
            h += details('Alternatives, reasons, what would change this and what it affects', rest)
            h += '</article>'
            body += h
        secs.append(('dr-decisions', C.nav('dr-decisions', 'Decisions')))
        out.append(C.sec('dr-decisions', 'Decisions', '', body))
    # questions
    if qd and C.q:
        cov.append('QUESTIONS')
        at = [b for b in qd.tables() if model.clean(b[1][0]) == 'ID' and len(b[1]) > 1 and model.clean(b[1][1]) == 'Answer']
        ans_t = at[0] if at else None
        ans_rows = [[model.clean(c) for c in r] for r in ans_t[2]] if ans_t else []

        def answers_for(qid):
            hits = []
            for r in ans_rows:
                ids = expand_ids(r[0])
                if re.search(r'\b%s\b' % re.escape(qid), ids) or re.search(r'\bQ-(\d+) to Q-(\d+)\b', ids) and any(int(a) <= int(qid[2:]) <= int(b) for a, b in re.findall(r'Q-(\d+) to Q-(\d+)', ids)):
                    hits.append(r[1] + ' <span class="small">(recorded in %s)</span>' % r[2] if len(r) > 2 else r[1])
            return hits
        qo, qp = C.open_q(), C.part_q()
        qa = [k for k in C.q if k not in qo and k not in qp]

        def qcard(qid):
            q = C.q[qid]
            m = re.match(r'\*\*(.+?)\*\*', q['Question'])
            title = m.group(1) if m else re.split(r'(?<=[a-z\)])\. |\? ', q['Question'])[0]
            if len(title) > 120:
                title = title[:117].rsplit(' ', 1)[0] + '...'
            rest = re.sub(r'^\*\*.+?\*\*\s*', '', q['Question']) if m else q['Question']
            an = answers_for(qid)
            return ('<article class="card" id="%s"><h3>%s <span class="meta">%s</span></h3><p>%s</p><p>%s</p><dl class="kv"><dt>Who can answer</dt><dd>%s</dd><dt>What it blocks</dt><dd>%s</dd><dt>Recommended answer</dt><dd>%s</dd><dt>Needed by layer</dt><dd>%s</dd>%s</dl></article>' % (
                qid, R.inl(title.rstrip('.:')), qid, R.cell(q['Status'], True), R.inl(rest) if not m or rest else '', R.inl(q['Owner']), R.inl(q['Why it matters']), R.inl(q['Recommended answer']), q['Needed by layer'],
                '<dt>Answer recorded</dt><dd>%s</dd>' % '<br>'.join(R.inl(a) if '<span' not in a else R.inl(a.split(' <span')[0]) + ' <span class="small">' + a.split('<span class="small">')[1] for a in an) if an else ''))

        qb = '<div id="QUESTIONS"></div>' + C.plain_html(qd)
        qb += '<h3>Open: %d questions still need an answer</h3>' % len(qo) + ''.join(qcard(k) for k in qo)
        if qp:
            qb += '<h3>Answered in part</h3>' + ''.join(qcard(k) for k in qp)
        hdr = ['ID', 'Question', 'Owner', 'Recommended answer', 'Status', 'Needed by layer', 'Answer recorded']
        arows = []
        for k in sorted(qa, key=qkey):
            q = C.q[k]
            arows.append([k, q['Question'], q['Owner'], q['Recommended answer'], q['Status'], q['Needed by layer'], '<br>'.join(answers_for(k))])
        h = ''.join('<th>%s</th>' % x for x in hdr)
        trs = ''
        for r in arows:
            trs += '<tr id="%s"><td class="idc">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                r[0], r[0], R.inl(r[1]), R.inl(r[2]), R.inl(r[3]), R.cell(r[4], True) + (' ' + chip('draft', 'final answer differs from the question as first asked') if C.is_superseded(r[0]) else ''), r[5], R.inl(re.sub(r'<br>', '\n', re.sub(r' <span class="small">\(recorded in ([^<]*)\)</span>', r' (recorded in \1)', r[6]))))
        if qa:
            qb += details('Answered: %d questions (%d plainly, %d where the final answer differs from the question as first asked)' % (len(qa), len([k for k in qa if not C.is_superseded(k)]), len([k for k in qa if C.is_superseded(k)])), '<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (h, trs))
        if ans_t:
            qb += details(C.T('answers_recorded_title', 'Answers as recorded'), table(R, ans_t[1], ans_t[2], first_is_id=False))
        if C.qfixed:
            C.notes.append('QUESTIONS: row %s had an escaped pipe inside a cell, so one column was missing in the source; the cell was split at the pipe.' % ', '.join(sorted(set(C.qfixed))))
        qb += '<p class="small">Questions %s · QUESTIONS · v%s</p>' % (chip(qd.status), qd.version)
        secs.append(('dr-questions', C.nav('dr-questions', 'Questions')))
        out.append(C.sec('dr-questions', '{n_open} questions are open; the rest are answered', '', qb))
    # risks
    if rd and C.risks:
        cov.append('RISKS')
        rt = rd.tables()[0]
        rids = {r['id'] for r in C.risks}
        hd = [model.clean(x) for x in rt[1]]
        cols = {hd.index('Status')} if 'Status' in hd else set()
        top = max(r['score'] for r in C.risks)
        C.count['n_top_score'] = len([r for r in C.risks if r['score'] == top])
        C.count['top_score'] = top
        C.count['n_risks'] = len(C.risks)
        rb = '<div id="RISKS"></div>' + C.plain_html(rd) + D.diag_L(C.risks, au.get('risk_short', {}), au.get('diagram_text')) + '<h3>All %s risks</h3>' % words(len(C.risks)) + table(R, rt[1], rt[2], anchor_ids=rids, chip_cols=cols)
        rb += '<p class="small">Risks %s · RISKS · v%s</p>' % (chip(rd.status), rd.version)
        secs.append(('dr-risks', C.nav('dr-risks', 'Risks')))
        out.append(C.sec('dr-risks', '{n_risks} assumptions could break the design; {n_top_score} of them score the top {top_score}', '', rb))
    # spikes
    if spikes:
        sb = ''
        for d in spikes:
            i = d.id
            cov.append(i)
            pre = d.sections[0][1]
            inner = ''
            for name in ['Why it matters', 'Method and data', 'Result', 'What we do now']:
                inner += sub(R, d, name)
            for n in [n for n in d.sec_names() if n.startswith('Correction')]:
                inner += '<h4>%s</h4>' % esc(n) + blocks(R, d.sec(n))
            sb += ('<article class="card" id="%s"><h3>%s <span class="meta">%s · v%s</span></h3><p>%s</p>%s%s%s%s</article>' % (
                i, R.inl(d.fm.get('title', i)), i, d.version, chip(d.status), blocks(R, pre), sub(R, d, 'The question'),
                sub(R, d, 'The bar, set before we look', tab=lambda b: dict(first_is_id=False)),
                details('Why it matters, method, result and what we do now', inner) if inner else ''))
        secs.append(('dr-spikes', C.nav('dr-spikes', 'Spikes')))
        out.append(C.sec('dr-spikes', 'Spikes', '', sb))
    return secs, ''.join(out), cov, []


# =====================================================================================================
def build_plan(C):
    R = C.R
    au = C.au
    pl, ga, cl_ = C.doc('PLAN'), C.doc('GATES'), C.doc('CHANGELOG')
    sdocs = C.of_kind('slice')
    if not (pl or ga or cl_ or sdocs):
        return None
    secs, out, cov = [], [], []
    C.count['n_slices'] = len(C.slices)
    out.append(C.hero('build-plan', 'Build plan', '', ' id="PLAN"' if pl else ''))
    if pl:
        cov.append('PLAN')
        special = ('In plain words', 'Slices', 'Deferred', 'Test strategy', 'Rollout', 'How a change is handled')
        pb = C.plain_html(pl, rest=False)
        for name in pl.sec_names():
            if not name.startswith(special) and pl.sec(name):
                pb += '<h3>%s</h3>' % esc(name) + blocks(R, pl.sec(name))
        pb += '<p class="small">Plan %s · PLAN · v%s</p>' % (chip(pl.status), pl.version)
        secs.append(('bp-plan', C.nav('bp-plan', 'The plan')))
        out.append(C.sec('bp-plan', 'The plan', '', pb))
        # timeline
        if C.slices:
            conds = ''
            if au.get('timeline_conditions'):
                conds = '<h3>Conditions on the timeline</h3><ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in au['timeline_conditions'])
            secs.append(('bp-timeline', C.nav('bp-timeline', 'Timeline')))
            out.append(C.sec('bp-timeline', 'Timeline', '', D.diag_G(C.slices, C.ptitles, C.tracks, au.get('join_slice_prefix', ''), C.T('timeline_freeze'), au.get('diagram_text')) + conds))
        # phases
        sname = next((n for n in pl.sec_names() if n.startswith('Slices')), None)
        if sname and C.slices:
            ph = ''
            tr = {t[0]: t for t in C.tracks}
            for b in pl.sec(sname):
                if b[0] == 'h':
                    ph += '<h3>%s</h3>' % R.inl(b[2])
                elif b[0] == 'table':
                    head = [model.clean(x) for x in b[1]]
                    anchor_ids = {model.clean(r[0]) for r in b[2] if model.clean(r[0]) not in C.slice_docs}

                    def exit_cell(c, r):
                        return details('Exit check', R.inl(model.clean(c)))

                    def track_cell(c, r):
                        t = model.clean(c)
                        cls = tr[t][2][1:] if t in tr else None
                        return '<span class="chip track" style="background:var(--%s)">%s</span>' % (cls, t) if cls else '<span class="chip" data-s="doc">%s</span>' % esc(t)
                    ch = {}
                    for ix, hname in enumerate(head):
                        if hname.startswith('Exit check'):
                            ch[ix] = exit_cell
                        elif hname == 'Track':
                            ch[ix] = track_cell
                    ph += table(R, b[1], b[2], anchor_ids=anchor_ids, cell_html=ch)
                elif b[0] == 'p':
                    ph += '<p>%s</p>' % R.inl(b[1])
            secs.append(('bp-phases', C.nav('bp-phases', 'Phases and slices')))
            out.append(C.sec('bp-phases', 'Slices', '', ph))
    # slice documents
    ret = ''.join('<div class="card" id="%s"><h3>Retired slice <span class="meta">%s</span></h3><p>%s</p></div>' % (k, k, esc(v)) for k, v in au.get('retired', {}).items())
    if sdocs or ret:
        sb = ''
        track_of = {s['id']: s for s in C.slices}
        tr = {t[0]: t for t in C.tracks}
        for d in sdocs:
            i = d.id
            cov.append(i)
            s = track_of.get(i, {})
            t = s.get('track', '')
            cl = 'cb-' + tr[t][2][1:] if t in tr else 'k'
            h = '<article class="card %s" id="%s"><h3>%s <span class="meta">%s · v%s</span></h3><p>%s %s</p><p>%s</p>' % (
                cl, i, R.inl(d.fm.get('title', i)), i, d.version, chip(d.status), '<span class="chip" data-s="doc">track: %s</span>' % esc(t) if t else '', R.inl(d.fm.get('summary', '')))
            if s:
                h += '<dl class="kv"><dt>Owner (plan table)</dt><dd>%s</dd><dt>Rests on</dt><dd>%s</dd><dt>Flag or rollback (plan table)</dt><dd>%s</dd></dl>' % (R.inl(s.get('owner', '')), R.inl(s.get('rests', '')), R.inl(s.get('flag', '')))
            pre = d.sections[0][1]
            if pre:
                h += blocks(R, pre)
            if C.plain(d)[0]:
                h += '<div class="plain"><p>%s</p></div>' % R.inl(C.plain(d)[0])
            if d.sec('Proves'):
                h += '<h4>What it proves</h4>' + blocks(R, d.sec('Proves'))
            h += sub(R, d, 'Exit check', title='Exit check (written before the work)')
            rest = ''
            for n in d.sec_names():
                if n in ('In plain words', 'Proves', 'Exit check'):
                    continue
                rest += '<h4>%s</h4>' % esc(n) + blocks(R, d.sec(n))
            if rest:
                h += details('Inputs, deliverables, flag or rollback and notes', rest)
            h += '</article>'
            sb += h
        secs.append(('bp-slices', C.nav('bp-slices', 'Slice documents')))
        out.append(C.sec('bp-slices', 'Slice documents', '', sb + ret))
    # deferred, tests, rollout, change
    if pl:
        dname = next((n for n in pl.sec_names() if n.startswith('Deferred')), None)
        dt = [b for b in pl.sec(dname) if b[0] == 'table'] if dname else []
        if dt:
            C.count['n_def'] = len(dt[0][2])
        db = table(R, dt[0][1], dt[0][2], first_is_id=False) if dt else ''
        if pl.sec('Test strategy'):
            db += '<h3>Test strategy</h3>' + details(C.T('test_strategy_title', 'Test strategy'), blocks(R, pl.sec('Test strategy')))
        if pl.sec('Rollout'):
            db += '<h3>Rollout</h3>' + details(C.T('rollout_title', 'Rollout'), blocks(R, pl.sec('Rollout')))
        if pl.sec('How a change is handled'):
            db += '<h3>How a change is handled</h3>' + blocks(R, pl.sec('How a change is handled'))
        if db:
            secs.append(('bp-deferred', C.nav('bp-deferred', 'Deferred, tests, rollout, change')))
            out.append(C.sec('bp-deferred', 'Deferred, tests, rollout, change', '', db))
    # gates
    if ga and C.gates:
        li = ''
        for g in C.gates:
            st = g['Status']
            cls = {'passed': '', 'passed-with-conditions': 'cond', 'not-started': 'todo'}.get(st, 'todo')
            notes = ''
            if g['Notes']:
                notes = '<ul>%s</ul>' % ''.join('<li>%s</li>' % R.inl(p) for p in model.split_sentences_notes(g['Notes']))
            li += '<li class="%s"><strong>Layer %s: %s</strong> %s%s<br><span class="small">Evidence: %s</span>%s</li>' % (
                cls, g['Layer'], esc(g['Name']), chip(st), '', R.inl(g['Evidence']) if g['Evidence'] else 'none yet', notes)
        gb = '<div id="GATES"></div>' + C.plain_html(ga) + '<ul class="check">%s</ul>' % li
        gb += '<p class="small">Gates %s · GATES · v%s. A ticked box means passed, a half box passed with conditions, an empty box not started.</p>' % (chip(ga.status), ga.version)
        secs.append(('bp-gates', C.nav('bp-gates', 'Gate conditions')))
        out.append(C.sec('bp-gates', 'Gate conditions', '', gb))
    # change log
    ct = cl_.tables()[0] if cl_ and cl_.tables() else None
    if ct:
        C.count['n_log'] = len(ct[2])
        head = [model.clean(h) for h in ct[1]]
        oi = head.index('Outcome') if 'Outcome' in head else len(head) - 1
        hdr = ['Date', 'What changed and why', 'Outcome']
        rows = []
        for r in ct[2]:
            rows.append([model.clean(r[0]), model.clean(r[1]) if len(r) > 1 else '', model.clean(r[oi]) if len(r) > oi and oi > 1 else ''])
        lb = '<div id="CHANGELOG"></div>' + C.plain_html(cl_) + table(R, hdr, rows, first_is_id=False)
        lb += '<p class="small">Change log %s · CHANGELOG · v%s</p>' % (chip(cl_.status), cl_.version)
        secs.append(('bp-log', C.nav('bp-log', 'Change log')))
        out.append(C.sec('bp-log', 'Change log', '', lb))
    # documents covered, in a fixed reading order: plan, slices, change log, gates
    cov = [x for x in ['PLAN'] if pl] + [d.id for d in sdocs] + (['CHANGELOG'] if ct else []) + (['GATES'] if ga and C.gates else [])
    return secs, ''.join(out), cov, []
