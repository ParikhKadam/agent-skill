"""Page builders, part 2: story and system."""
import re
from mdparse import esc, attr, inline, chip, expand_ids
import model, diagrams as D
from htmlkit import *
from pages_a import A, href, ID_ANY, words


def sub(R, d, name, h='h4', title=None, tab=None):
    """A heading and the blocks of one section of a doc; nothing when the section is empty."""
    bl = d.sec(name)
    if not bl:
        return ''
    return '<%s>%s</%s>%s' % (h, title or name, h, blocks(R, bl, tab=tab) if tab else blocks(R, bl))


def build_story(C):
    R = C.R
    au = C.au
    secs, out, cov = [], [], []
    cases = C.of_kind('case')
    fl, g = C.doc('FLOW-USER'), C.doc('GLOSSARY')
    if not (cases or fl or g):
        return None
    out.append(C.hero('story', 'Cases and the user flow', ''))
    wf = au.get('diagrams', {}).get('wireframe')
    if cases:
        body = []
        for d in cases:
            cid = d.id
            cov.append(cid)
            notes = au.get('case_notes', {}).get(cid, [])
            idx = 0
            parts = ['<article class="card k" id="%s"><h3>%s <span class="meta">%s · v%s</span></h3><p>%s%s</p><p>%s</p>' % (
                cid, R.inl(d.fm.get('title', cid)), cid, d.version, chip(d.status), chip('invented') if d.fm.get('invented') else '', R.inl(d.fm.get('summary', '')))]
            parts.append(sub(R, d, 'The situation'))
            parts.append(sub(R, d, 'What the user does today'))
            ideal = d.sec('The ideal result, written by hand')
            if ideal:
                parts.append('<h4>The ideal result, annotated</h4>')
            for b in ideal:
                if b[0] in ('ul', 'ol'):
                    tag = b[0]
                    lis = []
                    for it in b[1]:
                        ann = ''
                        if idx < len(notes):
                            tags, note = notes[idx]
                            ann = '<div class="small"><strong>How the system gets there.</strong> %s <span class="nowrap">%s</span></div>' % (esc(note), ', '.join(tags))
                        idx += 1
                        lis.append('<li>%s%s</li>' % (R.inl(it), ann))
                    parts.append('<%s>%s</%s>' % (tag, ''.join(lis), tag))
                else:
                    parts.append(blocks(R, [b]))
            if wf and wf.get('case') == cid:
                parts.append(D.draw(wf, 'H'))
            parts.append(sub(R, d, 'What was hard or surprising'))
            came = d.sec('Where it came from')
            facts = d.sec('Facts we reached for')
            if came or facts:
                parts.append(details('Where the case came from and the facts it reached for',
                                     blocks(R, came) + ('<h4>Facts we reached for</h4>' + blocks(R, facts) if facts else '')))
            parts.append('</article>')
            body.append(''.join(parts))
        secs.append(('sy-cases', C.nav('sy-cases', 'The worked cases')))
        out.append(C.sec('sy-cases', 'Worked cases', '', ''.join(body)))
    if fl:
        cov.append('FLOW-USER')
        steps = [b for b in fl.sec('The story, step by step') if b[0] == 'ol']
        fb = '<div id="FLOW-USER"></div>' + C.plain_html(fl)
        if steps:
            fb += '<h3>The story, step by step</h3><ol>%s</ol>' % ''.join('<li>%s</li>' % R.inl(s) for s in steps[0][1])
        other = fl.sec('Other paths')
        if other:
            fb += details(C.T('other_paths_title', 'Other paths'), blocks(R, other))
        fb += sub(R, fl, 'Re-entry points', 'h3', esc(C.T('reentry_heading', 'Where the user can step back in')))
        if fl.sec('Re-entries ruled out'):
            fb += details('Re-entries that were ruled out, and why', blocks(R, fl.sec('Re-entries ruled out')))
        fb += '<p class="small">User flow %s · FLOW-USER · v%s</p>' % (chip(fl.status), fl.version)
        secs.append(('sy-flow', C.nav('sy-flow', 'The user flow')))
        out.append(C.sec('sy-flow', 'The user flow', '', fb))
    if g:
        cov.append('GLOSSARY')
        gb = '<div id="GLOSSARY"></div>' + C.plain_html(g)
        if g.tables():
            gb += table(R, g.tables()[0][1], g.tables()[0][2], first_is_id=False)
        secs.append(('sy-glossary', C.nav('sy-glossary', 'Glossary')))
        out.append(C.sec('sy-glossary', 'Glossary', '', gb))
    return secs, ''.join(out), cov, []


# =====================================================================================================
def classify_factory(au):
    """Cell classifier for the permission grid. Labels are authored: [[prefix, label]]; a prefix starting with ~ matches anywhere."""
    labels = au.get('permission_labels', [])
    debug = au.get('permission_debug_actor', '').lower()

    def classify(actor, col, cell):
        c = cell.lower()
        on = bool(debug) and debug in actor.lower()
        if c.startswith('n/a'):
            return 'pu', 'n/a'
        if c.startswith('no'):
            return 'pn', 'no'
        lab = 'yes'
        for pref, l in labels:
            if (pref[1:] in c) if pref.startswith('~') else c.startswith(pref):
                lab = l
                break
        return ('pd' if on else 'pa'), lab
    return classify


def build_system(C):
    R = C.R
    au = C.au
    secs, out, cov = [], [], []
    ar, sf, cc, co, fa, ex = (C.doc(i) for i in ('ARTIFACTS', 'FLOW-SYSTEM', 'CROSSCUT', 'CONSTRAINTS', 'FACTS', 'EXISTING'))
    comps = sorted(C.comps, key=lambda c: (au.get('order', {}).get('component', []).index(c['id']) if c['id'] in au.get('order', {}).get('component', []) else 999, c['id']))
    if not (ar or sf or cc or co or fa or ex or comps):
        return None
    C.count['n_components'] = len(comps)
    out.append(C.hero('system', 'The system: parts, flows and rules', ''))
    if au.get('diagrams', {}).get('system_context'):
        secs.append(('sys-picture', C.nav('sys-picture', 'The system in one picture')))
        out.append(C.sec('sys-picture', 'The system in one picture', '', '<p>%s</p>' % esc(C.T('sys_picture_body', 'The system picture is on the %s page, so it exists once.')).replace('%s', A('start-here', 'st-picture', 'Start here'))))
    # --- artifacts
    if ar and ar.tables():
        cov.append('ARTIFACTS')
        art_ids = {model.clean(r[0]) for r in ar.tables()[0][2]}
        ab = '<div id="ARTIFACTS"></div>' + C.plain_html(ar)
        edits = au.get('dependency_edits', [])
        if edits:
            ab += '<h3>If you change X, these become outdated</h3><div class="tw"><table><thead><tr><th>If this changes</th><th>These become outdated</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(
                '<tr><td>%s</td><td>%s</td></tr>' % (esc(s_), ', '.join(d_)) for s_, d_ in edits)
        if comps and C.art_titles:
            dm = au.get('dependency_map', {})
            ab += details(C.T('dependency_map_title', 'Dependency map: what each component reads and writes (a busy diagram)'),
                          D.diag_B(comps, C.art_titles, au.get('art_part', {}), edits, dm.get('hub', ''), dm.get('hub_label', ''), dm.get('order') or au.get('order', {}).get('component', []), au.get('diagram_text')))
        ab += '<h3>The %d stored or derived results</h3>' % len(ar.tables()[0][2]) + table(R, ar.tables()[0][1], ar.tables()[0][2], anchor_ids=art_ids)
        items = [b for b in ar.sec('Decisions found by filling in this table') if b[0] == 'ol']
        hl = []
        for it in (items[0][1] if items else []):
            m = re.match(r'\*\*(H-\d+) ([^*]+?)\.\*\*\s*(.*)', it, re.S)
            if m:
                hl.append(details('%s <span class="meta">%s</span>' % (esc(m.group(2)), m.group(1)), '<p>%s</p>' % R.inl(m.group(3)), sid=m.group(1)))
        if hl:
            ab += '<h3>The %s rules found while filling in the table</h3>' % words(len(hl)) + ''.join(hl)
        ab += '<p class="small">Artifacts %s · ARTIFACTS · v%s</p>' % (chip(ar.status), ar.version)
        secs.append(('sys-artifacts', C.nav('sys-artifacts', 'Stored results and what goes stale')))
        out.append(C.sec('sys-artifacts', 'Stored results and what goes stale', '', ab))
    # --- re-entry matrix
    if ar or sf:
        re_ = au.get('reentry')
        secs.append(('sys-matrix', C.nav('sys-matrix', 'Re-entry matrix')))
        if re_:
            mh = D.diag_E(re_['cols'], re_['rows'], re_.get('star_note', ''), au.get('diagram_text'))
        else:
            C.missing.append('Re-entry matrix')
            mh = D.placeholder('E', 'Re-entry matrix')
        out.append(C.sec('sys-matrix', 'Re-entry matrix', '', mh))
    # --- components
    if comps:
        cb = ''
        tr = {t[0]: t for t in C.tracks}
        for c in comps:
            cid = c['id']
            cov.append(cid)
            d = C.docs[cid]
            t = tr.get(c['side'])
            trk = t[2][1:] if t else ''
            io = ''
            for k, lab in (('reads_raw', 'Reads'), ('writes_raw', 'Writes')):
                v = re.sub(r'^(Reads|Writes) \([^)]*\):\s*', '', c[k])
                io += '<dt>%s</dt><dd>%s</dd>' % (lab, R.inl(v))
            inner = ''
            for name in ['Who decides inside', 'Runs alone', 'Quality bar and test set', 'Failure modes', 'Cost, latency and owner']:
                inner += sub(R, d, name)
            cb += ('<article class="card%s" id="%s"><h3>%s <span class="meta">%s · v%s</span></h3><p>%s %s %s</p><p>%s</p><dl class="kv">%s</dl>%s%s</article>' % (
                ' cb-' + trk if trk else '', cid, R.inl(d.fm.get('title', cid)), cid, d.version, chip(d.status),
                '<span class="chip track" style="background:var(--%s)">%s</span>' % (trk, t[1]) if t else '',
                chip(c['card_status']) if c['card_status'] else '', R.inl(d.fm.get('summary', '')), io,
                '<div class="plain"><p>%s</p></div>' % R.inl(C.plain(d)[0]) if C.plain(d)[0] else '',
                details('Who decides inside, runs alone, quality bar, failure modes, cost and owner', inner)))
        secs.append(('sys-components', C.nav('sys-components', 'The components')))
        out.append(C.sec('sys-components', 'The %s components' % words(len(comps)), '', cb))
    # --- system flow
    if sf:
        cov.append('FLOW-SYSTEM')
        seqs = au.get('sequences', [])
        full = [q for q in seqs if q.get('size') == 'full'] or seqs[:1]
        small = [q for q in seqs if q not in full]
        fb = '<div id="FLOW-SYSTEM"></div>' + C.plain_html(sf)
        run_name = next((n for n in sf.sec_names() if n.startswith('A full run')), None)
        fb += '<h3>%s</h3>' % esc(C.T('full_run_heading', 'A full run'))
        if full:
            fb += D.sequence_from(full[0])
        else:
            C.missing.append('Sequence diagrams')
            fb += D.placeholder('C1', 'Sequence diagrams')
        if run_name:
            ols = [b for b in sf.sec(run_name) if b[0] == 'ol']
            ps = [b for b in sf.sec(run_name) if b[0] == 'p']
            if ols:
                fb += '<ol>%s</ol>' % ''.join('<li>%s</li>' % R.inl(i) for i in ols[0][1])
            if ps:
                fb += '<p>%s</p>' % R.inl(ps[0][1])
        if small:
            fb += '<h3>%s</h3><div class="grid">%s</div>' % (esc(C.T('small_sequences_heading', 'More sequences')), ''.join(D.sequence_from(q) for q in small))
        st_blocks = sf.sec('Start points')
        if st_blocks:
            fb += '<h3>Start points: where a run can begin</h3>' + blocks(R, [b for b in st_blocks if b[0] == 'table']) + blocks(R, [b for b in st_blocks if b[0] == 'p'])
        fail = sf.sec('What happens when a step fails')
        ft_ = au.get('diagrams', {}).get('failure_tree')
        if fail or ft_:
            fb += '<h3>What happens when a step fails</h3>' + blocks(R, fail)
            if ft_:
                fb += D.draw(ft_, 'F')
            else:
                C.missing.append('Failure and retry tree')
                fb += D.placeholder('F', 'Failure and retry tree')
        for name, title in (('Duplicates, retries and concurrency', None), ('Visibility and budgets', None)):
            if sf.sec(name):
                fb += details(name, blocks(R, sf.sec(name)))
        fb += '<p class="small">System flow %s · FLOW-SYSTEM · v%s</p>' % (chip(sf.status), sf.version)
        secs.append(('sys-flow', C.nav('sys-flow', 'The system flow')))
        out.append(C.sec('sys-flow', 'The system flow', '', fb))
        secs.append(('sys-states', C.nav('sys-states', 'Part states')))
        sm = au.get('diagrams', {}).get('state_machine')
        if sm:
            smh = D.draw(sm, 'D')
        else:
            C.missing.append('State machine')
            smh = D.placeholder('D', 'State machine')
        out.append(C.sec('sys-states', 'States', '', smh))
    # --- cross-cutting
    if cc:
        cov.append('CROSSCUT')
        pm = model.perm_matrix(cc)
        cb = '<div id="CROSSCUT"></div>' + C.plain_html(cc)
        if pm:
            head, rows = pm
            cb += D.diag_M(head, rows, classify_factory(au), au.get('diagram_text'))
            cb += details('The permission matrix in full words', table(R, cc.tables()[0][1], cc.tables()[0][2], first_is_id=False) +
                          blocks(R, [b for b in cc.sec('Permission matrix (actors × artifacts × actions)') if b[0] == 'p']))
        vt = [b for b in cc.sec('Verdicts') if b[0] == 'table']
        if vt:
            verd = vt[0]
            chipsets = {}
            for r in model.fix_rows(verd[1], verd[2])[0]:
                v = model.clean(r[1]).split(',')[0].split(' (')[0].strip()
                chipsets.setdefault(v, []).append(model.clean(r[0]))
            summ = ''.join('<p><strong>%s:</strong> %s</p>' % (esc(k), '; '.join(esc(x) for x in v)) for k, v in chipsets.items())
            cb += '<h3>Verdict for every concern</h3>' + summ
            cb += details('What each verdict means for the design (full table)', table(R, verd[1], verd[2], first_is_id=False))
        if cc.sec('Interactions found'):
            cb += details('Interactions found between concerns', blocks(R, cc.sec('Interactions found')))
        cb += '<p class="small">Cross-cutting %s · CROSSCUT · v%s</p>' % (chip(cc.status), cc.version)
        secs.append(('sys-cross', C.nav('sys-cross', 'Cross-cutting rules')))
        out.append(C.sec('sys-cross', 'Cross-cutting rules', '', cb))
    # --- constraints
    if co and co.tables():
        cov.append('CONSTRAINTS')
        xt = co.tables()[0]
        xids = {model.clean(r[0]) for r in xt[2]}
        secs.append(('sys-constraints', C.nav('sys-constraints', 'Constraints')))
        out.append(C.sec('sys-constraints', 'Constraints', '', '<div id="CONSTRAINTS"></div>' + C.plain_html(co) + table(R, xt[1], xt[2], anchor_ids=xids) +
                         '<p class="small">Constraints %s · CONSTRAINTS · v%s</p>' % (chip(co.status), co.version)))
    # --- facts
    if fa and fa.tables():
        cov.append('FACTS')
        ft = fa.tables()[0]
        fids = {model.clean(r[0]) for r in ft[2]}
        hd = [model.clean(h) for h in ft[1]]
        cols = {hd.index('Status')} if 'Status' in hd else set()
        fb = '<div id="FACTS"></div>' + C.plain_html(fa) + details('All %d facts with where they live, how reliable they are and their status' % len(ft[2]),
                                                                  table(R, ft[1], ft[2], anchor_ids=fids, chip_cols=cols), open_=False)
        fb += '<p class="small">Facts %s · FACTS · v%s</p>' % (chip(fa.status), fa.version)
        secs.append(('sys-facts', C.nav('sys-facts', 'Facts')))
        out.append(C.sec('sys-facts', 'Facts', '', fb))
    # --- existing
    if ex:
        cov.append('EXISTING')
        eb = '<div id="EXISTING"></div>' + C.plain_html(ex)
        if ex.tables():
            eb += table(R, ex.tables()[0][1], ex.tables()[0][2], first_is_id=False)
        br = C.doc('BRIEF')
        if br and (C.plain(br)[1] or br.sec('Size and depth') or br.sec('What already exists')):
            eb += details('Where the plan comes from: source rule, authorised extras, size and what already exists', ''.join('<p>%s</p>' % R.inl(p) for p in C.plain(br)[1]) +
                          sub(R, br, 'Size and depth', title='Size and depth') + sub(R, br, 'What already exists'))
        if ex.sec('Things that behave differently from what the docs say'):
            eb += '<h3>Things that behave differently from what the docs say</h3>' + blocks(R, ex.sec('Things that behave differently from what the docs say'))
        eb += '<p class="small">Existing system %s · EXISTING · v%s</p>' % (chip(ex.status), ex.version)
        secs.append(('sys-existing', C.nav('sys-existing', 'The existing system')))
        out.append(C.sec('sys-existing', 'The existing system', '', eb))
    cov = [x for x in ['ARTIFACTS', 'FLOW-SYSTEM', 'CROSSCUT', 'CONSTRAINTS', 'FACTS', 'EXISTING'] if x in cov] + [c['id'] for c in comps]
    return secs, ''.join(out), cov, []
