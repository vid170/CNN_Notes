#!/usr/bin/env python3
"""
generate_index.py

Scans the current directory for .html lecture note files and
regenerates index.html as a styled list of links to all of them.

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

def get_title(filepath):
    """Try to extract the <title> or <h1> from the HTML file for a nicer label."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(3000)  # only need the head/start
        match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
        if match:
            return re.sub(r"<[^>]+>", "", match.group(1)).strip()
        match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    # Fallback: prettify the filename
    name = os.path.splitext(os.path.basename(filepath))[0]
    return name.replace("_", " ").replace("-", " ").title()

def build_index():
    html_files = sorted(
        f for f in os.listdir(".")
        if f.endswith(".html") and f not in EXCLUDE
    )

    list_items = "\n".join(
        f'    <li><a href="{f}">{get_title(f)}</a></li>'
        for f in html_files
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
    for f in html_files:
        print(f"  - {f} → {get_title(f)}")

if __name__ == "__main__":
    build_index()
