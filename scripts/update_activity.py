"""Refresh contribution artwork from GitHub without changing README content."""

import datetime as dt
import html
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
USER = "Lakshay-13"
MINT = "#2effbf"
COLORS = ["#10231e", "#14563e", "#15805a", "#1fb582", MINT]


def github(endpoint, token, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": f"{USER}-profile-activity",
    }
    for attempt in range(3):
        try:
            with urlopen(Request(f"https://api.github.com/{endpoint}", data=data, headers=headers), timeout=30) as response:
                result = json.load(response)
            if isinstance(result, dict) and result.get("errors"):
                raise RuntimeError("GitHub GraphQL did not return contribution data.")
            return result
        except (HTTPError, URLError, TimeoutError) as error:
            if attempt == 2:
                reason = f"HTTP {error.code}" if isinstance(error, HTTPError) else type(error).__name__
                raise RuntimeError(f"GitHub request failed after 3 attempts: {reason}.") from error
            time.sleep(2 ** attempt)
    raise RuntimeError("GitHub returned no data.")


def label(x, y, value, size=14, fill="#aab3c0", anchor="start", weight=400):
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(str(value))}</text>'


def calendar_svg(calendar, updated, mobile=False, still=False):
    width, height = (640, 310) if mobile else (1200, 310)
    weeks = calendar["weeks"][-26:] if mobile else calendar["weeks"]
    spacing = (width - 76) / len(weeks)
    cell = min(16, spacing - 4)
    peak = max((day["contributionCount"] for week in weeks for day in week["contributionDays"]), default=0)
    period = "Recent 26 weeks" if mobile else "Last 12 months"
    parts = [
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="#080f16" stroke="#243331"/>',
        label(36, 42, "GitHub activity", 28, "#f4f7fb", weight=700),
        label(36, 70, f"{period} / contributions", 14),
        label(width - 36, 43, f'{calendar["totalContributions"]:,}', 32, MINT, "end", 700),
        label(width - 36, 65, "TOTAL / LAST 12 MONTHS", 10, "#aab3c0", "end"),
    ]
    previous_month = None
    for column, week in enumerate(weeks):
        first = dt.date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != previous_month and column < len(weeks) - 2:
            parts.append(label(round(38 + column * spacing, 2), 98, first.strftime("%b"), 11))
            previous_month = first.month
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            if not isinstance(count, int) or count < 0 or day["weekday"] not in range(7):
                raise ValueError("GitHub returned an invalid contribution day.")
            level = 0 if not count else min(4, max(1, int(count / max(1, peak) * 3) + 1))
            x = 38 + column * spacing
            y = 112 + day["weekday"] * 20
            tooltip = f'{day["date"]}: {count} contribution' + ("" if count == 1 else "s")
            parts.append(f'<rect x="{x:.2f}" y="{y}" width="{cell:.2f}" height="{cell:.2f}" rx="3" fill="{COLORS[level]}"><title>{tooltip}</title></rect>')
    parts.append(label(36, 278, "Less", 12))
    for index, color in enumerate(COLORS):
        parts.append(f'<rect x="{70+index*19}" y="267" width="13" height="13" rx="3" fill="{color}"/>')
    parts.extend([
        label(169, 278, "More", 12),
        label(width - 36, 278, f'Updated {updated.strftime("%d %b %Y")} / daily', 12, anchor="end"),
        f'<circle class="pulse" cx="{width-27}" cy="86" r="3" fill="{MINT}"/>',
    ])
    result = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
<title id="title">Lakshay Chawla's GitHub contribution calendar</title>
<desc id="description">{calendar["totalContributions"]} contributions in the last 12 months. {period} displayed. Source: GitHub GraphQL contributionCalendar. Retrieved {updated.isoformat()}. Updated daily by GitHub Actions.</desc>
<style>.pulse{{animation:pulse 4s ease-in-out infinite}}@keyframes pulse{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{"".join(parts)}
</svg>
'''
    if still:
        result = result.replace("</style>", "*{animation:none!important}</style>")
    ElementTree.fromstring(result)
    return result


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required to retrieve verified contribution data.")
    query = """query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date weekday contributionCount } }
          }
        }
      }
    }"""
    response = github("graphql", token, {"query": query, "variables": {"login": USER}})
    calendar = response["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    if not calendar["weeks"] or not isinstance(calendar["totalContributions"], int):
        raise RuntimeError("GitHub returned an empty or invalid contribution calendar.")
    updated = dt.datetime.now(ZoneInfo("Asia/Kolkata")).replace(microsecond=0)
    output = {
        ROOT / "assets/activity.svg": calendar_svg(calendar, updated),
        ROOT / "assets/activity-mobile.svg": calendar_svg(calendar, updated, mobile=True),
        ROOT / "assets/activity-still.svg": calendar_svg(calendar, updated, still=True),
        ROOT / "assets/activity-mobile-still.svg": calendar_svg(calendar, updated, mobile=True, still=True),
    }
    for path, content in output.items():
        path.write_text(content)
    print(f'Refreshed verified activity: {calendar["totalContributions"]} contributions, {len(calendar["weeks"])} weeks.')


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        message = str(error).replace("\n", " ").replace("\r", " ")[:250]
        print(f"Activity refresh failed: {message}", file=sys.stderr)
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a") as output:
                output.write(f"error={message}\n")
        sys.exit(1)
