#!/usr/bin/env python3
"""Hand-authored SVG diagrams for the ROGII top-kernel report.
Coordinates are computed; the vector diagram design is bespoke (not chart output).
Palette matches the dataviz reference (light surface)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
SURFACE = "#fcfcfb"; INK = "#0b0b0b"; SUB = "#52514e"
BLUE = "#2a78d6"; AQUA = "#1baf7a"; YELLOW = "#eda100"; VIOLET = "#4a3aa7"
RED = "#e34948"; ORANGE = "#eb6834"; MAGENTA = "#e87ba4"; GREEN = "#0ca30c"
CARD = "#ffffff"; STROKE = "#d7d6d1"

# ----------------------------------------------------------------------
# SVG 1 — dependency web: featured kernels (left) → shared datasets (right)
# ----------------------------------------------------------------------
def dependency_web():
    W, H = 1000, 700
    kx, dx = 250, 720          # right edge of kernel cards / left edge of dataset cards
    kw, dw = 200, 250
    top, gap = 132, 62
    kernels = [
        ("cdeotte / xgb-starter-cv-15", "starter · no data deps", []),
        ("nihilisticneuralnet / DWT-based", "645 votes", ["art"]),
        ("ravaghi / …-ridge", "260 votes", ["art"]),
        ("pixiux / dual-pipeline-blend", "229 votes", ["kool", "claude", "art"]),
        ("lightningv08 / …-self-verifying", "281 v · FORK of pixiux v3", ["kool", "claude", "art"]),
        ("bernubritz / LB7295-rebuild", "442 votes", ["kool", "claude", "art"]),
        ("pilkwang / target-free-geosteering", "213 v · 42 versions", ["pmodel", "claude", "art"]),
        ("degnonguidi / public-score-7.159", "200 v · 18 versions", ["kool", "nina", "v10", "claude", "tab", "art"]),
    ]
    datasets = {
        "art":   ("ravaghi / …-artifacts", "v6 · 2.36 GB", BLUE, True),
        "claude":("fleongg / rogii-claude-models-pub", "v1 · 0.01 GB", AQUA, False),
        "kool":  ("phongnguyn23021656 / koolbox-offline", "v1 · offline pip", VIOLET, False),
        "pmodel":("pilkwang / rogii-model-package", "v9 · 0.22 GB", ORANGE, False),
        "nina":  ("nina2025 / rogii-03", "v5", SUB, False),
        "v10":   ("thbdh5765 / rogii-v10-fresh-artifacts", "v1 · 0.41 GB", SUB, False),
        "tab":   ("needless090 / rogii-tabicl-mirror", "v1 · 0.11 GB", SUB, False),
    }
    dorder = ["art", "claude", "kool", "pmodel", "nina", "v10", "tab"]
    ky = {i: top + i * gap for i in range(len(kernels))}
    dy = {k: top + i * gap for i, k in enumerate(dorder)}

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>')
    s.append(f'<text x="40" y="42" font-size="21" font-weight="700" fill="{INK}">'
             f'Featured-kernel dependency web</text>')
    s.append(f'<text x="40" y="64" font-size="12.5" fill="{SUB}">'
             f'Data sources each kernel attaches (version = the dataset&#8217;s current version, fetched 2026-07-03).</text>')
    s.append(f'<text x="40" y="80" font-size="12.5" fill="{SUB}">'
             f'Sources attach unpinned &#8212; they resolve to the dataset&#8217;s latest version at run time.</text>')
    s.append(f'<text x="{kx-kw}" y="112" font-size="11.5" font-weight="700" fill="{SUB}">KERNELS</text>')
    s.append(f'<text x="{dx}" y="112" font-size="11.5" font-weight="700" fill="{SUB}">SHARED DATA SOURCES</text>')

    # edges first (under nodes)
    for i, (_, _, deps) in enumerate(kernels):
        y0 = ky[i]
        for dk in deps:
            y1 = dy[dk]
            x0, x1 = kx, dx
            hub = datasets[dk][3]
            col = BLUE if hub else "#cfcec9"
            wdt = 2.2 if hub else 1.1
            op = 0.85 if hub else 0.9
            cxx = (x0 + x1) / 2
            s.append(f'<path d="M{x0},{y0} C{cxx},{y0} {cxx},{y1} {x1},{y1}" '
                     f'fill="none" stroke="{col}" stroke-width="{wdt}" opacity="{op}"/>')
    # fork edge (kernel -> kernel): pixiux(3) -> lightningv08(4)
    yA, yB = ky[3], ky[4]
    s.append(f'<path d="M{kx-kw-6},{yA} C{kx-kw-70},{yA} {kx-kw-70},{yB} {kx-kw-6},{yB}" '
             f'fill="none" stroke="{RED}" stroke-width="2.2" stroke-dasharray="6 4" '
             f'marker-end="url(#ar)"/>')
    s.append(f'<text x="{kx-kw-78}" y="{(yA+yB)/2+4}" font-size="11" fill="{RED}" '
             f'text-anchor="end" font-weight="700">fork</text>')
    s.append(f'<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="3" '
             f'orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{RED}"/></marker></defs>')

    # kernel nodes
    for i, (name, sub, _) in enumerate(kernels):
        y = ky[i]
        s.append(f'<rect x="{kx-kw}" y="{y-19}" width="{kw}" height="38" rx="7" '
                 f'fill="{CARD}" stroke="{STROKE}"/>')
        s.append(f'<circle cx="{kx}" cy="{y}" r="4.5" fill="{INK}"/>')
        s.append(f'<text x="{kx-kw+12}" y="{y-3}" font-size="11.3" font-weight="700" fill="{INK}">{name}</text>')
        s.append(f'<text x="{kx-kw+12}" y="{y+12}" font-size="10" fill="{SUB}">{sub}</text>')
    # dataset nodes
    for dk in dorder:
        name, sub, col, hub = datasets[dk]
        y = dy[dk]
        fill = "#eaf2fd" if hub else CARD
        s.append(f'<rect x="{dx}" y="{y-19}" width="{dw}" height="38" rx="7" '
                 f'fill="{fill}" stroke="{col if hub else STROKE}" stroke-width="{2 if hub else 1}"/>')
        s.append(f'<circle cx="{dx}" cy="{y}" r="4.5" fill="{col}"/>')
        s.append(f'<text x="{dx+14}" y="{y-3}" font-size="11" font-weight="700" fill="{INK}">{name}</text>')
        s.append(f'<text x="{dx+14}" y="{y+12}" font-size="10" fill="{SUB}">{sub}</text>')

    # hub callout
    s.append(f'<text x="40" y="{H-38}" font-size="12.5" fill="{BLUE}" font-weight="700">'
             f'ravaghi/&#8230;-artifacts (v6) is the shared backbone &#8212; 7 of 8 featured kernels load it.</text>')
    s.append(f'<text x="40" y="{H-18}" font-size="11.5" fill="{SUB}">'
             f'Blue edges = the hub dataset &#160;&#183;&#160; gray edges = other shared sources &#160;&#183;&#160; '
             f'red dashed = a code fork (identical bytes).</text>')
    s.append('</svg>')
    (OUT / "dependency_web.svg").write_text("\n".join(s))
    print("wrote dependency_web.svg")


# ----------------------------------------------------------------------
# SVG 2 — how we tell a real edit from an identical rerun
# ----------------------------------------------------------------------
def diff_method():
    W, H = 1000, 470
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>')
    s.append(f'<text x="40" y="42" font-size="21" font-weight="700" fill="{INK}">'
             f'Telling a real edit from an identical rerun</text>')
    s.append(f'<text x="40" y="66" font-size="13.5" fill="{SUB}">'
             f'Kaggle keeps every notebook version but never shows a diff. This is the pipeline behind '
             f'every &#8220;identical / changed&#8221; label in this report.</text>')

    steps = [
        ("1  Pull each version", "kernel_archive.py\n--version N", BLUE),
        ("2  Keep code only", "drop outputs &amp;\nexecution counts", AQUA),
        ("3  Normalize", "strip trailing ws,\nblank lines", VIOLET),
        ("4  Hash + diff", "SHA-256 &amp;\nunified diff", ORANGE),
    ]
    n = len(steps); bw, bh = 190, 88; y0 = 128
    gapx = (W - 80 - n * bw) / (n - 1)
    xs = [40 + i * (bw + gapx) for i in range(n)]
    s.append(f'<defs><marker id="a2" markerWidth="10" markerHeight="10" refX="7" refY="3" '
             f'orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{SUB}"/></marker></defs>')
    for i, (t, d, col) in enumerate(steps):
        x = xs[i]
        s.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="10" '
                 f'fill="{CARD}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<rect x="{x}" y="{y0}" width="6" height="{bh}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{x+20}" y="{y0+28}" font-size="13.5" font-weight="700" fill="{INK}">{t}</text>')
        for j, line in enumerate(d.split("\n")):
            s.append(f'<text x="{x+20}" y="{y0+50+j*17}" font-size="11.5" '
                     f'fill="{SUB}" font-family="monospace">{line}</text>')
        if i < n - 1:
            xa = x + bw; xb = xs[i + 1]
            s.append(f'<line x1="{xa+4}" y1="{y0+bh/2}" x2="{xb-6}" y2="{y0+bh/2}" '
                     f'stroke="{SUB}" stroke-width="2" marker-end="url(#a2)"/>')

    # two outcome branches
    by = 300
    ax = xs[-1] + bw / 2
    # identical branch
    s.append(f'<line x1="{ax}" y1="{y0+bh}" x2="{ax}" y2="{by-6}" stroke="{SUB}" stroke-width="2"/>')
    ox1, ox2 = 250, 660
    s.append(f'<rect x="{ox1}" y="{by}" width="300" height="92" rx="10" fill="#fdeef4" stroke="{MAGENTA}" stroke-width="2"/>')
    s.append(f'<text x="{ox1+18}" y="{by+27}" font-size="13.5" font-weight="700" fill="{INK}">same hash  =  IDENTICAL rerun</text>')
    s.append(f'<text x="{ox1+18}" y="{by+50}" font-size="11.5" fill="{SUB}">score change is pure run-to-run</text>')
    s.append(f'<text x="{ox1+18}" y="{by+68}" font-size="11.5" fill="{SUB}">noise &#8212; e.g. DWT 4 versions, one hash,</text>')
    s.append(f'<text x="{ox1+18}" y="{by+86}" font-size="11.5" fill="{RED}" font-weight="700">LB 9.251 to 9.632 (0.38 spread)</text>')

    s.append(f'<rect x="{ox2}" y="{by}" width="300" height="92" rx="10" fill="#eaf2fd" stroke="{BLUE}" stroke-width="2"/>')
    s.append(f'<text x="{ox2+18}" y="{by+27}" font-size="13.5" font-weight="700" fill="{INK}">diff &gt; 0  =  real CHANGE</text>')
    s.append(f'<text x="{ox2+18}" y="{by+50}" font-size="11.5" fill="{SUB}">count added / removed lines,</text>')
    s.append(f'<text x="{ox2+18}" y="{by+68}" font-size="11.5" fill="{SUB}">read the actual edit &#8212; e.g. XGB&#8217;s</text>')
    s.append(f'<text x="{ox2+18}" y="{by+86}" font-size="11.5" fill="{BLUE}" font-weight="700">4-line baseline swap: 19.05 to 14.34</text>')

    # fork the vertical connector into the two boxes
    s.append(f'<path d="M{ax},{by-6} L{ox1+150},{by-6}" stroke="{MAGENTA}" stroke-width="2" fill="none"/>')
    s.append(f'<path d="M{ax},{by-6} L{ox2+150},{by-6}" stroke="{BLUE}" stroke-width="2" fill="none"/>')
    s.append(f'<line x1="{ox1+150}" y1="{by-6}" x2="{ox1+150}" y2="{by}" stroke="{MAGENTA}" stroke-width="2" marker-end="url(#a2)"/>')
    s.append(f'<line x1="{ox2+150}" y1="{by-6}" x2="{ox2+150}" y2="{by}" stroke="{BLUE}" stroke-width="2" marker-end="url(#a2)"/>')
    s.append('</svg>')
    (OUT / "diff_method.svg").write_text("\n".join(s))
    print("wrote diff_method.svg")


if __name__ == "__main__":
    dependency_web()
    diff_method()
