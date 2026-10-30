"""CSS and the tiny optional script. Everything works without the script."""

LIGHT = dict(bg='#fbfaf7', fg='#1f2328', mut='#59636e', card='#ffffff', line='#d9d6cc', acc='#1b5e8a', chip='#eef3f7', warn='#9a5b00',
             b='#2f6fa3', bbg='#e4eef7', l='#2f8f6b', lbg='#e2f3ec', f='#b4651f', fbg='#fbeadb', x='#6b7280', xbg='#eeeff2', q='#7a4fb0', qbg='#eee7f8',
             ok='#1f7a4d', okbg='#e3f3ea', bad='#a33a3a', badbg='#f9e4e4', warnbg='#fdf0d8', cond='#7a6a12', condbg='#f4efc9', edge='#4b5560', zebra='#f3f1ea')
DARK = dict(bg='#15181c', fg='#e6e8ea', mut='#9aa4ae', card='#1d2127', line='#323941', acc='#6db3e0', chip='#25303a', warn='#e0a85a',
            b='#6db3e0', bbg='#1d2c3a', l='#5fcf9f', lbg='#1b3028', f='#e8a366', fbg='#3a2a1b', x='#9aa4ae', xbg='#262b31', q='#b79be3', qbg='#2c2540',
            ok='#6fd39b', okbg='#1c3327', bad='#ee8c8c', badbg='#3a2121', warnbg='#3a2e16', cond='#d9c75a', condbg='#35311a', edge='#a9b3bd', zebra='#1a1e23')

CHIPS = {  # status: (light fg, light bg, dark fg, dark bg)
    'agreed': ('#1f7a4d', '#e3f3ea', '#6fd39b', '#1c3327'), 'passed': ('#14653c', '#cfeadb', '#7fe0aa', '#1f3d2d'),
    'passed-with-conditions': ('#7a6a12', '#f4efc9', '#d9c75a', '#35311a'), 'pending': ('#9a5b00', '#fdf0d8', '#e0a85a', '#3a2e16'),
    'draft': ('#59636e', '#eceef0', '#a9b3bd', '#2a2f35'), 'decided': ('#1b5e8a', '#e0eef7', '#7fc0ea', '#1c2f40'),
    'hypothesis': ('#6b3fa0', '#eee6f7', '#c2a6ec', '#2f2540'), 'measured': ('#0f766e', '#dff3f0', '#6fd8cd', '#173532'),
    'doc': ('#475569', '#e8ecf1', '#aab6c6', '#262d37'), 'inferred': ('#4f46a5', '#e8e6f8', '#b0a9ee', '#272541'),
    'unknown': ('#a33a3a', '#f9e4e4', '#ee8c8c', '#3a2121'), 'invented': ('#a8326e', '#fbe3ef', '#f09ac4', '#3d2030'),
    'answered': ('#0e7490', '#dff2f8', '#78d3ea', '#16313a'), 'open': ('#b4501a', '#fde8da', '#f0a272', '#3b2517'),
    'deferred': ('#6b7280', '#eef0f3', '#a9b0ba', '#2a2e34'), 'accepted': ('#3f6212', '#ecf5d9', '#b4dc7a', '#26331a'),
    'mitigated': ('#166534', '#dcf3e4', '#7fdca2', '#1b3526'), 'not-started': ('#59636e', '#eceef0', '#a9b3bd', '#2a2f35'),
    'in-progress': ('#9a5b00', '#fdf0d8', '#e0a85a', '#3a2e16'), 'skipped': ('#6b7280', '#eef0f3', '#a9b0ba', '#2a2e34'), 'dropped': ('#6b7280', '#eef0f3', '#a9b0ba', '#2a2e34'),
}


def vars_block(d):
    return ''.join('--%s:%s;' % (k, v) for k, v in d.items())


def chip_css(idx):
    out = []
    for k, v in CHIPS.items():
        fg, bg = v[idx], v[idx + 1]
        out.append('.chip[data-s="%s"]{color:%s;background:%s;border-color:%s}' % (k, fg, bg, fg))
    return ''.join(out)


def css():
    return """
:root{%(light)s}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){%(dark)s}%(chipdark)s}
:root[data-theme=dark]{%(dark)s}
:root[data-theme=dark] .chip{}
%(chiplight)s
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-text-size-adjust:100%%}
[id]{scroll-margin-top:132px}
a{color:var(--acc)}
a.id,a.svg-id{color:var(--mut);font-size:.82em;text-decoration:none;border-bottom:1px dotted var(--mut);white-space:nowrap}
a.id:hover{color:var(--acc);border-bottom-color:var(--acc)}
.top{position:sticky;top:0;z-index:50;background:var(--card);border-bottom:1px solid var(--line);box-shadow:0 1px 6px rgba(0,0,0,.06)}
.top .r1,.top .r2{display:flex;gap:6px;align-items:center;overflow-x:auto;white-space:nowrap;padding:6px 16px;max-width:1180px;margin:0 auto;scrollbar-width:thin}
.top .r2{padding-top:0;padding-bottom:7px}
.top .r3{font-size:12px;color:var(--mut);padding:0 16px 6px;max-width:1180px;margin:0 auto;overflow-x:auto;white-space:nowrap}
.top .brand{font-weight:700;margin-right:6px;font-size:14px}
.top a.pg{padding:4px 11px;border:1px solid var(--line);border-radius:999px;color:var(--fg);text-decoration:none;font-size:13px}
.top a.pg.on{background:var(--acc);border-color:var(--acc);color:var(--bg)}
.top a.sec{font-size:12.5px;color:var(--mut);text-decoration:none;padding:2px 8px;border-radius:6px}
.top a.sec:hover{background:var(--chip);color:var(--fg)}
.top .sp{flex:1}
.tool{display:none;font:inherit;font-size:12.5px;padding:3px 10px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);cursor:pointer}
.js .tool{display:inline-block}
main{max-width:1060px;margin:0 auto;padding:12px 16px 56px}
h1{font-size:clamp(25px,4.4vw,36px);line-height:1.2;margin:24px 0 8px;letter-spacing:-.01em}
h2{font-size:clamp(20px,3vw,25px);line-height:1.3;margin:0 0 6px}
h3{font-size:18px;line-height:1.35;margin:22px 0 6px}
h4{font-size:15.5px;margin:16px 0 4px}
.lede{color:var(--mut);font-size:17px;margin:0 0 14px;max-width:760px}
section.sec{margin:46px 0 0;padding-top:20px;border-top:2px solid var(--line)}
section.sec>.sowhat{font-size:17.5px;font-weight:600;margin:2px 0 12px;max-width:820px}
.plain{background:var(--chip);border-left:4px solid var(--acc);border-radius:0 8px 8px 0;padding:10px 16px;margin:10px 0 16px;max-width:860px}
.plain::before{content:"In plain words";display:block;font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut);margin-bottom:2px}
.meta{color:var(--mut);font-size:12.5px;font-weight:400;margin-left:6px;white-space:nowrap}
.meta a{color:inherit}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:14px 0}
.card>h3{margin:0 0 6px;font-size:18px}
.card.k{border-left:5px solid var(--acc)}
.cb-b{border-left:5px solid var(--b)}.cb-l{border-left:5px solid var(--l)}.cb-f{border-left:5px solid var(--f)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin:12px 0}
.grid .card{margin:0}
.hero{background:linear-gradient(135deg,var(--chip),var(--card));border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin:14px 0}
.hero .outcome{font-size:19px;font-weight:600;margin:10px 0 0;max-width:820px}
.statebar{border:1px solid var(--warn);border-left-width:6px;border-radius:8px;background:var(--card);padding:8px 14px;margin:12px 0;font-weight:600}
.chip{display:inline-block;padding:0 9px;border-radius:999px;border:1px solid;font-size:12px;line-height:19px;margin:0 3px 0 0;white-space:nowrap;font-weight:600;vertical-align:1px}
.chip[data-s=deferred]{border-style:dashed}
.chip-h{font-size:11px}
.chip.track{color:var(--bg);border-color:transparent}
.ev{display:inline-block;min-width:19px;text-align:center;padding:0 5px;border-radius:5px;background:var(--chip);border:1px solid var(--line);font-size:11px;font-weight:700;color:var(--mut)}
.src{color:var(--mut);font-size:.82em}
.gloss{color:var(--mut);font-size:.9em;font-style:italic}
code{background:var(--chip);padding:1px 5px;border-radius:4px;font-size:.88em;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;overflow-wrap:anywhere}
pre{background:var(--chip);border:1px solid var(--line);padding:12px 14px;border-radius:8px;overflow-x:auto;font-size:12.5px;line-height:1.5;margin:6px 0}
pre code{background:none;padding:0;overflow-wrap:normal}
.tw{overflow-x:auto;margin:10px 0;border-radius:8px}
table{border-collapse:collapse;width:100%%;font-size:14px;background:var(--card)}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
th{background:var(--chip);font-weight:600}
tr.grp td{background:var(--chip);font-weight:700}
td.idc{white-space:nowrap}
ul,ol{padding-left:22px;margin:6px 0 10px}li{margin:3px 0}
details{margin:10px 0;border:1px solid var(--line);border-radius:10px;background:var(--card)}
details>summary{cursor:pointer;padding:8px 14px;font-weight:600;list-style:none;display:flex;gap:8px;align-items:baseline}
details>summary::before{content:"\\25B8";color:var(--mut);flex:none}
details[open]>summary::before{content:"\\25BE"}
details>summary::-webkit-details-marker{display:none}
details>.dbody{padding:2px 16px 12px}
details details{background:var(--bg)}
td details{border:0;margin:0;background:none}td details>summary{padding:0;font-weight:500;color:var(--acc)}td details>.dbody{padding:4px 0 0}
.kv{display:grid;grid-template-columns:150px 1fr;gap:4px 14px;margin:8px 0;font-size:14.5px}.kv dt{color:var(--mut)}.kv dd{margin:0}
.copy{float:right;font-size:12px;padding:2px 9px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);cursor:pointer;display:none;margin-left:8px}
.js .copy{display:inline-block}
.diagram{margin:16px 0;border:1px solid var(--line);border-radius:12px;background:var(--card);padding:10px 12px 8px;break-inside:avoid}
.dscroll{overflow-x:auto}
.diagram svg{width:100%%;height:auto;display:block}
.diagram figcaption{color:var(--mut);font-size:13px;margin-top:6px}
svg text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;fill:var(--fg)}
svg .tt{font-size:12.5px;font-weight:700}svg .ts2{font-size:11.5px;font-weight:600}svg .ts{font-size:11px;fill:var(--mut)}svg .tl{font-size:11px;font-weight:600}
svg .halo{paint-order:stroke;stroke:var(--card);stroke-width:4px;stroke-linejoin:round}
svg a text,svg text a{text-decoration:none}svg a.svg-id{fill:var(--mut);text-decoration:underline dotted}
svg .nd{stroke-width:1.2}
svg .nb{fill:var(--bbg);stroke:var(--b)}svg .nl{fill:var(--lbg);stroke:var(--l)}svg .nf{fill:var(--fbg);stroke:var(--f)}svg .nx{fill:var(--xbg);stroke:var(--x)}
svg .nq{fill:var(--qbg);stroke:var(--q)}svg .ng{fill:var(--card);stroke:var(--line)}svg .na{fill:var(--warnbg);stroke:var(--warn)}svg .nok{fill:var(--okbg);stroke:var(--ok)}
svg .nbad{fill:var(--badbg);stroke:var(--bad)}svg .ncond{fill:var(--condbg);stroke:var(--cond)}svg .nj{fill:var(--q);stroke:var(--q)}
svg .nbl{fill:var(--lbg);stroke:var(--b);stroke-width:2}
svg .cont{fill:none;stroke-width:1.5;stroke-dasharray:5 4}svg .cb{stroke:var(--b)}svg .cl{stroke:var(--l)}svg .cx{stroke:var(--x)}
svg .e{fill:none;stroke:var(--edge);stroke-width:1.5}svg .eq{stroke:var(--q);stroke-width:2}svg .ecb{stroke:var(--l);stroke-dasharray:6 3;stroke-width:2}svg .edash{stroke-dasharray:4 3}
svg .ebad{stroke:var(--bad)}svg .eread{stroke:var(--b);stroke-width:1.2;opacity:.8}svg .ewrite{stroke:var(--f);stroke-width:1.2;opacity:.85}svg .hub{opacity:.28}svg .eflow{stroke:var(--q);stroke-width:2.4;stroke-dasharray:3 3}svg .mk-f{fill:var(--q)}svg .eout{stroke:var(--warn);stroke-dasharray:5 3;stroke-width:1.8}svg .eleader{stroke:var(--mut);stroke-dasharray:3 3;stroke-width:1}
svg .mkp{stroke:none}svg .mk-a,svg .mk-g{fill:var(--edge)}svg .mk-q{fill:var(--q)}svg .mk-cb{fill:var(--l)}svg .mk-w{fill:var(--bad)}svg .mk-r{fill:var(--b)}svg .mk-o{fill:var(--warn)}
svg .mk-w{fill:var(--f)}
svg .life{stroke:var(--line);stroke-width:1.2;stroke-dasharray:3 4}svg .band{fill:var(--chip);stroke:none}svg .zebra{fill:var(--zebra)}
svg .cell{stroke:none}svg .cr{fill:var(--bbg);stroke:var(--b);stroke-width:1.2}svg .co{fill:var(--warnbg);stroke:var(--warn);stroke-width:1.2}svg .co.cond{stroke-dasharray:4 3}svg .cu{fill:var(--card);stroke:var(--line)}
svg .pa{fill:var(--okbg);stroke:var(--ok)}svg .pd{fill:var(--warnbg);stroke:var(--warn)}svg .pn{fill:var(--badbg);stroke:var(--bad)}svg .pu{fill:var(--xbg);stroke:var(--line)}
svg .lane{fill:var(--zebra);stroke:var(--line)}svg .freeze{stroke:var(--q);stroke-width:2;stroke-dasharray:6 4}
svg .heat{stroke:var(--line)}svg .h0{fill:var(--okbg)}svg .h1{fill:var(--warnbg)}svg .h2{fill:var(--badbg)}
svg .phone{fill:var(--card);stroke:var(--mut);stroke-width:2}svg .wf{fill:var(--bg);stroke:var(--line)}svg .badbox{stroke:var(--bad)}svg .warnbox{stroke:var(--warn)}
svg .chipw{stroke:none;fill:var(--chip)}svg .chipw.ok{fill:var(--okbg)}svg .chipw.bad{fill:var(--badbg)}svg .chipw.warn{fill:var(--warnbg)}svg .chipw.off{fill:var(--xbg)}svg .btn{stroke:var(--acc)}
.perm td.a{background:var(--okbg)}.perm td.d{background:var(--warnbg)}.perm td.n{background:var(--badbg)}
footer{border-top:1px solid var(--line);margin-top:56px;padding:16px;color:var(--mut);font-size:13px;max-width:1060px;margin-left:auto;margin-right:auto}
footer details{border:0;background:none}
.toc{columns:2 300px;column-gap:30px;margin:10px 0}.toc li{break-inside:avoid;list-style:none}.toc ul{padding-left:0}
.toc .pt{font-weight:700;margin-top:8px;display:block}
.check{list-style:none;padding-left:0}.check li{padding-left:28px;position:relative;margin:6px 0}.check li::before{content:"\\2611";position:absolute;left:0;color:var(--ok);font-size:18px}.check li.cond::before{content:"\\25D0";color:var(--cond)}.check li.todo::before{content:"\\2610";color:var(--mut)}
.small{font-size:13.5px;color:var(--mut)}
.nowrap{white-space:nowrap}
.legend span{margin-right:12px}
@media (max-width:640px){body{font-size:15.5px}.kv{grid-template-columns:1fr}.top .r3{font-size:12px;color:var(--mut);padding:0 16px 6px;max-width:1180px;margin:0 auto;overflow-x:auto;white-space:nowrap}
.top .brand{display:none}main{padding:8px 14px 40px}th,td{padding:5px 7px}}
@media print{
 body{background:#fff;color:#000;font-size:11pt}.top{position:static;box-shadow:none}.top .r2,.top .r3,.tool,.copy{display:none!important}
 details>summary::before{content:""}
 details::details-content{content-visibility:visible!important;display:block!important;height:auto!important}
 details>*:not(summary){display:block!important}
 .card,.diagram,table,tr,figure,.hero{break-inside:avoid}h1,h2,h3,h4{break-after:avoid}
 section.sec{border-top:1px solid #999}.tw{overflow:visible}pre{white-space:pre-wrap}.dscroll{overflow:visible}
 a{color:inherit;text-decoration:none}svg{max-width:100%%}
}
""" % dict(light=vars_block(LIGHT), dark=vars_block(DARK), chiplight=chip_css(0), chipdark=''.join(
        ':root:not([data-theme=light]) .chip[data-s="%s"]{color:%s;background:%s;border-color:%s}' % (k, v[2], v[3], v[2]) for k, v in CHIPS.items())) + ''.join(
        ':root[data-theme=dark] .chip[data-s="%s"]{color:%s;background:%s;border-color:%s}' % (k, v[2], v[3], v[2]) for k, v in CHIPS.items())


JS = r"""
(function(){var d=document,r=d.documentElement;r.classList.add('js');
function all(o){d.querySelectorAll('details').forEach(function(x){x.open=o})}
d.addEventListener('click',function(e){var t=e.target;if(!t.closest)return;
var b=t.closest('[data-act]');if(!b)return;var a=b.getAttribute('data-act');
if(a==='expand')all(true);else if(a==='collapse')all(false);
else if(a==='theme'){var c=r.getAttribute('data-theme');var dark=c?c==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;r.setAttribute('data-theme',dark?'light':'dark');try{localStorage.setItem('theme',dark?'light':'dark')}catch(x){}}
else if(a==='copy'){var p=b.closest('details,div').querySelector('pre');if(p&&navigator.clipboard){navigator.clipboard.writeText(p.innerText);b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1500)}}});
try{var s=localStorage.getItem('theme');if(s)r.setAttribute('data-theme',s)}catch(x){}
function openTo(){var h=location.hash.slice(1);if(!h)return;var e=d.getElementById(h);while(e){if(e.tagName==='DETAILS')e.open=true;e=e.parentElement}var t=d.getElementById(h);if(t)t.scrollIntoView()}
window.addEventListener('hashchange',openTo);openTo();
var st=[];window.addEventListener('beforeprint',function(){st=[];d.querySelectorAll('details').forEach(function(x){st.push(x.open);x.open=true})});
window.addEventListener('afterprint',function(){d.querySelectorAll('details').forEach(function(x,i){x.open=st[i]})});
})();
"""
