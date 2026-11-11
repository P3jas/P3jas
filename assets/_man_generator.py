# man-page style info panel for the P3jas profile — edit the text below and re-run
NAME     = "pejas — developer & artist"
SYNOPSIS = ["pejas", "[--code]", "[--draw]", "[--learn]", "<idea>"]
DESC     = ["Builds small things for the web and the terminal.",
            "Draws when the code doesn't compile.",
            "Prefers dark rooms, monospace and black holes."]
STACK    = ["python · javascript · typescript",
            "html/css · react · node.js",
            "git · linux"]
NOW      = ["working on: something new",
            "learning:   one thing at a time"]

FONT = 'ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,Consolas,"Liberation Mono",monospace'
W, H = 1000, 312
L, R = 40, 560          # column x
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="pejas(1) manual page">',
     f'<style>text{{font-family:{FONT};font-size:13px;fill:#9a9a9a}}.h{{fill:#fff;font-weight:700;letter-spacing:1px}}'
     '.w{fill:#e6e6e6}.d{fill:#4a4a4a}.c{animation:b 1.1s steps(1) infinite}@keyframes b{50%{opacity:0}}'
     '@media (prefers-reduced-motion:reduce){.c{animation:none}}</style>',
     f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="#0a0a0a" stroke="#262626"/>']
T = lambda x, y, s, c="", a="start": o.append(f'<text x="{x}" y="{y}" class="{c}" text-anchor="{a}" xml:space="preserve">{s}</text>')

# man header
T(L-16, 34, "PEJAS(1)", "w"); T(W/2, 34, "General Commands Manual", "d", "middle"); T(W-24, 34, "PEJAS(1)", "w", "end")

def section(x, y, title, lines, cls="w"):
    T(x, y, title, "h"); y += 22
    for ln in lines: T(x+28, y, ln, cls); y += 20
    return y + 14

y = section(L, 74, "NAME", [esc(NAME).replace("pejas", '<tspan class="h">pejas</tspan>', 1)])
syn = f'<tspan class="h">{SYNOPSIS[0]}</tspan> ' + " ".join(
    f'<tspan class="d">[</tspan><tspan class="w" text-decoration="underline">{esc(a[1:-1])}</tspan><tspan class="d">]</tspan>'
    if a.startswith("[") else f'<tspan class="w" text-decoration="underline">{esc(a)}</tspan>' for a in SYNOPSIS[1:])
y = section(L, y, "SYNOPSIS", [syn])
section(L, y, "DESCRIPTION", [esc(d) for d in DESC], "")

y = section(R, 74, "STACK", [esc(s).replace(" · ", ' <tspan class="d">·</tspan> ') for s in STACK])
section(R, y, "NOW", [f'<tspan class="d">→</tspan> {esc(n)}' for n in NOW])

# footer
o.append(f'<line x1="24" y1="{H-46}" x2="{W-24}" y2="{H-46}" stroke="#1e1e1e"/>')
T(L-16, H-20, "since 2025", "d"); T(W/2, H-20, '~/p3jas <tspan class="c" fill="#fff">▍</tspan>', "d", "middle"); T(W-24, H-20, "PEJAS(1)", "d", "end")
o.append("</svg>")
open("/home/claude/profile/assets/man.svg", "w").write("\n".join(o))
