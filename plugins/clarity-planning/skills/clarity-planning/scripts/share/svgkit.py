"""Tiny inline-SVG toolkit. Colours come from CSS classes (variables), never inline, so both themes work."""
import re
from mdparse import esc, attr


def wrap(s, px, cw=5.9):
    n = max(8, int(px / cw))
    words = s.split()
    out, cur = [], ''
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= n:
            cur = (cur + ' ' + w).strip()
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out or ['']


class Svg:
    def __init__(self, key, w, h, title, desc):
        self.key, self.w, self.h, self.title, self.desc = key, w, h, title, desc
        self.p = []
        self.markers = set()

    def raw(self, s):
        self.p.append(s)

    def rect(self, x, y, w, h, cls='', rx=8):
        self.p.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>' % (x, y, w, h, rx, cls))

    def text(self, x, y, s, cls='ts', anchor='start'):
        self.p.append('<text x="%g" y="%g" class="%s" text-anchor="%s">%s</text>' % (x, y, cls, anchor, esc(s)))

    def lines(self, x, y, ls, cls='ts', anchor='start', lh=14):
        for i, l in enumerate(ls):
            self.text(x, y + i * lh, l, cls, anchor)

    def node(self, x, y, w, h, cls, title, lines=(), anchor='middle', tcls='tt', scls='ts', wrap_lines=True, lh=13.5):
        self.rect(x, y, w, h, 'nd ' + cls)
        cx = x + w / 2 if anchor == 'middle' else x + 10
        ty = y + 18
        tl = wrap(title, w - 16, 6.6) if wrap_lines else [title]
        for t in tl:
            self.text(cx, ty, t, tcls, anchor)
            ty += 15
        ty += -1
        for l in lines:
            for wl in (wrap(l, w - 16) if wrap_lines else [l]):
                self.text(cx, ty, wl, scls, anchor)
                ty += lh
        return ty

    def marker(self, name):
        self.markers.add(name)
        return 'url(#mk-%s-%s)' % (self.key, name)

    def path(self, d, cls='e', mk='a', start=None):
        m = ' marker-end="%s"' % self.marker(mk) if mk else ''
        s = ' marker-start="%s"' % self.marker(start) if start else ''
        self.p.append('<path d="%s" class="%s"%s%s/>' % (d, cls, m, s))

    def poly(self, pts, cls='e', mk='a', start=None, round_=0):
        d = 'M%g %g' % pts[0] + ''.join(' L%g %g' % p for p in pts[1:])
        self.path(d, cls, mk, start)

    def label(self, x, y, s, cls='tl', anchor='middle'):
        self.p.append('<text x="%g" y="%g" class="%s halo" text-anchor="%s">%s</text>' % (x, y, cls, anchor, esc(s)))

    def render(self, caption, extra_after='', wide=720):
        defs = ''.join('<marker id="mk-%s-%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="mkp mk-%s"/></marker>' % (self.key, n, n) for n in sorted(self.markers))
        svg = ('<svg viewBox="0 0 %g %g" role="img" aria-labelledby="ti-%s de-%s" style="min-width:%dpx"><title id="ti-%s">%s</title><desc id="de-%s">%s</desc><defs>%s</defs>%s</svg>'
               % (self.w, self.h, self.key, self.key, min(wide, self.w), self.key, esc(self.title), self.key, esc(self.desc), defs, ''.join(self.p)))
        return '<figure class="diagram" id="fig-%s"><div class="dscroll">%s</div>%s<figcaption>%s</figcaption></figure>' % (self.key, svg, extra_after, caption)
