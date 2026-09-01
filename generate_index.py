#!/usr/bin/env python3
"""
generate_index.py

Scans the current directory for .html lecture note files and
regenerates index.html as a styled list of links to all of them.

Expects filenames like:
    95_ConvNext_Architecture.html      -> "95 ConvNext Architecture"
    97_Visualizing_CNNS.html           -> "97 Visualizing CNNS"
    Lec-96_FineTuning_CNNs.html        -> "96 FineTuning CNNs"

Underscores/hyphens in the name portion become spaces, and files
are sorted numerically by lecture number (not alphabetically).

Usage:
    python3 generate_index.py

Run this any time after adding a new .html file, or let the
GitHub Action (build-index.yml) run it automatically on every push.
"""

import os
import re
from datetime import datetime

# Files to exclude from the index (the index itself, templates, etc.)
EXCLUDE = {"index.html", "notes_style_template.html"}

# Matches an optional "Lec" / "Lec-" / "Lec_" prefix, then digits,
# then an optional separator, then the rest of the name.
FILENAME_PATTERN = re.compile(r'^(?:lec[-_]?)?(\d+)[_\-]?(.*)$', re.IGNORECASE)

def parse_filename(filename):
    """Return (display_title, sort_key) parsed from the filename."""
    base = os.path.splitext(filename)[0]
    match = FILENAME_PATTERN.match(base)
    if match:
        num, name = match.groups()
        name = name.replace('_', ' ').replace('-', ' ').strip()
        title = f"{num} {name}".strip() if name else num
        return title, int(num)
    # Fallback for files that don't match the numbered pattern:
    # prettify the filename and sort them after all numbered ones.
    title = base.replace('_', ' ').replace('-', ' ').strip().title()
    return title, float('inf')

def build_index():
    html_files = [
        f for f in os.listdir(".")
        if f.endswith(".html") and f not in EXCLUDE
    ]

    # Parse and sort by lecture number
    parsed = [(f, *parse_filename(f)) for f in html_files]
    parsed.sort(key=lambda x: x[2])

    list_items = "\n".join(
        f'    <li><a href="{fname}">{title}</a></li>'
        for fname, title, _ in parsed
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>My Lecture Notes</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; max-width: 820px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #1a1a1a; }}
  h1 {{ font-size: 1.6em; border-bottom: 3px solid #2563eb; padding-bottom: 8px; }}
  ul {{ list-style: none; padding: 0; margin-top: 20px; }}
  li {{ margin: 10px 0; }}
  a {{ text-decoration: none; color: #2563eb; font-size: 1.05em; padding: 10px 14px; display: block; border: 1px solid #e5e7eb; border-radius: 6px; transition: background 0.15s; }}
  a:hover {{ background: #eef2ff; }}
  .meta {{ color: #888; font-size: 0.85em; margin-top: 40px; }}
</style>
</head>
<body>

<h1>My Lecture Notes</h1>

<ul>
{list_items}
</ul>

<p class="meta">Auto-generated on {timestamp} · {len(html_files)} notes</p>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"index.html regenerated with {len(html_files)} notes:")
    for fname, title, key in parsed:
        print(f"  - {fname} -> \"{title}\" (sort key: {key})")

if __name__ == "__main__":
    build_index()
