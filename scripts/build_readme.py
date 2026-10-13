"""Assemble the profile from the same data used by its animated artwork."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_VERSIONS = {
    **{f"projects/{name}": 7 for name in ("artgridx", "frenshop", "url")},
    **{f"projects/{name}": 8 for name in ("pinnhub", "variable-stars", "customer", "music", "zinging")},
}


def picture(stem, alt, animated="svg", still="svg", link=None, width="100%"):
    version = ASSET_VERSIONS.get(stem, 6)
    def asset(suffix, extension):
        return f"assets/{stem}{suffix}.{extension}?v={version}"
    markup = f'''<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 540px)" srcset="{asset('-mobile-still', still)}">
  <source media="(prefers-reduced-motion: reduce)" srcset="{asset('-still', still)}">
  <source media="(max-width: 540px)" srcset="{asset('-mobile', animated)}">
  <img src="{asset('', animated)}" alt="{html.escape(alt, quote=True)}" width="{width}">
</picture>'''
    return f'<a href="{html.escape(link, quote=True)}" target="_blank" rel="noopener noreferrer">\n{markup}\n</a>' if link else markup


def main():
    profile = json.loads((ROOT / "assets/profile.json").read_text())
    projects = json.loads((ROOT / "assets/projects.json").read_text())
    parts = [picture("banner", "Lakshay Chawla. AI researcher / Entrepreneur / Educator. Data Scientist, PINNs, 3D Vision, and Generative AI. Original illustrated avatar with a circular wreath of blinking stars.", animated="gif", still="png"),
             "## About", picture("about", " ".join(profile["about"].values()))]
    for entry in profile["about_links"]:
        parts.append(picture(f'connect/{entry["id"]}', f'{entry["label"]}: {entry["value"]}', link=entry["url"]))
    parts.append("## Projects")
    for project in projects:
        alt = f'{project["name"]}. {project["description"]}'
        if not project["url"]:
            alt += " Preview soon."
        parts.append(picture(f'projects/{project["id"]}', alt, animated="gif", link=project["url"]))
    parts.extend([
        '<a href="https://www.nextgenaischool.in/" target="_blank" rel="noopener noreferrer"><img src="https://www.nextgenaischool.in/api/portfolio/full-stats.svg" alt="Live NextGenAISchool ecosystem statistics" width="100%"></a>',
        "## Activity", picture("activity", "Lakshay Chawla's GitHub contribution calendar, refreshed daily from GitHub."),
        "## Experience", picture("experience", "; ".join(f'{e["role"]} at {e["organization"]} ({e["dates"]})' for e in profile["experience"])),
        "## Toolkit", picture("toolkit", "; ".join(g["group"] + ": " + ", ".join(g["items"]) for g in profile["toolkit"])),
        "## Education", picture("education", "; ".join(f'{e["degree"]}, {e["institution"]} ({e["dates"]})' for e in profile["education"])),
        "## Connect",
    ])
    for index in range(0, len(profile["connect"]), 3):
        row = []
        for entry in profile["connect"][index:index+3]:
            row.append(picture(f'connect/{entry["id"]}', f'{entry["label"]}: {entry["value"]}', link=entry["url"], width="32%"))
        parts.append('<p align="center">\n'+"\n".join(row)+'\n</p>')
    (ROOT / "README.md").write_text("\n\n".join(parts) + "\n")
    print(f"Built a visual README with {len(projects)} project cards, without duplicate introductions or text toggles.")


if __name__ == "__main__":
    main()
