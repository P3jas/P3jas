# P3jas profile panels — edit the content block and re-run: python3 gen4.py
import os
OUT = "/home/claude/profile/assets"; os.makedirs(OUT, exist_ok=True)

# ─────────────── content ───────────────
NAME     = "developer & artist"
SYNOPSIS = ["--code", "--draw", "--learn"]
DESC     = ["Builds small things for the web",
            "and the terminal. Draws when the",
            "code doesn't compile."]
STACK    = ["python", "javascript", "typescript", "html/css", "react", "node.js", "git", "linux"]
NOW      = [("building", "something new"), ("learning", "one thing at a time"), ("drawing", "@pejas_rysuje")]
PROJECTS = [("projekt-1", "krótki opis projektu", "python"),
            ("projekt-2", "krótki opis projektu", "javascript"),
            ("projekt-3", "krótki opis projektu", "typescript"),
            ("projekt-4", "krótki opis projektu", "python")]
LINKS    = [("gh", "P3jas"), ("x", "@Dardewilll"), ("ig", "@pejas_rysuje")]
# ───────────────────────────────────────

FONT = 'ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,Consolas,"Liberation Mono",monospace'
CSS = (f'<style>text{{font-family:{FONT};font-size:14px;fill:#d4d4d4}}'
       '.h{fill:#fff;font-weight:700}.d{fill:#6a6a6a}.inv{fill:#0a0a0a;font-weight:700;font-size:12px;letter-spacing:2px}'
       '.c{animation:b 1.1s steps(1) infinite}@keyframes b{50%{opacity:0}}'
       '@media (prefers-reduced-motion:reduce){.c{animation:none}}</style>')
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
class S:
    def __init__(s, w, h, label):
        s.w, s.h = w, h
        s.o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">', CSS,
               f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="#0a0a0a" stroke="#2a2a2a"/>']
    def t(s, x, y, txt, c="", a="start", size=None):
        st = f' style="font-size:{size}px"' if size else ""
        s.o.append(f'<text x="{x}" y="{y}" class="{c}" text-anchor="{a}" xml:space="preserve"{st}>{txt}</text>')
    def tag(s, x, y, label):          # inverted retro label
        w = len(label)*9.6+18
        s.o.append(f'<rect x="{x}" y="{y-15}" width="{w}" height="21" fill="#fff"/>')
        s.t(x+9, y, esc(label), "inv")
    def dots(s, x1, x2, y):
        s.o.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#3a3a3a" stroke-dasharray="1 5" stroke-linecap="round" stroke-width="1.5"/>')
    def crops(s, m=12, l=10):
        for x, y, dx, dy in [(m, m, 1, 1), (s.w-m, m, -1, 1), (m, s.h-m, 1, -1), (s.w-m, s.h-m, -1, -1)]:
            s.o.append(f'<path d="M{x} {y+dy*l}V{y}H{x+dx*l}" fill="none" stroke="#4a4a4a"/>')
    def moon(s, cx, cy, r, step=4.2):
        import math
        lx, ly, lz = -0.62, -0.45, 0.64
        n = int(r/step)+1
        for j in range(-n, n+1):
            for i in range(-n, n+1):
                x, y = i*step, j*step
                if x*x+y*y > r*r: continue
                nx, ny = x/r, y/r; nz = math.sqrt(max(0, 1-nx*nx-ny*ny))
                L = max(0, nx*lx+ny*ly+nz*lz)
                # craters
                for (ccx, ccy, cr) in [(-.3, -.2, .22), (.25, .3, .16), (-.05, .45, .1), (.35, -.35, .12)]:
                    if (nx-ccx)**2+(ny-ccy)**2 < cr*cr: L *= .55
                if L < .06: continue
                s.o.append(f'<circle cx="{cx+x:.1f}" cy="{cy+y:.1f}" r="{.35+L*1.15:.2f}" fill="#fff" opacity="{min(.9,.15+L*.8):.2f}"/>')
    def icon(s, path, x, y, size, fill="#fff"):
        k = size/24
        s.o.append(f'<path transform="translate({x} {y}) scale({k})" d="{path}" fill="{fill}"/>')
    def save(s, name): open(os.path.join(OUT, name), "w").write("\n".join(s.o + ["</svg>"]))

# ═══════════ man page panel ═══════════
m = S(1000, 360, "pejas(1)")
m.t(28, 36, "PEJAS(1)", "d", size=12); m.t(500, 36, "General Commands Manual", "d", "middle", 12); m.t(972, 36, "PEJAS(1)", "d", "end", 12)
m.o.append('<line x1="0" y1="54" x2="1000" y2="54" stroke="#1e1e1e"/>')
# hero row
m.t(36, 104, "pejas", "h", size=34)
m.t(160, 104, f'<tspan class="d">—</tspan> {esc(NAME)}', size=17)
syn = '<tspan class="d">$</tspan> <tspan class="h">pejas</tspan> ' + " ".join(
    f'<tspan class="d">[</tspan><tspan text-decoration="underline">{esc(a)}</tspan><tspan class="d">]</tspan>' for a in SYNOPSIS) \
    + ' <tspan text-decoration="underline">&lt;idea&gt;</tspan>'
m.t(36, 136, syn)
m.dots(36, 680, 166)
# moon + orbit decoration
m.o.append('<g transform="rotate(-14 852 180)"><ellipse cx="852" cy="180" rx="112" ry="22" fill="none" stroke="#fff" stroke-opacity=".25" stroke-dasharray="2 5"/><circle cx="744" cy="186" r="3.2" fill="#fff"/></g>')
m.moon(852, 180, 64, 4.6)
m.t(852, 280, "fig. 1 — the moon, mostly", "d", "middle", 11)
m.crops()
# three columns
cols = [36, 0, 400]
for x, lab in [(36, "DESCRIPTION"), (400, "NOW")]: m.tag(x, 206, lab)
for i, ln in enumerate(DESC): m.t(cols[0], 242+i*24, esc(ln))
for i, (k, v) in enumerate(NOW):
    y = 242+i*24
    m.t(cols[2], y, esc(k), "d"); m.t(cols[2]+100, y, esc(v))
m.o.append('<line x1="0" y1="318" x2="1000" y2="318" stroke="#1e1e1e"/>')
m.t(28, 344, "since 2025", "d", size=12)
m.t(500, 344, '~/p3jas <tspan class="c" fill="#fff">█</tspan>', "d", "middle", 12)
m.t(972, 344, "nothing escapes", "d", "end", 12)
m.save("man.svg")

# ═══════════ stack panel ═══════════
import json
ICONS = json.load(open("/home/claude/icons/paths.json"))
STACK_ICONS = [("python","python"),("javascript","javascript"),("typescript","typescript"),("html / css","html"),
               ("react","react"),("node.js","node"),("git","git"),("linux","linux")]
st = S(1000, 236, "stack")
st.tag(36, 46, "STACK")
st.t(964, 46, "~/stack · apt list --installed", "d", "end", 12)
n = len(STACK_ICONS); tw = 104; gap = (928 - n*tw)/(n-1)
for i, (label, key) in enumerate(STACK_ICONS):
    x = 36 + i*(tw+gap); y = 72
    st.o.append(f'<rect x="{x:.1f}" y="{y}" width="{tw}" height="112" rx="6" fill="#111" stroke="#2a2a2a"/>')
    st.o.append(f'<rect x="{x+1:.1f}" y="{y+1}" width="{tw-2}" height="3" rx="1" fill="#fff" opacity=".08"/>')
    st.t(x+10, y+20, f"{i+1:02d}", "d", size=10)
    st.icon(ICONS[key], x+tw/2-16, y+30, 32)
    st.t(x+tw/2, y+96, esc(label), "", "middle", 12.5)
bar = "".join("█" for _ in range(n))
st.t(36, 214, f'<tspan class="d">[</tspan>{bar}<tspan class="d">]</tspan>  <tspan class="d">{n} packages installed · 0 broken · always learning</tspan>', size=12)
st.crops()
st.save("stack.svg")

# ═══════════ project rows (clickable, 2 per line) ═══════════
for i, (name, desc, lang) in enumerate(PROJECTS, 1):
    p = S(492, 78, f"project {name}")
    p.o.append(f'<rect x="16" y="20" width="38" height="38" fill="#fff"/>')
    p.t(35, 45, f"{i:02d}", "inv", "middle", 14)
    p.t(72, 36, esc(name), "h", size=16)
    p.t(72, 59, esc(desc), "d", size=13)
    p.t(470, 36, "↗", "d", "end", 16)
    p.t(470, 59, esc(lang), "", "end", 12)
    p.save(f"p{i}.svg")

# ═══════════ link chips (with icons) ═══════════
LINKS = [("gh", "P3jas"), ("x", "@Dardewilll"), ("ig", "@pejas_rysuje")]
for k, v in LINKS:
    w = round(54 + len(v)*8.4 + 22)
    c = S(w, 44, f"{k} {v}")
    c.o.append('<rect x="6" y="6" width="32" height="32" rx="3" fill="#fff"/>')
    c.icon(ICONS[k], 13, 13, 18, "#0a0a0a")
    c.t(52, 27, esc(v), size=13.5)
    c.save(f"l-{k}.svg")

# ═══════════ greeting strip ═══════════
g = S(1000, 64, "hi, i'm pejas")
g.t(28, 39, '<tspan class="h">o/</tspan>', size=18)
g.t(70, 39, '<tspan class="h">hi, i\'m pejas.</tspan> <tspan class="d">welcome to my little corner of the void — make yourself at home.</tspan>', size=15)
g.t(972, 39, '<tspan class="c" fill="#fff">█</tspan>', "", "end", 15)
g.save("hello.svg")
print("ok")
