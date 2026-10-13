"""Build the profile's self-contained SVG artwork. No network or dependencies."""

import base64
import html
import json
import math
import random
import textwrap
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MINT = "#2effbf"
LAVENDER = "#b9a7ff"
CSS = """
text{font-family:Arial,Helvetica,sans-serif;fill:#f4f7fb}
.mono{font-family:'Courier New',monospace}
.muted{fill:#aab3c0}.soft{fill:#7d8d9b}
.flow{stroke-dasharray:12 160;animation:flow 8s linear infinite}
.dash{stroke-dasharray:3 9;animation:dash 8s linear infinite}
.float{animation:float 8s ease-in-out infinite}
.breath{animation:breath 4s ease-in-out infinite}
.glint{animation:glint 4s ease-in-out infinite}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 24s linear infinite}
.signal{animation:signal 4s ease-in-out infinite}
@keyframes flow{to{stroke-dashoffset:-688}}
@keyframes dash{to{stroke-dashoffset:-96}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes breath{0%,100%{opacity:.3}50%{opacity:.8}}
@keyframes glint{0%,100%{opacity:.18}50%{opacity:.9}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes signal{0%,100%{opacity:.35}50%{opacity:1}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def text(x, y, value, size=16, color=None, **attrs):
    attributes = {"x": x, "y": y, "font-size": size, **attrs}
    if color:
        attributes["style"] = f"fill:{color}"
    return "<text " + " ".join(
        f'{key}="{html.escape(str(value), quote=True)}"'
        for key, value in attributes.items()
    ) + ">" + html.escape(value) + "</text>"


def svg(width, height, title, description, content, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
<title id="title">{html.escape(title)}</title>
<desc id="description">{html.escape(description)}</desc>
<defs>
<linearGradient id="surface" x2="1" y2="1"><stop stop-color="#07110f"/><stop offset=".55" stop-color="#080d16"/><stop offset="1" stop-color="#141126"/></linearGradient>
<linearGradient id="edge"><stop stop-color="{MINT}" stop-opacity=".65"/><stop offset=".55" stop-color="{LAVENDER}" stop-opacity=".15"/><stop offset="1" stop-color="{LAVENDER}" stop-opacity=".65"/></linearGradient>
<radialGradient id="mint-glow"><stop stop-color="{MINT}" stop-opacity=".18"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></radialGradient>
<radialGradient id="purple-glow"><stop stop-color="{LAVENDER}" stop-opacity=".18"/><stop offset="1" stop-color="{LAVENDER}" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
{defs}
</defs>
<style>{CSS}</style>
{content}
</svg>
'''


def save(path, content):
    ElementTree.fromstring(content)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def still(content):
    return content.replace("</style>", "*{animation:none!important}</style>")


def stars(width, height, count=65):
    rng = random.Random(13)
    return "".join(
        f'<circle class="glint" cx="{rng.uniform(18, width-18):.1f}" cy="{rng.uniform(18, height-18):.1f}" r="{rng.choice([.7, 1, 1.4]):.1f}" fill="{rng.choice([MINT, LAVENDER, "#d6e9e3"])}" style="animation-delay:-{rng.uniform(0, 4):.2f}s"/>'
        for _ in range(count)
    )


def chip(x, y, label, color=MINT, size=13):
    width = round(len(label) * size * .55 + 24)
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="30" rx="15" fill="{color}" fill-opacity=".06" stroke="{color}" stroke-opacity=".24"/>'
        + text(x + 12, y + 20, label, size, color)
    ), width


def banner(mobile=False):
    width, height = (640, 700) if mobile else (1200, 480)
    # The existing banner's portrait is displayed through a viewport, unchanged.
    original = base64.b64encode((ROOT / "top-banner.jpg").read_bytes()).decode()
    px, py, size = (168, 55, 304) if mobile else (795, 64, 346)
    cx, cy = px + size / 2, py + size / 2
    defs = f'''<radialGradient id="portrait-fade" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{size/2}"><stop offset=".67" stop-color="white"/><stop offset="1" stop-color="black"/></radialGradient>
<mask id="portrait-mask" maskUnits="userSpaceOnUse" x="{px}" y="{py}" width="{size}" height="{size}"><rect x="{px}" y="{py}" width="{size}" height="{size}" fill="url(#portrait-fade)"/></mask>'''
    parts = [
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="26" fill="url(#surface)" stroke="#233330"/>',
        f'<ellipse cx="{cx}" cy="{cy}" rx="250" ry="235" fill="url(#mint-glow)"/>',
        f'<ellipse cx="{width*.15}" cy="{height}" rx="{width*.6}" ry="200" fill="url(#purple-glow)"/>',
        stars(width, height),
    ]
    # A quiet perspective grid and wave traces connect the scene to scientific ML.
    grid_top = height - 90
    for i in range(13):
        end = i * width / 12
        start = width / 2 + (end - width / 2) * .30
        parts.append(f'<path d="M {start:.1f} {grid_top} L {end:.1f} {height-18}" stroke="{MINT}" stroke-opacity=".055"/>')
    for i in range(4):
        y = grid_top + i * i * 7
        parts.append(f'<path d="M 24 {y} H {width-24}" stroke="{MINT}" stroke-opacity=".065"/>')
    parts.extend([
        f'<ellipse cx="{cx}" cy="{cy}" rx="{size*.57}" ry="{size*.39}" transform="rotate(-23 {cx} {cy})" fill="none" stroke="{MINT}" stroke-opacity=".22"/>',
        f'<ellipse class="flow" cx="{cx}" cy="{cy}" rx="{size*.57}" ry="{size*.39}" transform="rotate(-23 {cx} {cy})" fill="none" stroke="{MINT}" stroke-opacity=".7" stroke-width="2"/>',
        f'<ellipse class="dash" cx="{cx}" cy="{cy}" rx="{size*.49}" ry="{size*.55}" fill="none" stroke="{LAVENDER}" stroke-opacity=".35"/>',
        f'<g mask="url(#portrait-mask)"><svg x="{px}" y="{py}" width="{size}" height="{size}" viewBox="260 125 1040 1040" overflow="hidden"><image href="data:image/jpeg;base64,{original}" width="4441" height="1200"/></svg></g>',
        f'<circle class="breath" cx="{cx+size*.43}" cy="{cy+size*.2}" r="6" fill="{MINT}" filter="url(#glow)"/>',
        f'<circle cx="{cx+size*.43}" cy="{cy+size*.2}" r="3" fill="{MINT}"/>',
    ])
    if mobile:
        parts.extend([
            text(320, 35, "RESEARCH / PRODUCTS / EDUCATION", 13, MINT, **{"text-anchor": "middle", "letter-spacing": 2, "class": "mono"}),
            text(320, 412, "Lakshay Chawla.", 54, **{"text-anchor": "middle", "font-weight": 700, "letter-spacing": -2}),
            text(320, 451, "Data Scientist / AI Researcher", 23, LAVENDER, **{"text-anchor": "middle"}),
            text(320, 558, "Useful, grounded, accessible AI.", 22, **{"text-anchor": "middle", "class": "muted"}),
            text(320, 623, "CLARITY LAB / IIT JODHPUR", 15, MINT, **{"text-anchor": "middle", "class": "mono"}),
            text(320, 651, "NEXTGENAISCHOOL", 15, LAVENDER, **{"text-anchor": "middle", "class": "mono", "letter-spacing": 2}),
        ])
        x, y = 128, 479
    else:
        parts.extend([
            text(56, 55, "RESEARCH / PRODUCTS / EDUCATION", 14, MINT, **{"letter-spacing": 2.4, "class": "mono"}),
            text(52, 157, "Lakshay", 86, **{"font-weight": 700, "letter-spacing": -3}),
            text(52, 243, "Chawla.", 86, **{"font-weight": 700, "letter-spacing": -3}),
            text(56, 289, "Data Scientist / AI Researcher", 24, LAVENDER),
            text(56, 391, "AI that is useful, grounded, and accessible.", 19, **{"class": "muted"}),
            text(56, 446, "CLARITY LAB / IIT JODHPUR", 12, MINT, **{"class": "mono", "letter-spacing": 1}),
            text(1144, 446, "NEXTGENAISCHOOL", 12, LAVENDER, **{"text-anchor": "end", "class": "mono", "letter-spacing": 1}),
        ])
        x, y = 56, 318
    for label in ["PINNs", "3D Vision", "Generative AI"]:
        markup, chip_width = chip(x, y, label, size=15)
        parts.append(markup)
        x += chip_width + 10
    return svg(width, height, "Lakshay Chawla", "The original illustrated avatar in a mint and lavender orbital starfield. Data scientist, AI researcher, entrepreneur, and educator working on PINNs, 3D vision, and generative AI.", "".join(parts), defs)


def node(x, y, color=MINT, radius=7, delay=0):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#0a171b" stroke="{color}" stroke-width="1.5"/><circle class="signal" cx="{x}" cy="{y}" r="{radius*.4}" fill="{color}" style="animation-delay:-{delay}s"/>'


def illustration(kind, color):
    parts = [f'<circle cx="0" cy="0" r="100" fill="url(#{"mint" if color==MINT else "purple"}-glow)"/>']
    if kind == "fren":
        parts.append(f'<g class="float"><rect x="-56" y="-48" width="112" height="82" rx="24" fill="#0b1920" stroke="{color}" stroke-width="2"/><path d="M -28 34 L -42 50 L -40 26" fill="#0b1920" stroke="{color}" stroke-width="2"/><path d="M 0 -48 V -62" stroke="{LAVENDER}" stroke-width="2"/><circle class="breath" cy="-66" r="4" fill="{LAVENDER}"/><rect x="-34" y="-25" width="18" height="18" rx="8" fill="{color}"/><rect x="16" y="-25" width="18" height="18" rx="8" fill="{color}"/><path d="M -17 10 Q 0 24 17 10" fill="none" stroke="{LAVENDER}" stroke-width="3"/></g>')
        parts.append(f'<ellipse class="dash" rx="93" ry="68" fill="none" stroke="{color}" stroke-opacity=".3"/>')
        for x, y, delay in [(-78, 44, 0), (82, -38, 1.2), (60, 60, 2.4)]:
            parts.append(node(x, y, LAVENDER, 8, delay))
    elif kind in {"pinnhub", "rlpinn"}:
        for row in range(7):
            points = []
            for col in range(31):
                x = -100 + col * 6.7 + row * 4
                y = -28 + row * 12 + 23 * math.sin(col * .20 + row * .30)
                points.append(f"{x:.1f},{y:.1f}")
            parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-opacity="{.18+row*.08:.2f}" stroke-width="1.2"/>')
            if row in (1, 4):
                parts.append(f'<polyline class="flow" points="{" ".join(points)}" fill="none" stroke="{MINT}" stroke-width="2" style="animation-delay:-{row}s"/>')
        if kind == "rlpinn":
            parts.append(f'<path class="dash" d="M -76 -45 Q 5 -114 88 -37" fill="none" stroke="{MINT}" stroke-width="2"/><path d="M 79 -39 L 88 -37 L 87 -47" fill="none" stroke="{MINT}" stroke-width="2"/>')
            for x, y, delay in [(-76, -45, 0), (0, -74, 1), (88, -37, 2)]:
                parts.append(node(x, y, MINT, 6, delay))
    elif kind == "artgridx":
        parts.append('<g class="float">')
        for x, y, w, h in [(-82, -64, 72, 78), (4, -64, 76, 52), (-82, 28, 72, 40), (4, 2, 76, 66)]:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#101926" stroke="{color}" stroke-opacity=".5"/>')
        parts.append(f'<circle class="breath" cx="-46" cy="-25" r="18" fill="{LAVENDER}"/><path d="M 17 -22 L 34 -45 L 63 -22 Z" fill="{MINT}" fill-opacity=".65"/><path d="M 18 50 Q 38 5 66 49" fill="none" stroke="{LAVENDER}" stroke-width="5"/><path d="M -67 47 H -27" stroke="{MINT}" stroke-width="4"/></g>')
    elif kind == "notifyme":
        parts.append(f'<g class="float"><path d="M -34 -5 V -24 A 34 34 0 0 1 34 -24 V -5 Q 34 12 47 22 H -47 Q -34 12 -34 -5 Z" fill="#13192a" stroke="{color}" stroke-width="2.5"/><path d="M -12 35 A 12 12 0 0 0 12 35" fill="none" stroke="{MINT}" stroke-width="3"/><circle class="signal" cx="29" cy="-42" r="8" fill="{MINT}"/><path class="breath" d="M -59 -42 Q -79 -7 -59 19 M 59 -42 Q 79 -7 59 19" fill="none" stroke="{color}" stroke-width="2"/></g>')
        parts.append(f'<ellipse class="dash" rx="98" ry="72" fill="none" stroke="{MINT}" stroke-opacity=".25"/>')
    elif kind == "host":
        parts.append(f'<g class="float"><path d="M -47 8 C -96 7 -92 -49 -49 -49 C -34 -89 29 -84 43 -43 C 93 -42 94 11 51 11 Z" fill="#0b1920" stroke="{color}" stroke-width="2"/><path d="M 0 53 V -27 M -17 -10 L 0 -27 L 17 -10" fill="none" stroke="{LAVENDER}" stroke-width="3" stroke-linecap="round"/></g>')
        parts.append(f'<path d="M -65 62 H 65" stroke="{color}" stroke-opacity=".25"/><path class="flow" d="M -65 62 H 65" stroke="{color}" stroke-width="2"/>')
    elif kind in {"tree", "zinging"}:
        coords = [(0, -56), (-60, -5), (60, -5), (-86, 54), (-27, 54), (27, 54), (86, 54)] if kind == "tree" else [(0, 0), (-77, -47), (70, -54), (-80, 52), (77, 50), (0, -80), (0, 80)]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)] if kind == "tree" else [(0, i) for i in range(1, 7)] + [(1, 5), (5, 2), (3, 6), (6, 4)]
        for index, (a, b) in enumerate(edges):
            x1, y1 = coords[a]
            x2, y2 = coords[b]
            parts.append(f'<path d="M {x1} {y1} L {x2} {y2}" stroke="{color}" stroke-opacity=".3"/><path class="flow" d="M {x1} {y1} L {x2} {y2}" stroke="{color}" stroke-width="2" style="animation-delay:-{index*.6}s"/>')
        for index, (x, y) in enumerate(coords):
            parts.append(node(x, y, MINT if index % 2 else LAVENDER, 11 if index == 0 else 7, index * .55))
    return "".join(parts)


def project_card(project, index, mobile=False):
    width, height = (640, 352) if mobile else (1200, 236)
    color = project["color"]
    parts = [
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="url(#surface)" stroke="#243331"/>',
        f'<path d="M 22 1 H {width-22}" stroke="{color}" stroke-opacity=".5"/>',
        text(30 if mobile else 36, 35 if mobile else 37, project["category"], 12 if mobile else 13, color, **{"class": "mono", "letter-spacing": 1}),
        text(30 if mobile else 36, 81 if mobile else 83, project["name"], 34 if mobile else 38, **{"font-weight": 700, "letter-spacing": -.8}),
    ]
    lines = textwrap.wrap(project["description"], width=48 if mobile else 78)
    for line_index, line in enumerate(lines):
        parts.append(text(30 if mobile else 36, (119 if mobile else 124) + line_index * 24, line, 18, **{"class": "muted"}))
    x, tag_y = (30, 314) if mobile else (36, 182)
    for label in project["tags"]:
        markup, chip_width = chip(x, tag_y, label, color, 13)
        parts.append(markup)
        x += chip_width + 9
    if mobile:
        parts.append(f'<g transform="translate(500 243) scale(.72)">{illustration(project["id"], color)}</g>')
        parts.append(text(30, 254, "EXPLORE PROJECT", 12, color, **{"class": "mono", "letter-spacing": 1}))
        parts.append(f'<path d="M 170 251 H 185 M 180 246 L 185 251 L 180 256" fill="none" stroke="{color}" stroke-width="1.5"/>')
    else:
        parts.append(f'<path d="M 848 30 V 206" stroke="#243331"/>')
        parts.append(f'<g transform="translate(1022 110)">{illustration(project["id"], color)}</g>')
        parts.append(text(1022, 211, "EXPLORE PROJECT", 11, color, **{"class": "mono", "letter-spacing": 1, "text-anchor": "middle"}))
        parts.append(f'<path d="M 1150 33 H 1162 V 45 M 1149 46 L 1162 33" fill="none" stroke="{color}" stroke-width="1.5"/>')
    return svg(width, height, project["name"], project["description"], "".join(parts))


def main():
    ASSETS.mkdir(exist_ok=True)
    save(ASSETS / "banner.svg", banner())
    save(ASSETS / "banner-mobile.svg", banner(mobile=True))
    divider = f'<path d="M 0 12 H 1200" stroke="url(#edge)" stroke-width="1"/><path class="flow" d="M 0 12 H 1200" stroke="{MINT}" stroke-width="2"/>'
    divider_svg = svg(1200, 24, "", "", divider)
    save(ASSETS / "divider.svg", divider_svg)
    save(ASSETS / "divider-still.svg", still(divider_svg))
    projects = json.loads((ASSETS / "projects.json").read_text())
    for index, project in enumerate(projects):
        for mobile in (False, True):
            name = project["id"] + ("-mobile" if mobile else "")
            card = project_card(project, index, mobile=mobile)
            save(ASSETS / "projects" / f"{name}.svg", card)
            save(ASSETS / "projects" / f"{name}-still.svg", still(card))
    print(f"Built two banners, {len(projects)} animated project cards with mobile versions, and a divider.")


if __name__ == "__main__":
    main()
