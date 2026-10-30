"""Page builders, part 1: shared context and the start-here page.

Every builder returns None when the workspace has nothing for that page, or (sections, body html, documents covered, extra notes).
Text that is specific to one workspace (headings, one-line summaries, glosses, diagrams) comes from html-src/authored.json;
each builder has a plain default for when that data is missing."""
import re
from mdparse import esc, attr, inline, chip, expand_ids
import model, diagrams as D
from htmlkit import *

PAGES = [('start-here', 'Start here'), ('story', 'Story'), ('system', 'System'), ('contracts', 'Contracts'),
         ('decisions-and-risks', 'Decisions and risks'), ('build-plan', 'Build plan')]
KIND_HOME = {'brief': 'start-here', 'case': 'story', 'glossary': 'story', 'world': 'system', 'fact': 'system', 'decision': 'decisions-and-risks',
             'risk': 'decisions-and-risks', 'question': 'decisions-and-risks', 'spike': 'decisions-and-risks', 'flow': 'system', 'artifact': 'system',
             'component': 'system', 'crosscut': 'system', 'contract': 'contracts', 'plan': 'build-plan', 'slice': 'build-plan', 'log': 'build-plan', 'gates': 'build-plan'}
# Conventional ids (workspace-structure.md) that read as story rather than system.
DEFAULT_HOME = {'FLOW-USER': 'story', 'GLOSSARY': 'story'}
ID_ANY = re.compile(r'^[A-Z]+(-[A-Za-z0-9]+)+$')
NUM = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
       'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']


def words(n):
    return NUM[n] if 0 <= n < len(NUM) else str(n)


def href(page, token):
    return '@@href:%s:%s@@' % (page, token)


def A(page, token, label):
    return '<a href="%s">%s</a>' % (href(page, token), label)


def fill(text, counts):
    return re.sub(r'\{(\w+)\}', lambda m: str(counts[m.group(1)]) if m.group(1) in counts else m.group(0), text)


class Ctx:
    def __init__(self, docs, order, authored):
        self.docs, self.order, self.au = docs, order, authored
        self.R = Rules([tuple(x) for x in authored.get('rewrites', [])])
        self.home = {}
        hov = dict(DEFAULT_HOME)
        hov.update(authored.get('home_override', {}))
        for i, d in docs.items():
            self.home[i] = hov.get(i) or KIND_HOME.get(d.fm.get('kind'), 'build-plan')
        # tracks: [letter, label, svg class]
        tr = authored.get('tracks')
        self.tracks = [list(t) for t in tr] if tr else []
        if not tr:
            letters = []
            for sl in model.plan_slices(docs.get('PLAN')):
                if re.fullmatch(r'[A-Z]', sl['track']) and sl['track'] not in letters:
                    letters.append(sl['track'])
            self.tracks = [[l, l, ['nb', 'nl', 'nf'][i % 3]] for i, l in enumerate(letters)]
        D.TRACK_CLASS.clear()
        D.TRACK_CLASS.update({t[0]: t[2] for t in self.tracks})
        self.comps = model.components(docs, authored.get('owner_tracks', {}))
        self.slices = model.plan_slices(docs.get('PLAN'))
        self.ptitles = model.phase_titles(docs.get('PLAN'))
        self.risks = model.risks(docs.get('RISKS'))
        self.gates = model.gates(docs.get('GATES'))
        self.qhead, self.qrows, self.qfixed = model.questions(docs.get('QUESTIONS'))
        self.q = {model.clean(r[0]): dict(zip(self.qhead, [model.clean(x) for x in r])) for r in self.qrows}
        for q in self.q.values():
            for k in ('Question', 'Recommended answer', 'Status', 'Owner', 'Why it matters', 'Needed by layer'):
                q.setdefault(k, '')
        self.reg = {}   # id -> (page, anchor)
        self.notes = []  # gaps / disagreements found while building
        self.missing = []  # authored diagrams with no data
        self.absent = []   # other authored content with no data
        self.count = {}
        self.slice_docs = {i for i, d in self.docs.items() if d.fm.get('kind') == 'slice'}
        self.art_titles = {}
        ar = docs.get('ARTIFACTS')
        if ar and ar.tables():
            for r in model.fix_rows(ar.tables()[0][1], ar.tables()[0][2])[0]:
                self.art_titles[model.clean(r[0])] = model.clean(r[1]).split(' (')[0]
        self._register()

    # ---- helpers
    def doc(self, i):
        return self.docs.get(i)

    def of_kind(self, kind, prefix=None):
        ds = [d for d in self.docs.values() if d.fm.get('kind') == kind and (prefix is None or d.id.startswith(prefix))]
        order = self.au.get('order', {}).get(kind)
        if order:
            ds.sort(key=lambda d: order.index(d.id) if d.id in order else len(order))
        else:
            ds.sort(key=lambda d: d.id)
        return ds

    def T(self, key, default=''):
        t = self.au.get('texts', {}).get(key, default)
        return fill(t, self.count)

    def nav(self, sid, default):
        return self.au.get('nav', {}).get(sid, default)

    def title(self, sid, default):
        return fill(self.au.get('titles', {}).get(sid, default), self.count)

    def hero(self, page, default_h1, default_lede='', extra_attrs=''):
        h = self.au.get('heroes', {}).get(page, {})
        h1 = fill(h.get('h1', default_h1), self.count)
        lede = fill(h.get('lede', default_lede), self.count)
        return '<div class="hero"%s><h1>%s</h1>%s</div>' % (extra_attrs, esc(h1), '<p class="lede">%s</p>' % esc(lede) if lede else '')

    def diagram(self, key, label, authored_key, fn):
        """An authored diagram: drawn when its data exists, a visible placeholder when not."""
        spec = self.au.get('diagrams', {}).get(authored_key)
        if not spec:
            self.missing.append(label)
            return D.placeholder(key, label)
        return fn(spec)

    # ---- registry of anchors
    def put(self, i, page, anchor=None):
        self.reg.setdefault(i, (page, anchor or i))

    def _register(self):
        for i, d in self.docs.items():
            self.put(i, self.home[i])
        for q in self.q:
            self.put(q, 'decisions-and-risks')
        for r in self.risks:
            self.put(r['id'], 'decisions-and-risks')
        for sl in self.slices:
            self.put(sl['id'], 'build-plan')
        for did in ('FACTS', 'CONSTRAINTS', 'ARTIFACTS'):
            d = self.docs.get(did)
            if d:
                for t in d.tables():
                    for r in model.fix_rows(t[1], t[2])[0]:
                        self.put(model.clean(r[0]), 'system')
        ar = self.docs.get('ARTIFACTS')
        if ar:
            for b in ar.blocks:
                if b[0] == 'ol':
                    for it in b[1]:
                        m = re.match(r'\*\*(H-\d+) ', it)
                        if m:
                            self.put(m.group(1), 'system')
        for i in self.au.get('retired', {}):
            self.put(i, 'build-plan')

    def plain(self, doc):
        ps = [b[1] for b in doc.sec('In plain words') if b[0] == 'p']
        return (ps[0] if ps else ''), ps[1:]

    def plain_html(self, doc, rest=True):
        first, more = self.plain(doc)
        if not first:
            return ''
        h = '<div class="plain"><p>%s</p></div>' % self.R.inl(first)
        if rest and more:
            h += ''.join('<p>%s</p>' % self.R.inl(p) for p in more)
        return h

    def section(self, sid, title, so, body, doc_ids=()):
        so = fill(so, self.count) if so else ''
        return ('<section class="sec" id="%s"><h2>%s</h2>%s%s</section>' % (sid, title, '<p class="sowhat">%s</p>' % so if so else '', body))

    def sec(self, sid, default_title, default_so, body):
        """A section whose heading and one-line summary can be authored (titles / sowhat)."""
        return self.section(sid, esc(self.title(sid, default_title)), self.au.get('sowhat', {}).get(sid, default_so), body)

    def is_superseded(self, qid):
        q = self.q[qid]
        return ('Superseded' in q['Question'] or 'first asked' in q['Question'] or q['Recommended answer'].startswith('Final')) and q['Status'].lower().startswith('answered')

    def open_q(self):
        return sorted([k for k, q in self.q.items() if q['Status'].lower().startswith('open')], key=qkey)

    def part_q(self):
        return sorted([k for k, q in self.q.items() if q['Status'].lower().startswith('answered in part')], key=qkey)


def qkey(x):
    m = re.search(r'(\d+)$', x)
    return (int(m.group(1)) if m else 0, x)


def doc_chips(d):
    return chips_html(d.status)


# =====================================================================================================
def release1(C):
    """Release panel from the plan's 'Release 1, blockers and estimates' section; authored 'release' keys override."""
    au = C.au.get('release', {})
    cont = notc = est = ''
    blocks_ = []
    pl = C.doc('PLAN')
    if pl:
        sec = [b for b in pl.sec('Release 1, blockers and estimates') if b[0] == 'ul']
        if sec:
            for it in sec[0][1]:
                m = re.match(r'\*\*(.+?):\*\*\s*(.*)', it, re.S)
                if not m:
                    continue
                lab, txt = m.group(1).lower(), m.group(2)
                if 'contains' in lab and 'not' not in lab:
                    cont, _, notc = txt.partition('**It does not contain:**')
                elif lab.startswith('blocking'):
                    blocks_ = [x.strip().rstrip('.') for x in txt.split(';') if x.strip()]
                elif lab.startswith('estimate'):
                    est = txt
    cont = au.get('contains', cont.strip().rstrip('.'))
    notc = au.get('not_contains', notc.strip().rstrip('.'))
    est = au.get('estimates', est.strip())
    blocks_ = au.get('blocking', blocks_)
    blocked_by = au.get('blocked_by', '; '.join(blocks_))
    return cont, notc, blocks_, est, blocked_by


def build_start(C):
    R = C.R
    au = C.au
    brief = C.doc('BRIEF')
    secs, out = [], []
    C.count['n_open'] = len(C.open_q())
    cont, notc, blocks_, est, blocked_by = release1(C)
    cov, extra = ['BRIEF'] if brief else [], []
    # ---- hero
    first, more = C.plain(brief) if brief else ('', [])
    outcome = ''
    if brief:
        ps = [b[1] for b in brief.sec('Outcome in one sentence') if b[0] == 'p']
        outcome = ps[0] if ps else ''
    cases = C.of_kind('case')
    ex_case = C.doc(au.get('worked_example', {}).get('case', '')) or (cases[0] if cases else None)
    example = ''
    if ex_case:
        ideal = [b for b in ex_case.sec('The ideal result, written by hand') if b[0] == 'ul']
        if ideal:
            pick = au.get('worked_example', {}).get('starts_with', '')
            items = [x for x in ideal[0][1] if x.startswith(pick)] if pick else ideal[0][1]
            example = items[0] if items else ''
    chips = au.get('start_chips')
    if chips is None:
        chips = [[brief.status, brief.status]] if brief and brief.status else []
    chip_html = ' '.join(chip(s, t) for s, t in chips)
    h1 = au.get('heroes', {}).get('start-here', {}).get('h1') or (brief.title if brief else au.get('brand', 'Planning workspace'))
    lede = au.get('heroes', {}).get('start-here', {}).get('lede', '')
    hero = '<div class="hero" id="BRIEF"><h1>%s</h1>%s' % (esc(h1), '<p class="lede">%s</p>' % esc(lede) if lede else '')
    if chip_html:
        hero += '<p>%s</p>' % chip_html
    if first:
        hero += '<div class="plain"><p>%s</p></div>' % R.inl(first)
    if outcome:
        hero += '<p class="outcome">%s</p>' % R.inl(outcome)
    if ex_case and example:
        hero += ('<div class="card"><h3>A worked example <span class="meta">%s</span></h3><p>%s</p><p class="small">%s</p></div>'
                 % (ex_case.id, R.inl(example), esc(C.T('example_note', 'Shown in full on the Story page.'))))
    hero += ('<p class="small legend"><strong>Evidence tags:</strong> <span class="ev">M</span> measured, <span class="ev">D</span> documented, <span class="ev">I</span> inferred, '
             '<span class="ev">T</span> needs a test.%s</p></div>' % esc(C.T('legend_extra', '')))
    out.append(hero)
    # ---- release panel
    if cont or notc or est or blocked_by:
        kv = ''
        for lab, v in (('Contains', cont), ('Does not contain', notc), ('Estimates', est), ('Blocked by', blocked_by)):
            if v:
                kv += '<dt>%s</dt><dd>%s</dd>' % (lab, R.inl(v))
        out.append('<div class="card k"><h3>%s <span class="meta">%s</span></h3><dl class="kv">%s</dl></div>' % (
            esc(au.get('release', {}).get('title', 'Release 1')), esc(au.get('release', {}).get('tag', 'phase 1')), kv))
    elif pl_exists(C):
        C.absent.append('release panel (authored release data or a plan section \'Release 1, blockers and estimates\')')
    # ---- needs you
    needs = au.get('needs')
    if needs:
        nr = ''.join('<tr><td><strong>%s</strong></td><td class="idc">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (esc(t), q, R.inl(o), R.inl(rec), R.inl(b)) for t, q, o, rec, b in needs)
        out.append('<div class="card" style="border-left:5px solid var(--warn)" id="needs-you"><h3>Needs you</h3><p class="small">%s</p><div class="tw"><table><thead><tr><th>What</th><th>Item</th><th>Who decides</th><th>Recommended answer</th><th>What it blocks</th></tr></thead><tbody>%s</tbody></table></div></div>'
                   % (esc(C.T('needs_intro', 'Things that need a named person. Each says what it blocks.')), nr))
    elif C.count['n_open']:
        C.absent.append("'needs you' rows (authored needs)")
    tg = au.get('tech_gloss')
    if tg:
        gl = ''.join('<dt>%s</dt><dd>%s</dd>' % (esc(a), esc(b)) for a, b in tg)
        out.append(details('Plain words for the technical terms used here', '<dl class="kv">%s</dl>' % gl, open_=True))
    cards = []
    if brief:
        def card(title, sec_name, chip_=''):
            bl = brief.sec(sec_name)
            if bl:
                cards.append('<div class="card"><h3>%s</h3>%s%s</div>' % (title, chip_, blocks(R, bl)))
        card('Who it is for', 'Who acts on the result, and what they do next')
        card('What would make them distrust it', 'What would make them distrust it')
        vp = [b[1] for b in brief.sec('The valuable part') if b[0] == 'p']
        if vp:
            hyp = 'hypothesis' in vp[0].lower() or 'hypothesis' in ' '.join(brief.sec_names()).lower()
            cards.append('<div class="card"><h3>%s</h3>%s</div>' % ('The valuable part, still a hypothesis' if hyp else 'The valuable part',
                                                                   '<p>%s</p>%s' % (chip('hypothesis'), R.inl(vp[0])) if hyp else '<p>%s</p>' % R.inl(vp[0])))
        card('What we are not doing', 'Non-goals and anti-goals')
        card('What success looks like', 'What success looks like')
    if cards:
        out.append('<div class="grid">%s</div>' % ''.join(cards))
    if au.get('faq'):
        out.append(details('Questions stakeholders ask', ''.join('<h4>%s</h4><p>%s</p>' % (esc(q), R.inl(a_)) for q, a_ in au['faq']), open_=True))
    if C.T('statebar'):
        out.append('<p class="statebar">%s</p>' % esc(C.T('statebar')))
    # ---- wireframe
    if True:
        secs.append(('st-sees', C.nav('st-sees', 'What the user sees')))
        out.append(C.sec('st-sees', 'The screen', '', C.diagram('H2', 'Wireframe', 'wireframe', lambda s: D.draw(s, 'H2'))))
    # ---- system context
    secs.append(('st-picture', C.nav('st-picture', 'The system in one picture')))
    out.append(C.sec('st-picture', 'The system in one picture', '', C.diagram('A', 'System context diagram', 'system_context', lambda s: D.draw(s, 'A')) +
                     ('<p class="small">%s</p>' % esc(C.T('picture_note')) if C.T('picture_note') else '')))
    # ---- journey
    j = au.get('journey')
    secs.append(('st-journey', C.nav('st-journey', 'The journey')))
    if j:
        jh = D.diag_I(j['steps'], j.get('note', ''), au.get('diagram_text'))
    else:
        C.missing.append('Journey diagram')
        jh = D.placeholder('I', 'Journey diagram')
    out.append(C.sec('st-journey', 'The user journey', '', jh))
    # ---- scope map and status board
    deferred = []
    pl = C.doc('PLAN')
    if pl:
        for t in pl.tables():
            if model.clean(t[1][0]) == 'Item':
                deferred = [model.clean(r[0]) for r in t[2]]
    C.count['n_def'] = len(deferred)
    if C.slices:
        secs.append(('st-scope', C.nav('st-scope', 'Scope by phase')))
        sc = au.get('scope_map')
        out.append(C.sec('st-scope', 'Scope by phase', '', D.placeholder('J', 'Scope map') if not sc else D.diag_J(C.slices, sc, deferred, au.get('diagram_text'))))
        if not sc:
            C.missing.append('Scope map')
    sl_status = {i: C.docs[i].status for i in C.slice_docs}
    cnt = {}
    for s in C.slices:
        cnt[s['phase']] = cnt.get(s['phase'], 0) + 1
    if C.gates or C.slices:
        secs.append(('st-status', C.nav('st-status', 'Status board')))
        sb = D.diag_K(C.gates, C.slices, sl_status, au.get('diagram_text'))
        if C.slices:
            sb += '<p class="small">%s</p>' % esc(C.T('status_note', 'Slices per phase: {per_phase}. {with_docs} of the {n_slices} slices have a slice document; the others are briefs in the plan table.').replace(
                '{per_phase}', ', '.join('phase %d: %d' % (p, n) for p, n in sorted(cnt.items()))).replace('{with_docs}', words(len(C.slice_docs)).capitalize()).replace('{n_slices}', str(len(C.slices))))
        out.append(C.sec('st-status', 'Status board', '', sb))
    # ---- decisions at a glance
    dec = C.of_kind('decision')
    C.count['n_decisions'] = len(dec)
    if dec:
        rows = []
        for d in dec:
            rows.append('<tr><td class="idc">%s</td><td>%s</td><td>%s%s<span class="small"> v%s</span></td><td>%s</td></tr>' % (
                d.id, '<strong>%s</strong>' % R.inl(d.fm.get('title', d.id)), chip(d.status), chip(d.fm.get('confidence', '')), d.version, R.inl(d.fm.get('summary', ''))))
        secs.append(('st-decisions', C.nav('st-decisions', 'Decisions at a glance')))
        out.append(C.sec('st-decisions', '%s decisions shape the design' % words(len(dec)).capitalize(), '',
                         '<div class="tw"><table><thead><tr><th>Decision</th><th>Plain words</th><th>Status</th><th>What was decided</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(rows) +
                         '<p>%s</p>' % A('decisions-and-risks', 'dr-decisions', 'Open the decisions with their alternatives and reasons')))
    # ---- open questions
    if C.q:
        open_ids = C.open_q()
        part_ids = C.part_q()
        ans_ids = [k for k in C.q if k not in open_ids and k not in part_ids]
        sup = [k for k in ans_ids if C.is_superseded(k)]
        plain_ans = [k for k in ans_ids if k not in sup]
        plan_text = {sl['id']: ' '.join([sl['exit'], sl['rests'], sl['title'], sl['flag']]) for sl in C.slices}
        for i in C.slice_docs:
            plan_text[i] = plan_text.get(i, '') + ' ' + ' '.join(b[1] for _, bl in C.docs[i].sections for b in bl if b[0] == 'p')

        def needed(qid):
            return [s for s, t in plan_text.items() if re.search(r'\b%s\b' % re.escape(qid), expand_ids(t))]

        def qcard(qid):
            q = C.q[qid]
            m = re.match(r'\*\*(.+?)\*\*', q['Question'])
            title = m.group(1) if m else q['Question']
            if not m:
                title = re.split(r'(?<=[a-z\)])\. |\? ', title)[0]
                if len(title) > 110:
                    title = title[:107].rsplit(' ', 1)[0] + '...'
            sl = needed(qid)
            h = '<div class="card"><h3>%s <span class="meta">%s</span></h3><p>%s</p>' % (R.inl(title.rstrip(':?.')), qid, R.cell(q['Status'], True))
            if m:
                h += '<p>%s</p>' % R.inl(re.sub(r'^\*\*.+?\*\*\s*', '', q['Question']))
            h += '<dl class="kv"><dt>Who can answer</dt><dd>%s</dd><dt>What it blocks</dt><dd>%s</dd><dt>Recommended answer</dt><dd>%s</dd><dt>Needed by</dt><dd>%s</dd></dl></div>' % (
                R.inl(q['Owner']), R.inl(q['Why it matters']), R.inl(q['Recommended answer']), ('slices ' + ', '.join(sl)) if sl else 'layer ' + q['Needed by layer'])
            return h
        secs.append(('st-human', C.nav('st-human', 'Open questions')))
        hb = '<h3>%s</h3><div class="grid">%s</div>' % (esc(C.T('open_heading', 'Open questions')), ''.join(qcard(k) for k in open_ids))
        if part_ids:
            hb += '<h3>Answered in part</h3><div class="grid">%s</div>' % ''.join(qcard(k) for k in part_ids)
        hb += '<p>%d questions are answered (%d plainly, %d where the final answer differs from the question as first asked%s). %s</p>' % (
            len(ans_ids), len(plain_ans), len(sup), (': ' + ', '.join(sorted(sup, key=qkey))) if sup else '', A('decisions-and-risks', 'dr-questions', 'Read them with their answers'))
        out.append(C.sec('st-human', 'Questions that still need a named person', '{n_open} questions still need a named person; the rest are answered.', hb))
    # ---- top risks
    if C.risks:
        byid = {r['id']: r for r in C.risks}
        top = [r for r in au.get('risk_top', []) if r in byid] or [r['id'] for r in sorted(C.risks, key=lambda r: (-r['score'], -r['impact'], r['id']))[:5]]
        r1 = au.get('risk_r1')
        short, plain_ = au.get('risk_short', {}), au.get('risk_plain', {})
        rrows = ''
        for rid in top:
            r = byid[rid]
            blk = 'yes' if rid in (r1 or []) else 'no'
            rrows += '<tr><td class="idc">%s</td><td><strong>%s</strong>%s</td><td>%s x %s = %s</td>%s<td>%s%s</td><td>%s</td></tr>' % (
                rid, esc(D.short_title(r, short)), '<br>' + esc(plain_[rid]) if plain_.get(rid) else '', r['impact'], r['unc'], r['score'],
                '<td>%s</td>' % blk if r1 is not None else '',
                ('Spike %s<br>' % ', '.join(r['spikes'])) if r['spikes'] else 'No spike: ', R.inl(r['plan']), R.cell(r['status'], True))
        secs.append(('st-risks', C.nav('st-risks', 'Top risks')))
        note = 'All %d risks are in the full table. ' % len(C.risks)
        if r1 is not None:
            note += C.T('risk_note', 'Risks that can stop release 1 (the builder\'s reading of the plan): {blockers}. ').replace('{blockers}', ', '.join(sorted(r1)))
        out.append(C.sec('st-risks', 'The riskiest assumptions each have a named test', '',
                         '<div class="tw"><table><thead><tr><th>Risk</th><th>What happens if it comes true</th><th>Impact x uncertainty</th>%s<th>What tests it</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div>' % (
                             '<th>Can it stop release 1?</th>' if r1 is not None else '', rrows) +
                         '<p class="small">%s%s</p>' % (esc(note), A('decisions-and-risks', 'dr-risks', 'Open the full risk table and the risk grid'))))
    # ---- conditions
    if C.gates or blocks_:
        grouped = []
        for g in C.gates:
            if g['Status'] != 'passed-with-conditions':
                continue
            if grouped and grouped[-1][0] == g['Notes']:
                grouped[-1][1].append(g)
            else:
                grouped.append((g['Notes'], [g]))
        cl = []
        for key, gs in grouped:
            names = ', '.join('layer %s %s' % (g['Layer'], g['Name'].lower()) for g in gs)
            cl.append('<li class="cond"><strong>%s</strong><ul>%s</ul></li>' % (esc(names[0].upper() + names[1:]), ''.join('<li>%s</li>' % R.inl(p) for p in model.split_sentences_notes(key))))
        cond_extra = ''.join('<li>%s</li>' % esc(x) for x in au.get('condition_notes', []))
        body = ''
        if blocks_:
            body += '<h3>Blocking conditions</h3><ul>%s</ul>' % ''.join('<li>%s</li>' % R.inl(b) for b in blocks_)
        if C.gates:
            npc = len([g for g in C.gates if g['Status'] == 'passed-with-conditions'])
            body += '<p>%s</p>' % esc(C.T('conditions_text', 'Each planning layer has a gate: a check that must pass, with evidence, before the layer counts as done. {n_pwc} layers are passed with conditions.').replace('{n_pwc}', words(npc).capitalize()))
            if cl:
                body += details('The conditions behind each layer' + C.T('conditions_extra_title', ''), '<ul class="check">%s</ul>%s' % (''.join(cl), '<ul>%s</ul>' % cond_extra if cond_extra else ''))
        secs.append(('st-conditions', C.nav('st-conditions', 'What passed with conditions means')))
        out.append(C.sec('st-conditions', 'Conditions on the plan', '', body))
    # ---- readers
    readers = au.get('readers')
    if readers:
        rr = []
        for r in readers:
            pgs = []
            for page, tok, note in r['pages']:
                if ID_ANY.match(tok):
                    pgs.append('%s <span class="small">%s</span>' % (tok, esc(note)))
                else:
                    pgs.append('%s' % A(page, tok, esc(note)))
            rr.append('<tr><td><strong>%s</strong><br><span class="small">%s</span></td><td>%s</td><td>%s</td></tr>' % (
                esc(r['who']), esc(r['people']), ', '.join(pgs), details('More to read', '<p>%s</p><p>Slices: %s</p>' % (', '.join(r['also']), ', '.join(r['slices'])))))
        secs.append(('st-readers', C.nav('st-readers', 'Who reads what')))
        out.append(C.sec('st-readers', 'Each team has a one-line reading list', 'Pick your team and read only the pages and slices in your row.',
                         '<div class="tw"><table><thead><tr><th>Team</th><th>Read first</th><th>Then</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(rr) +
                         '<p class="small">%sEverything on one page: <a href="everything.html">everything.html</a>.</p>' % (esc(C.T('readers_note', '')) + ' ' if C.T('readers_note', '') else '')))
    # ---- where we are
    if au.get('where_we_are'):
        secs.append(('st-state', C.nav('st-state', 'Where we are')))
        out.append(C.sec('st-state', 'Where we are', '', '<ul>%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in au['where_we_are'])))
    extra = au.get('start_covers', [])
    return secs, ''.join(out), cov, extra


def pl_exists(C):
    return C.doc('PLAN') is not None
