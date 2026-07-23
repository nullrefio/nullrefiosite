# -*- coding: utf-8 -*-
"""Build the Locumfy documentation static site.
Usage: python build.py   (writes *.html into this directory)."""
import os
from _shared import page, FILE_OF
import content_part1 as p1
import content_part2 as p2

ALL_PAGES = [p1.INDEX, p1.ARCHITECTURE, p1.DATA, p1.API] + p2.PART2_PAGES

HERE = os.path.dirname(os.path.abspath(__file__))

for pid, title, crumb, lede, body in ALL_PAGES:
    html = page(pid, title, crumb, lede, body)
    out = os.path.join(HERE, FILE_OF[pid])
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", FILE_OF[pid], f"({len(html):,} bytes)")

print("done:", len(ALL_PAGES), "pages")
