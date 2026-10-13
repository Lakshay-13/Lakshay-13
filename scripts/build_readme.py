"""Assemble the profile from the same data used by its animated artwork."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def picture(stem, alt, animated="svg", still="svg", link=None):
    def asset(suffix, extension):
        return f"assets/{stem}{suffix}.{extension}?v=3"
    markup = f'''<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 540px)" srcset="{asset('-mobile-still', still)}">
  <source media="(prefers-reduced-motion: reduce)" srcset="{asset('-still', still)}">
  <source media="(max-width: 540px)" srcset="{asset('-mobile', animated)}">
  <img src="{asset('', animated)}" alt="{html.escape(alt, quote=True)}" width="100%">
</picture>'''
    return f'<a href="{html.escape(link, quote=True)}">\n{markup}\n</a>' if link else markup


def main():
    profile = json.loads((ROOT / "assets/profile.json").read_text())
    projects = json.loads((ROOT / "assets/projects.json").read_text())
    parts = [picture("banner", "Lakshay Chawla — Researcher / Freelancer. The original illustrated avatar, animated mint and lavender orbits, PINNs, 3D Vision, and Generative AI.", animated="gif", still="png"),
             "## About", picture("about", " ".join(profile["about"].values()))]
    for entry in profile["about_links"]:
        parts.append(picture(f'connect/{entry["id"]}', f'{entry["label"]}: {entry["value"]}', link=entry["url"]))
    parts.append("## Selected work")
    for project in projects:
        alt = f'{project["name"]}. {project["description"]}'
        if not project["url"]:
            alt += " Preview soon."
        parts.append(picture(f'projects/{project["id"]}', alt, animated="gif", link=project["url"]))
    parts.extend([
        '<a href="https://www.nextgenaischool.in/"><img src="https://www.nextgenaischool.in/api/portfolio/full-stats.svg" alt="Live NextGenAISchool ecosystem statistics" width="100%"></a>',
        "## Activity", picture("activity", "Lakshay Chawla's GitHub contribution calendar, refreshed daily from GitHub."),
        "## Experience", picture("experience", "; ".join(f'{e["role"]} at {e["organization"]} ({e["dates"]})' for e in profile["experience"])),
        "## Toolkit", picture("toolkit", "; ".join(g["group"] + ": " + ", ".join(g["items"]) for g in profile["toolkit"])),
        "## Education", picture("education", "; ".join(f'{e["degree"]}, {e["institution"]} ({e["dates"]})' for e in profile["education"])),
        "## Connect",
    ])
    for entry in profile["connect"]:
        parts.append(picture(f'connect/{entry["id"]}', f'{entry["label"]}: {entry["value"]}', link=entry["url"]))
    (ROOT / "README.md").write_text("\n\n".join(parts) + "\n")
    print(f"Built a visual README with {len(projects)} project cards, without duplicate introductions or text toggles.")


if __name__ == "__main__":
    main()
