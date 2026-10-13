"""Build self-contained SVG artwork from local profile data and verified logos."""

import base64
import html
import json
import math
import random
import textwrap
from pathlib import Path
from xml.etree import ElementTree
from PIL import ImageFont
from project_scenes import render as project_scene

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
.orbit{transform-box:fill-box;transform-origin:center;animation:spin 8s linear infinite}
.drift{animation:drift 8s ease-in-out infinite}
.meter{transform-box:fill-box;transform-origin:bottom;animation:meter 4s ease-in-out infinite}
@keyframes flow{to{stroke-dashoffset:-688}}
@keyframes dash{to{stroke-dashoffset:-96}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes breath{0%,100%{opacity:.3}50%{opacity:.8}}
@keyframes glint{0%,100%{opacity:.18}50%{opacity:.9}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes signal{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(4px,-12px)}}
@keyframes meter{0%,100%{transform:scaleY(.3);opacity:.35}50%{transform:scaleY(1);opacity:.75}}
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


def stars(width, height, count=250):
    rng = random.Random(13)
    return "".join(
        f'<circle class="poster-star" cx="{rng.uniform(18, width-18):.1f}" cy="{rng.uniform(18, height-18):.1f}" r="{rng.choice([.6, .8, 1.1, 1.5]):.1f}" fill="{rng.choice([MINT, LAVENDER, "#d6e9e3"])}" style="animation-delay:-{rng.uniform(0, 2):.2f}s"/>'
        for _ in range(count)
    )


def chip_width(label, size=13):
    if FONT_PATH:
        return round(ImageFont.truetype(str(FONT_PATH), size).getlength(label) + 32)
    return round(len(label) * size * .65 + 32)


def wrap_pixels(value, width, size):
    lines, line = [], ""
    for word in value.split():
        candidate = f"{line} {word}".strip()
        if line and chip_width(candidate, size) - 32 > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    return lines + ([line] if line else [])


def asset_image(file, x, y, width, height):
    mime = "image/svg+xml" if file.endswith(".svg") else "image/png"
    encoded = base64.b64encode((ASSETS / file).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{width}" height="{height}" href="data:{mime};base64,{encoded}" preserveAspectRatio="xMidYMid meet"/>'


def star_wreath(cx, cy, radius):
    rng = random.Random(13)
    parts = []
    for index in range(72):
        angle = index * 2 * math.pi / 72
        x, y = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
        size = 6.5 if index % 18 == 0 else rng.choice([2, 2.5, 3.5, 4.5, 5])
        color = rng.choice(["#e0f4ed", MINT, LAVENDER])
        parts.append(f'<path class="poster-spark" d="M {x:.2f} {y-size:.2f} Q {x:.2f} {y:.2f} {x+size:.2f} {y:.2f} Q {x:.2f} {y:.2f} {x:.2f} {y+size:.2f} Q {x:.2f} {y:.2f} {x-size:.2f} {y:.2f} Q {x:.2f} {y:.2f} {x:.2f} {y-size:.2f} Z" fill="{color}" style="animation-delay:-{rng.uniform(0,1.6):.2f}s"/>')
    return f'<g class="poster-orbit" style="transform-origin:{cx}px {cy}px">'+"".join(parts)+'</g>'


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
        '<style>.poster-star{animation:posterTwinkle 2s ease-in-out infinite}.poster-spark{animation:posterSpark 1.6s ease-in-out infinite}.poster-orbit{transform-box:view-box;animation:posterOrbit 8s linear infinite}@keyframes posterTwinkle{0%,100%{opacity:.25}50%{opacity:.9}}@keyframes posterSpark{0%,100%{opacity:.45}50%{opacity:1}}@keyframes posterOrbit{to{transform:rotate(360deg)}}</style>',
        stars(width, height, 190 if mobile else 250),
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
        star_wreath(cx, cy, size*.53),
        f'<g mask="url(#portrait-mask)"><svg x="{px}" y="{py}" width="{size}" height="{size}" viewBox="260 125 1040 1040" overflow="hidden"><image href="data:image/jpeg;base64,{original}" width="4441" height="1200"/></svg></g>',
        f'<circle class="breath" cx="{cx+size*.43}" cy="{cy+size*.2}" r="6" fill="{MINT}" filter="url(#glow)"/>',
        f'<circle cx="{cx+size*.43}" cy="{cy+size*.2}" r="3" fill="{MINT}"/>',
    ])
    if mobile:
        parts.extend([
            text(320, 35, "AI researcher / Entrepreneur / Educator", 22, LAVENDER, **{"text-anchor": "middle"}),
            text(320, 424, "Lakshay Chawla.", 54, **{"text-anchor": "middle", "font-weight": 700, "letter-spacing": -2}),
            text(320, 463, "Data Scientist", 27, LAVENDER, **{"text-anchor": "middle"}),
            text(320, 558, "Useful, grounded, accessible AI.", 22, **{"text-anchor": "middle", "class": "muted"}),
            text(320, 623, "CLARITY LAB / IIT JODHPUR", 15, MINT, **{"text-anchor": "middle", "class": "mono"}),
            text(320, 651, "NEXTGENAISCHOOL", 15, LAVENDER, **{"text-anchor": "middle", "class": "mono", "letter-spacing": 2}),
        ])
        x, y = (width - sum(chip_width(label, 15) for label in ["PINNs", "3D Vision", "Generative AI"]) - 16) / 2, 491
    else:
        parts.extend([
            text(56, 55, "AI researcher / Entrepreneur / Educator", 23, LAVENDER),
            text(52, 157, "Lakshay", 86, **{"font-weight": 700, "letter-spacing": -3}),
            text(52, 243, "Chawla.", 86, **{"font-weight": 700, "letter-spacing": -3}),
            text(56, 289, "Data Scientist", 27, LAVENDER),
            text(56, 391, "AI that is useful, grounded, and accessible.", 19, **{"class": "muted"}),
            text(56, 446, "CLARITY LAB / IIT JODHPUR", 12, MINT, **{"class": "mono", "letter-spacing": 1}),
            text(1144, 446, "NEXTGENAISCHOOL", 12, LAVENDER, **{"text-anchor": "end", "class": "mono", "letter-spacing": 1}),
        ])
        x, y = 56, 318
    for label in ["PINNs", "3D Vision", "Generative AI"]:
        markup, pill_width = chip(x, y, label, size=15)
        parts.append(markup)
        x += pill_width + 8
    return svg(width, height, "Lakshay Chawla — Data Scientist", "Original titles restored: AI researcher / Entrepreneur / Educator. Data Scientist working on PINNs, 3D Vision, and Generative AI. The unchanged illustrated avatar is surrounded by a circular wreath of blinking stars.", '<g clip-path="url(#panel-clip)">' + "".join(parts) + '</g>', defs)


def project_card(project, index, mobile=False):
    width, height = (640, 454) if mobile else (1200, 282)
    color = project["color"]
    parts = [
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="url(#surface)" stroke="#243331"/>',
        f'<path d="M 22 1 H {width-22}" stroke="{color}" stroke-opacity=".5"/>',
        text(30 if mobile else 36, 36 if mobile else 38, project["category"], 16 if mobile else 17, "#afc9c2", **{"class": "mono", "letter-spacing": .5}),
    ]
    name_x = 92 if project.get("artwork") else (30 if mobile else 36)
    if project.get("artwork"):
        parts.append(asset_image(project["artwork"], 30 if mobile else 36, 55, 44, 44))
    title_lines = wrap_pixels(project["name"], 590-name_x if mobile else 820-name_x, 36)
    for line_index, line in enumerate(title_lines):
        parts.append(text(name_x, 86 + line_index * 42, line, 36, **{"font-weight": 700, "letter-spacing": -.6}))
    desc_y = 126 + (len(title_lines)-1)*42
    lines = wrap_pixels(project["description"], 565 if mobile else 784, 25 if mobile else 24)
    for line_index, line in enumerate(lines):
        parts.append(text(30 if mobile else 36, desc_y + line_index * 33, line, 25 if mobile else 24, "#c2cbd7"))
    for line_index, line in enumerate(wrap_pixels(" / ".join(project["tags"]), 340 if mobile else 780, 18)):
        parts.append(text(30 if mobile else 36, (342 if mobile else 241) + line_index * 26, line, 18, "#9aadb9"))
    if mobile:
        parts.append(f'<g transform="translate(384 267) scale(.72)">{project_scene(project["id"])}</g>')
    else:
        parts.append(f'<g transform="translate(862 24)">{project_scene(project["id"])}</g>')
    if not project.get("url"):
        parts.append(text(30 if mobile else 36, 425 if mobile else 268, "PREVIEW SOON", 15, color, **{"class": "mono"}))
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
    width = 640 if mobile else 1200
    parts = [text(36, 48, "From research to production", 32, **{"font-weight": 700}),
             text(36, 83, "Data science / AI / systems", 22, "#afbbc9")]
    tiles = [("Python", "brands/python.svg"), ("Codex", "brands/codex-terminal.svg"),
             ("GCP / AWS", None), ("Database / APIs", None), ("PINNs / Neural nets", None)]
    columns = 3 if mobile else 5
    tile_width = (width-72-(columns-1)*14)/columns
    for i, (name, file) in enumerate(tiles):
        x, y = 36+(i%columns)*(tile_width+14), 110+(i//columns)*136
        parts.append(f'<rect x="{x}" y="{y}" width="{tile_width}" height="120" rx="14" fill="#111d2d"/>')
        center = x+tile_width/2
        if file:
            parts.append(f'<rect x="{center-27}" y="{y+13}" width="54" height="54" rx="12" fill="#edf1f5"/>')
            icon_size = 32 if "chatgpt" in file else 38
            parts.append(asset_image(file, center-icon_size/2, y+40-icon_size/2, icon_size, icon_size))
        elif i == 2:
            parts.append(f'<rect x="{center-66}" y="{y+15}" width="132" height="49" rx="10" fill="#edf1f5"/>')
            parts.append(asset_image("brands/gcp-mark.png", center-54, y+20, 40, 40))
            parts.append(asset_image("brands/aws.png", center+4, y+23, 54, 34))
        elif i == 3:
            parts.append(f'<ellipse cx="{center-29}" cy="{y+25}" rx="18" ry="6" fill="#162e32" stroke="{MINT}" stroke-width="1.6"/>')
            parts.append(f'<path d="M {center-47} {y+25} V {y+52} C {center-47} {y+61} {center-11} {y+61} {center-11} {y+52} V {y+25} M {center-47} {y+37} C {center-47} {y+46} {center-11} {y+46} {center-11} {y+37}" fill="none" stroke="{MINT}" stroke-width="1.6"/>')
            parts.append(text(center+30, y+52, "{ }", 25, LAVENDER, **{"text-anchor": "middle", "class": "mono"}))
            parts.append(f'<path d="M {center-2} {y+42} H {center+6} M {center+3} {y+39} L {center+6} {y+42} L {center+3} {y+45}" fill="none" stroke="#8da7b3" stroke-width="1.5"/>')
        else:
            for layer, count in enumerate([2,3,2]):
                for n in range(count):
                    nx, ny = center-43+layer*43, y+24+n*19+(3-count)*9
                    if layer<2:
                        for m in range([3,2][layer]):
                            dest_y=y+24+m*19+(3-[3,2][layer])*9
                            parts.append(f'<path d="M {nx} {ny} L {nx+43} {dest_y}" stroke="#486371" stroke-opacity=".45"/>')
                    parts.append(f'<circle class="signal" cx="{nx}" cy="{ny}" r="4.5" fill="{MINT if layer%2==0 else LAVENDER}" style="animation-delay:-{layer+n*.4}s"/>')
        title_size = 17 if mobile and i == 4 else 19
        parts.append(text(center, y+97, name, title_size, "#c9d5e1", **{"text-anchor": "middle"}))
    cursor = 110+((len(tiles)+columns-1)//columns)*136+24
    for group_index, group in enumerate(profile["toolkit"]):
        color = MINT if group_index % 2 == 0 else LAVENDER
        size = 29 if mobile else 24
        lines = wrap_pixels("  /  ".join(group["items"]), width-90 if mobile else 762, size)
        row_height = 88 + len(lines)*40 if mobile else max(108, 48+len(lines)*38)
        parts.append(f'<rect x="24" y="{cursor-24}" width="{width-48}" height="{row_height-12}" rx="14" fill="{("#101824" if group_index%2==0 else "#0d1520")}"/>')
        parts.append(f'<circle class="signal" cx="39" cy="{cursor+2}" r="2.5" fill="{color}" style="animation-delay:-{group_index*.8}s"/>')
        parts.append(text(55, cursor+10, group["group"], 27 if mobile else 25, "#d4dde9", **{"font-weight": 700}))
        for line_index, line in enumerate(lines):
            parts.append(text(55 if mobile else 388, cursor+56+line_index*40 if mobile else cursor+10+line_index*38, line, size, "#b8c5d5"))
        cursor += row_height
    height = cursor + 8
    description = "; ".join(group["group"] + ": " + ", ".join(group["items"]) for group in profile["toolkit"])
    return svg(width, height, "Toolkit", description, panel(width, height, parts))


def about_panel(profile, mobile=False):
    width, height = (640, 850) if mobile else (1200, 480)
    about = profile["about"]
    parts = [text(36, 43, "RESEARCH / PRODUCTS / EDUCATION", 18, "#afc9c2", **{"class": "mono"})]
    cursor = 93
    headline = ["Data science, research,", "and useful AI."] if mobile else ["Data science, research, and useful AI."]
    for line in headline:
        parts.append(text(36, cursor, line, 36, **{"font-weight": 700}))
        cursor += 43
    for line in wrap_pixels(about["intro"], width-72, 29 if mobile else 26):
        parts.append(text(36, cursor+6, line, 29 if mobile else 26, "#c2cbd7"))
        cursor += 38
    cursor += 35
    row_start = cursor
    for index, key in enumerate(["research", "building"]):
        x = 36 if mobile or index == 0 else 638
        if mobile:
            cursor = row_start if index == 0 else cursor+48
        else:
            cursor = row_start
        color = MINT if index == 0 else LAVENDER
        label = "Research" if index == 0 else "Building"
        parts.append(f'<circle class="signal" cx="{x+6}" cy="{cursor-9}" r="4" fill="{color}" style="animation-delay:-{index*2}s"/>')
        parts.append(text(x+23, cursor, label, 29 if mobile else 26, "#d4dde9", **{"font-weight": 700}))
        cursor += 39
        for line in wrap_pixels(about[key], 568 if mobile else 526, 28 if mobile else 24):
            parts.append(text(x, cursor, line, 28 if mobile else 24, "#b8c5d5"))
            cursor += 37 if mobile else 33
    height = max(height, cursor+50)
    for i in range(4):
        parts.append(f'<circle class="glint" cx="{width-91+i*15}" cy="{39+(i%2)*7}" r="2" fill="{LAVENDER}" style="animation-delay:-{i*.7}s"/>')
    return svg(width, height, "About Lakshay Chawla", " ".join(about.values()), panel(width, height, parts))


CONTACT_ICONS = {
    "email": '<rect x="8" y="16" width="44" height="30" rx="5"/><path d="m9 18 21 16 21-16"/>',
    "phone": '<path d="M18 9h8l4 13-6 4c5 9 10 14 19 19l4-6 13 4v8c0 5-6 8-10 6C24 47 13 36 10 18c-1-4 3-9 8-9Z" transform="translate(-3 -1) scale(.9)"/>',
    "github": '<path d="M21 42c-9 4-10-4-14-4M21 52v-9c0-3 1-4 3-5-9-1-17-4-17-15 0-4 2-7 4-10-1-3-1-6 0-9 6 0 10 4 10 4a35 35 0 0 1 19 0s4-4 10-4c1 3 1 6 0 9 3 3 4 6 4 10 0 11-8 14-17 15 2 2 3 4 3 7v7" transform="translate(2 5) scale(.85)"/>',
    "linkedin": '<rect x="9" y="9" width="42" height="42" rx="5"/><path d="M20 27v15M31 42V27c0-1 12-5 12 5v10"/><circle cx="20" cy="19" r="2"/>',
    "portfolio": '<circle cx="30" cy="30" r="22"/><ellipse cx="30" cy="30" rx="10" ry="22"/><path d="M8 30h44M12 18h36M12 42h36"/>',
    "resume": '<path d="M16 7h22l10 10v36H16V7Z M38 7v12h10M23 29h18M23 37h18M23 45h12"/>',
    "research": '<circle cx="21" cy="30" r="13"/><circle cx="40" cy="30" r="13"/><path d="M30 13v34"/>',
    "building": '<path d="M10 50V20h17V10h23v40H10ZM18 28h3m-3 9h3m14-19h7m-7 10h7m-7 10h7"/>',
}


def contact_card(entry, mobile=False):
    brand = entry["id"] in ["research", "building"]
    width, height = ((640, 166) if mobile else (1200, 136)) if brand else ((200, 196) if mobile else (380, 190))
    color = MINT if entry["id"] in ["email", "github", "portfolio", "research"] else LAVENDER
    if brand:
        parts = [asset_image(entry["artwork"], 22, 15, 98, height-30), text(145, 55, entry["label"], 30, **{"font-weight": 700})]
        value_x, value_y, value_size, value_width = 145, 99, 24, width-211
    else:
        icon_scale = .65 if mobile else .85
        parts = [f'<g transform="translate(20 19) scale({icon_scale})" fill="none" stroke="#c3d6dc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{CONTACT_ICONS[entry["id"]]}</g>', text(20 if mobile else 88, 85 if mobile else 56, entry["label"], 26, **{"font-weight": 700})]
        value_x, value_y, value_size, value_width = 20, 124 if mobile else 117, 18 if mobile else 23, width-40
    value = entry["value"]
    if mobile and not brand and entry["id"] == "email":
        lines = [value.split("@")[0], "@"+value.split("@")[1]]
    elif mobile and not brand and entry["id"] in ["github", "portfolio"]:
        lines = value.split("/") if entry["id"] == "github" else ["lakshay-13", ".github.io"]
    else:
        lines = wrap_pixels(value, value_width, value_size)
    for index, line in enumerate(lines):
        parts.append(text(value_x, value_y+index*29, line, value_size, "#afc1d1"))
    arrow_y = height/2 if brand else 41
    parts.append(f'<path d="M {width-48} {arrow_y-8} H {width-32} V {arrow_y+8} M {width-48} {arrow_y+8} L {width-32} {arrow_y-8}" fill="none" stroke="{color}" stroke-width="1.6"/>')
    parts.append(f'<circle class="signal" cx="{width-28}" cy="{height-25}" r="2.5" fill="{color}"/>')
    return svg(width, height, entry["label"], entry["value"], panel(width, height, parts))


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
    for name, render in [("experience", experience_panel), ("education", education_panel), ("toolkit", toolkit_panel), ("about", about_panel)]:
        for mobile in (False, True):
            stem = name + ("-mobile" if mobile else "")
            content = render(profile, mobile=mobile)
            save(ASSETS / f"{stem}.svg", content)
            save(ASSETS / f"{stem}-still.svg", still(content))
    for entry in profile["connect"] + profile["about_links"]:
        for mobile in (False, True):
            stem = entry["id"] + ("-mobile" if mobile else "")
            content = contact_card(entry, mobile=mobile)
            save(ASSETS / "connect" / f"{stem}.svg", content)
            save(ASSETS / "connect" / f"{stem}-still.svg", still(content))
    print(f"Built two banners, {len(projects)} animated project cards, About, Toolkit, Connect, Experience, and Education.")


if __name__ == "__main__":
    main()
