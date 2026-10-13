"""Build self-contained SVG artwork from local profile data and verified logos."""

import base64
import html
import json
import random
import textwrap
from pathlib import Path
from xml.etree import ElementTree
from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MINT = "#2effbf"
LAVENDER = "#b9a7ff"
FONT_PATH = next((path for path in [
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
    Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
] if path.is_file()), None)
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


def chip_width(label, size=13):
    if FONT_PATH:
        return round(ImageFont.truetype(str(FONT_PATH), size).getlength(label) + 32)
    return round(len(label) * size * .65 + 32)


def chip(x, y, label, color=MINT, size=13):
    width = chip_width(label, size)
    return (
        f'<g data-pill="true"><rect x="{x}" y="{y}" width="{width}" height="32" rx="16" fill="#10251f" stroke="{color}" stroke-opacity=".75" stroke-width="1.4"/>'
        + text(x + width / 2, y + 21, label, size, color, **{"text-anchor": "middle"}) + "</g>"
    ), width


def banner(mobile=False):
    width, height = (640, 700) if mobile else (1200, 480)
    # The existing banner's portrait is displayed through a viewport, unchanged.
    original = base64.b64encode((ROOT / "top-banner.jpg").read_bytes()).decode()
    px, py, size = (168, 55, 304) if mobile else (795, 64, 346)
    cx, cy = px + size / 2, py + size / 2
    defs = f'''<radialGradient id="portrait-fade" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{size/2}"><stop offset=".67" stop-color="white"/><stop offset="1" stop-color="black"/></radialGradient>
<mask id="portrait-mask" maskUnits="userSpaceOnUse" x="{px}" y="{py}" width="{size}" height="{size}"><rect x="{px}" y="{py}" width="{size}" height="{size}" fill="url(#portrait-fade)"/></mask>
<clipPath id="panel-clip"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="26"/></clipPath>'''
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
            text(320, 35, "DATA SCIENTIST", 24, MINT, **{"text-anchor": "middle", "letter-spacing": 3, "class": "mono", "font-weight": 700}),
            text(320, 412, "Lakshay Chawla.", 54, **{"text-anchor": "middle", "font-weight": 700, "letter-spacing": -2}),
            text(320, 451, "Scientific ML / AI Research", 23, LAVENDER, **{"text-anchor": "middle"}),
            text(320, 558, "Useful, grounded, accessible AI.", 22, **{"text-anchor": "middle", "class": "muted"}),
            text(320, 623, "CLARITY LAB / IIT JODHPUR", 15, MINT, **{"text-anchor": "middle", "class": "mono"}),
            text(320, 651, "NEXTGENAISCHOOL", 15, LAVENDER, **{"text-anchor": "middle", "class": "mono", "letter-spacing": 2}),
        ])
        x, y = (width - sum(chip_width(label, 15) for label in ["PINNs", "3D Vision", "Generative AI"]) - 16) / 2, 479
    else:
        parts.extend([
            text(56, 55, "DATA SCIENTIST", 28, MINT, **{"letter-spacing": 3, "class": "mono", "font-weight": 700}),
            text(52, 157, "Lakshay", 86, **{"font-weight": 700, "letter-spacing": -3}),
            text(52, 243, "Chawla.", 86, **{"font-weight": 700, "letter-spacing": -3}),
            text(56, 289, "Scientific ML / AI Research", 24, LAVENDER),
            text(56, 391, "AI that is useful, grounded, and accessible.", 19, **{"class": "muted"}),
            text(56, 446, "CLARITY LAB / IIT JODHPUR", 12, MINT, **{"class": "mono", "letter-spacing": 1}),
            text(1144, 446, "NEXTGENAISCHOOL", 12, LAVENDER, **{"text-anchor": "end", "class": "mono", "letter-spacing": 1}),
        ])
        x, y = 56, 318
    for label in ["PINNs", "3D Vision", "Generative AI"]:
        markup, pill_width = chip(x, y, label, size=15)
        parts.append(markup)
        x += pill_width + 8
    return svg(width, height, "Lakshay Chawla — Data Scientist", "The original illustrated avatar in a mint and lavender orbital starfield. Data scientist, AI researcher, entrepreneur, and educator working on PINNs, 3D vision, and generative AI.", '<g clip-path="url(#panel-clip)">' + "".join(parts) + '</g>', defs)


def artwork(project):
    color = project["color"]
    parts = [f'<rect x="-91" y="-87" width="182" height="174" rx="24" fill="#101821" stroke="{color}" stroke-opacity=".22"/>']
    if project.get("artwork"):
        encoded = base64.b64encode((ASSETS / project["artwork"]).read_bytes()).decode()
        image = f'<image x="-73" y="-70" width="146" height="140" href="data:image/png;base64,{encoded}" preserveAspectRatio="xMidYMid meet"/>'
        parts.append(f'<g class="float">{image}</g>')
    else:
        parts.append(text(0, 10, project["name"], 35, color, **{"text-anchor": "middle", "font-weight": 700}))
    parts.append(f'<circle class="signal" cx="80" cy="-76" r="3" fill="{color}"/>')
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
        parts.append(f'<g transform="translate(510 240) scale(.72)">{artwork(project)}</g>')
        parts.append(text(30, 254, "EXPLORE PROJECT", 12, color, **{"class": "mono", "letter-spacing": 1}))
        parts.append(f'<path d="M 170 251 H 185 M 180 246 L 185 251 L 180 256" fill="none" stroke="{color}" stroke-width="1.5"/>')
    else:
        parts.append(f'<path d="M 848 30 V 206" stroke="#243331"/>')
        parts.append(f'<g transform="translate(1022 110)">{artwork(project)}</g>')
        parts.append(text(1022, 211, "EXPLORE PROJECT", 11, color, **{"class": "mono", "letter-spacing": 1, "text-anchor": "middle"}))
        parts.append(f'<path d="M 1150 33 H 1162 V 45 M 1149 46 L 1162 33" fill="none" stroke="{color}" stroke-width="1.5"/>')
    return svg(width, height, project["name"], project["description"], "".join(parts))


def panel(width, height, parts):
    return f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="url(#surface)" stroke="#243331"/>' + "".join(parts)


def experience_panel(profile, mobile=False):
    width = 640 if mobile else 1200
    rows, cursor = [], 108
    for index, entry in enumerate(profile["experience"]):
        lines = textwrap.wrap(entry["role"], width=39 if mobile else 86)
        rows.append((entry, lines, cursor, index))
        cursor += 112 + (len(lines) - 1) * 32 if mobile else 79
    height = cursor + 20
    parts = [text(36, 44, "Data science, research, and applied AI", 25 if mobile else 28, **{"font-weight": 700})]
    parts.append(f'<path d="M 45 99 V {rows[-1][2]+10}" stroke="{MINT}" stroke-opacity=".2" stroke-width="2"/><path class="flow" d="M 45 99 V {rows[-1][2]+10}" stroke="{MINT}" stroke-width="2"/>')
    for entry, lines, y, index in rows:
        color = MINT if "Present" in entry["dates"] else LAVENDER
        parts.append(f'<circle cx="45" cy="{y-8}" r="7" fill="#101c21" stroke="{color}" stroke-width="1.5"/><circle class="signal" cx="45" cy="{y-8}" r="3" fill="{color}" style="animation-delay:-{index*.65}s"/>')
        for line_index, line in enumerate(lines):
            parts.append(text(76, y + line_index * 32, line, 25 if mobile else 23, **{"font-weight": 700}))
        company_y = y + (len(lines) - 1) * 32 + (31 if mobile else 27)
        parts.append(text(76, company_y, entry["organization"], 20 if mobile else 18, color))
        parts.append(text(76 if mobile else width-36, company_y + 26 if mobile else y, entry["dates"], 17 if mobile else 17, **{"class": "muted", "text-anchor": "start" if mobile else "end"}))
    description = "; ".join(f'{entry["role"]} at {entry["organization"]} ({entry["dates"]})' for entry in profile["experience"])
    return svg(width, height, "Experience", description, panel(width, height, parts))


def education_panel(profile, mobile=False):
    width = 640 if mobile else 1200
    parts, cursor = [], 52
    for index, entry in enumerate(profile["education"]):
        lines = textwrap.wrap(entry["degree"], width=37 if mobile else 87)
        color = MINT if index == 0 else LAVENDER
        row_height = 150 + (len(lines)-1)*32 if mobile else 130
        parts.append(f'<circle cx="45" cy="{cursor-9}" r="8" fill="#10251f" stroke="{color}" stroke-width="2"/><circle class="signal" cx="45" cy="{cursor-9}" r="4" fill="{color}" style="animation-delay:-{index*2}s"/>')
        for line_index, line in enumerate(lines):
            parts.append(text(76, cursor + line_index * 32, line, 25 if mobile else 28, **{"font-weight": 700}))
        institution_y = cursor + (len(lines)-1)*32 + 35
        for line_index, line in enumerate(textwrap.wrap(entry["institution"], width=47 if mobile else 100)):
            parts.append(text(76, institution_y + line_index * 27, line, 20 if mobile else 21, color))
        parts.append(text(76, institution_y + 35, entry["dates"], 17 if mobile else 18, **{"class": "muted"}))
        cursor += row_height
    height = cursor - 12
    line = f'<path d="M 45 43 V {52+(150 + (len(textwrap.wrap(profile["education"][0]["degree"], width=37))-1)*32 if mobile else 130)-9}" stroke="{MINT}" stroke-opacity=".2" stroke-width="2"/>'
    parts.insert(0, line)
    parts.insert(1, line.replace('<path ', '<path class="flow" ').replace('stroke-opacity=".2"', 'stroke-opacity=".85"'))
    description = "; ".join(f'{entry["degree"]}, {entry["institution"]} ({entry["dates"]})' for entry in profile["education"])
    return svg(width, height, "Education", description, panel(width, height, parts))


def toolkit_panel(profile, mobile=False):
    width, cursor = (640 if mobile else 1200), 46
    parts = []
    for group_index, group in enumerate(profile["toolkit"]):
        color = MINT if group_index % 2 == 0 else LAVENDER
        parts.append(text(36, cursor, group["group"], 23 if mobile else 26, color, **{"font-weight": 700}))
        for point in range(3):
            parts.append(f'<circle class="signal" cx="{width-76+point*14}" cy="{cursor-8}" r="3" fill="{color}" style="animation-delay:-{group_index+point*.6}s"/>')
        x, y = 36, cursor + 24
        size = 16 if mobile else 16
        for item in group["items"]:
            item_width = chip_width(item, size)
            if x + item_width > width-36:
                x, y = 36, y + 42
            markup, item_width = chip(x, y, item, color, size)
            parts.append(markup)
            x += item_width + 9
        cursor = y + 91
    height = cursor - 30
    description = "; ".join(group["group"] + ": " + ", ".join(group["items"]) for group in profile["toolkit"])
    return svg(width, height, "Data scientist's toolkit", description, panel(width, height, parts))


def main():
    ASSETS.mkdir(exist_ok=True)
    save(ASSETS / "banner.svg", banner())
    save(ASSETS / "banner-mobile.svg", banner(mobile=True))
    projects = json.loads((ASSETS / "projects.json").read_text())
    for index, project in enumerate(projects):
        for mobile in (False, True):
            name = project["id"] + ("-mobile" if mobile else "")
            card = project_card(project, index, mobile=mobile)
            save(ASSETS / "projects" / f"{name}.svg", card)
            save(ASSETS / "projects" / f"{name}-still.svg", still(card))
    profile = json.loads((ASSETS / "profile.json").read_text())
    for name, render in [("experience", experience_panel), ("education", education_panel), ("toolkit", toolkit_panel)]:
        for mobile in (False, True):
            stem = name + ("-mobile" if mobile else "")
            content = render(profile, mobile=mobile)
            save(ASSETS / f"{stem}.svg", content)
            save(ASSETS / f"{stem}-still.svg", still(content))
    print(f"Built two banners, {len(projects)} project cards with verified artwork, and animated experience, education, and toolkit panels.")


if __name__ == "__main__":
    main()
