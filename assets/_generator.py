import math, random, os
random.seed(11)
OUT = "/home/claude/profile/assets"
os.makedirs(OUT, exist_ok=True)

# ───────────────────────── editable content ─────────────────────────
ABOUT = [
    ("user",     "pejas  ·  P3jas"),
    ("role",     "developer  /  artist"),
    ("focus",    "web · tools · small experiments"),
    ("learning", "something new every week"),
    ("draws",    "@pejas_rysuje"),
    ("uptime",   "since 2025"),
]
STACK = [  # (name, category, level 0-10)
    ("Python", "lang", 7), ("JavaScript", "lang", 7), ("TypeScript", "lang", 5), ("HTML / CSS", "web", 8),
    ("React", "web", 5), ("Node.js", "runtime", 5), ("Git", "tool", 7), ("Linux", "os", 6),
]
PROJECTS = [  # (name, description, language, tag)
    ("projekt-1", "Krótki opis projektu — co robi i dlaczego jest fajny.", "Python", "tool"),
    ("projekt-2", "Krótki opis projektu — co robi i dlaczego jest fajny.", "JavaScript", "web"),
    ("projekt-3", "Krótki opis projektu — co robi i dlaczego jest fajny.", "TypeScript", "app"),
    ("projekt-4", "Krótki opis projektu — co robi i dlaczego jest fajny.", "Python", "lab"),
]
LINKS = [("gh", "P3jas"), ("x", "@Dardewilll"), ("ig", "@pejas_rysuje")]
# ────────────────────────────────────────────────────────────────────

FONT = 'ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,Consolas,"Liberation Mono",monospace'
BG, LINE, DIM, MID, HI = "#0a0a0a", "#262626", "#4a4a4a", "#8a8a8a", "#ffffff"
STYLE = f"""<style>
.m{{font-family:{FONT}}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
@keyframes pulse{{50%{{opacity:.25}}}}
.cur{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.scan{{animation:scan 6s linear infinite}}
@keyframes scan{{0%{{transform:translateX(-30%)}}100%{{transform:translateX(130%)}}}}
@media (prefers-reduced-motion:reduce){{.pulse,.cur,.scan{{animation:none}}}}
</style>"""

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            + STYLE + "\n".join(body) + "</svg>")
def t(x, y, s, size=12, fill=MID, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" class="m" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" xml:space="preserve" {extra}>{esc(s)}</text>'
def window(w, h, title, right=""):
    b = [f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{LINE}"/>',
         f'<line x1="0" y1="34" x2="{w}" y2="34" stroke="{LINE}"/>']
    for x in (20, 38, 56): b.append(f'<circle cx="{x}" cy="17" r="5" fill="none" stroke="#5a5a5a"/>')
    b.append(t(w/2, 21.5, title, 11.5, MID, anchor="middle"))
    if right: b.append(t(w-18, 21.5, right, 11, DIM, anchor="end"))
    return b
def dither(x0, y0, w, h, step=6, fn=None, fill="#fff"):
    """dot field whose opacity comes from fn(u,v) in 0..1 — the 'printed' texture"""
    out = []
    for j in range(int(h/step)):
        for i in range(int(w/step)):
            u, v = i*step/w, j*step/h
            o = fn(u, v)
            if o < 0.04: continue
            out.append(f'<circle cx="{x0+i*step+step/2:.1f}" cy="{y0+j*step+step/2:.1f}" r="{0.55+o*0.9:.2f}" fill="{fill}" opacity="{min(1,o):.2f}"/>')
    return out

# ── mini black hole (same physics as banner, smaller) ──
CH_SET = " .·:;-=+*x#%@"
TIER = ["#3a3a3a", "#6e6e6e", "#a8a8a8", "#dcdcdc", "#ffffff"]
def hole_rows(cols, rows, cw, chh, R0, a, b, phase=0):
    cx, cy = cols*cw/2, rows*chh/2
    res = []
    for r in range(rows):
        s = ""
        for c in range(cols):
            x, y = c*cw+cw/2, r*chh+chh/2
            dx, dy = x-cx, y-cy; d = math.hypot(dx, dy); ang = math.atan2(dy, dx)
            rho = math.hypot(dx/a, dy/b); rin = R0*1.35/a; disk = 0
            if rin < rho < 1:
                tt = (rho-rin)/(1-rin); disk = (1-tt)**1.6*1.25
                th = math.atan2(dy/b, dx/a); disk *= 0.72+0.28*math.sin(th*7+rho*26-phase); disk *= 1+0.45*(-dx/a)
            if d < R0: I = disk if dy >= 0 else 0
            else:
                halo = math.exp(-((d-R0*1.3)/(R0*0.3))**2)*(0.72+0.28*abs(math.sin(ang)))*(1+0.35*(-dx/d))
                ring = math.exp(-((d-R0*1.04)/(cw*0.7))**2)*1.1
                I = max(disk, halo*0.95, ring)+0.1*math.exp(-(d-R0)/(R0*1.4))
            I = max(0, min(0.999, I+(random.random()-.5)*0.04))
            s += CH_SET[int(I*len(CH_SET))]
        res.append(s)
    return res
def tiers(row):
    out = ""; cur = None; buf = ""
    for ch in row:
        tt = (min(4, int(CH_SET.index(ch)/len(CH_SET)*5.2)) if ch != " " else cur)
        tt = 0 if tt is None else tt
        if tt != cur and buf:
            out += f'<tspan fill="{TIER[cur]}">{esc(buf)}</tspan>'; buf = ""
        cur = tt; buf += ch
    if buf: out += f'<tspan fill="{TIER[cur]}">{esc(buf)}</tspan>'
    return out

# ═════════════ 1. section headers ═════════════
def header(num, name, path):
    W, H = 1000, 64
    b = [t(4, 40, num, 30, HI, 700, extra='letter-spacing="1"'),
         t(62, 40, "/", 30, "#333", 300),
         t(90, 39, name, 15, HI, 600, extra='letter-spacing="3"')]
    x0 = 100 + len(name)*11.5
    # dotted leader that fades out toward the right
    b += dither(x0, 28, 900-x0-len(path)*7.2, 12, 6, lambda u, v: (0.55*(1-u)**1.4+0.05) if abs(v-0.25) < 0.3 else 0)
    b.append(t(996, 39, path, 12, DIM, anchor="end"))
    b.append(f'<line x1="0" y1="{H-1}" x2="{W}" y2="{H-1}" stroke="#1c1c1c"/>')
    return svg(W, H, b, f"{num} {name}")

# ═════════════ 2. about (neofetch style) ═════════════
def about():
    W, H = 1000, 330
    b = window(W, H, "pejas@github: ~ — neofetch", "zsh")
    cw, chh = 6.2, 10.5; cols, rows = 52, 26
    hr = hole_rows(cols, rows, cw, chh, 42, 172, 22)
    for r, row in enumerate(hr):
        if row.strip(): b.append(f'<text x="34" y="{50+r*chh+8:.1f}" textLength="{cols*cw:.1f}" lengthAdjust="spacing" xml:space="preserve" class="m" font-size="10.5">{tiers(row)}</text>')
    X = 420; y = 78
    b.append(t(X, y, "pejas", 22, HI, 700, extra='letter-spacing="1"'))
    b.append(t(X+78, y, "@github", 22, "#5a5a5a", 400))
    y += 14
    b += dither(X, y, 520, 6, 4, lambda u, v: 0.6*(1-u)+0.08)
    y += 30
    for k, v in ABOUT:
        b.append(t(X, y, k, 13, "#6a6a6a"))
        b += dither(X+len(k)*7.9+8, y-6, 120-len(k)*7.9-14, 4, 4, lambda u, v: 0.22)
        b.append(t(X+128, y, v, 13, "#e6e6e6"))
        y += 25
    # status line with pulse
    b.append(t(X, y, "status", 13, "#6a6a6a"))
    b += dither(X+56, y-6, 58, 4, 4, lambda u, v: 0.22)
    b.append(f'<circle cx="{X+133}" cy="{y-4.5}" r="4" fill="{HI}" class="pulse"/>')
    b.append(t(X+146, y, "building things in the dark", 13, HI))
    y += 32
    # mono palette blocks (neofetch colors, in grayscale)
    for i, c in enumerate(["#141414", "#262626", "#3a3a3a", "#585858", "#7a7a7a", "#a0a0a0", "#c8c8c8", "#ffffff"]):
        b.append(f'<rect x="{X+i*30}" y="{y-12}" width="26" height="14" rx="2" fill="{c}" stroke="{LINE}"/>')
    return svg(W, H, b, "about pejas")

# ═════════════ 3. stack grid ═════════════
def stack():
    cols = 4; tw, th, gap = 229, 86, 15
    rows = math.ceil(len(STACK)/cols)
    W, H = 1000, 54+rows*(th+gap)+12
    b = window(W, H, "~/stack — ls -la", f"{len(STACK)} items")
    for i, (name, cat, lvl) in enumerate(STACK):
        x = 12+(i % cols)*(tw+gap); y = 50+(i//cols)*(th+gap)
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="6" fill="#0e0e0e" stroke="{LINE}"/>')
        # corner dither texture
        b += dither(x+tw-70, y+6, 64, 40, 5, lambda u, v: max(0, (u+(1-v))/2-0.35)*0.9)
        b.append(t(x+14, y+22, f"{i+1:02d}", 10, DIM))
        b.append(t(x+38, y+22, cat.upper(), 10, "#5a5a5a", extra='letter-spacing="2"'))
        b.append(t(x+14, y+50, name, 17, HI, 600))
        # level bar made of blocks
        for k in range(10):
            on = k < lvl
            b.append(f'<rect x="{x+14+k*13}" y="{y+64}" width="9" height="8" rx="1" fill="{HI if on else "#1f1f1f"}" opacity="{(0.35+0.065*k) if on else 1:.2f}"/>')
        b.append(t(x+tw-14, y+72, f"{lvl*10}%", 10, DIM, anchor="end"))
    return svg(W, H, b, "tech stack")

# ═════════════ 4. project cards ═════════════
def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur)+len(w)+1 > n: lines.append(cur); cur = w
        else: cur = (cur+" "+w).strip()
    lines.append(cur); return lines
def project(i, name, desc, lang, tag):
    W, H = 490, 210
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{LINE}"/>']
    # header band: dithered gradient + orbit
    seed = i*1.7
    b += dither(1, 1, W-2, 78, 6, lambda u, v: max(0, 0.75*math.exp(-((u-0.78)**2/0.03+(v-0.5)**2/0.5))+0.18*(1-v)*0.5*(1+math.sin(u*9+seed))))
    b.append(f'<ellipse cx="{W*0.78}" cy="40" rx="62" ry="9" fill="none" stroke="#fff" stroke-opacity=".35" stroke-dasharray="2 4"/>')
    b.append(f'<circle cx="{W*0.78}" cy="40" r="14" fill="{BG}" stroke="#fff" stroke-opacity=".8"/>')
    b.append(f'<line x1="0" y1="80" x2="{W}" y2="80" stroke="{LINE}"/>')
    b.append(t(20, 32, f"{i:02d}", 26, HI, 700))
    b.append(t(20, 56, f"repo://{tag}", 11, MID, extra='letter-spacing="1"'))
    b.append(t(20, 114, name, 20, HI, 600))
    b.append(t(W-20, 114, "↗", 18, MID, anchor="end"))
    for k, ln in enumerate(wrap(desc, 56)[:2]):
        b.append(t(20, 142+k*19, ln, 12.5, "#a8a8a8"))
    b.append(f'<line x1="20" y1="{H-38}" x2="{W-20}" y2="{H-38}" stroke="#1c1c1c"/>')
    b.append(f'<circle cx="25" cy="{H-19}" r="4" fill="{HI}"/>')
    b.append(t(36, H-15, lang, 11.5, "#bdbdbd"))
    b.append(t(W-20, H-15, f"[ {tag} ]", 11.5, DIM, anchor="end"))
    return svg(W, H, b, f"project {name}")

# ═════════════ 5. link pills ═════════════
def pill(key, label):
    w = 64+len(label)*8.2; h = 36
    b = [f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{BG}" stroke="#333"/>',
         f'<circle cx="18" cy="18" r="3.5" fill="{HI}" class="pulse"/>',
         t(30, 22.5, key, 11, DIM, extra='letter-spacing="1"'),
         t(30+len(key)*7+10, 22.5, label, 12.5, HI)]
    return svg(round(w), h, b, f"{key} {label}")

# ═════════════ 6. footer / event horizon ═════════════
def footer():
    W, H = 1000, 170
    b = []
    # curved horizon: a huge circle's top edge rendered as dots
    R = 1600; cx, cy = W/2, 120+R
    def f(u, v):
        x, y = u*W, v*H; d = math.hypot(x-cx, y-cy)
        g = math.exp(-((d-R)/9)**2)*0.95 + max(0, math.exp(-(R-d)/60)*0.35 if d < R else 0)
        return g*(0.35+0.65*math.exp(-((u-0.5)**2)/0.08))
    b += dither(0, 0, W, H, 5, f)
    b.append(f'<g class="scan"><rect x="0" y="0" width="160" height="{H}" fill="url(#g)"/></g>')
    b.insert(0, f'<defs><linearGradient id="g"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>')
    b.append(t(W/2, 70, "EOF", 13, HI, 700, "middle", 'letter-spacing="8"'))
    b.append(f'<text x="{W/2}" y="94" class="m" font-size="11.5" fill="#6a6a6a" text-anchor="middle" xml:space="preserve">thanks for falling in  ·  nothing escapes <tspan class="cur" fill="{HI}">▍</tspan></text>')
    return svg(W, H, b, "end of file")

files = {
    "h-about.svg": header("01", "ABOUT", "~/about.txt"),
    "h-stack.svg": header("02", "STACK", "~/stack"),
    "h-projects.svg": header("03", "PROJECTS", "~/projects --pinned"),
    "h-stats.svg": header("04", "SIGNAL", "~/stats --live"),
    "about.svg": about(), "stack.svg": stack(), "footer.svg": footer(),
}
for i, p in enumerate(PROJECTS, 1): files[f"project-{i}.svg"] = project(i, *p)
for k, l in LINKS: files[f"link-{k}.svg"] = pill(k, l)
for n, s in files.items(): open(os.path.join(OUT, n), "w").write(s)
print(sorted(files))
