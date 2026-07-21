#!/usr/bin/env python3
"""Compose the stats card and the top-languages card into one unified SVG that
shares a single gradient background and border. Each source card is embedded as
a nested <svg> so its internal layout, styles and animations are preserved; only
each card's own background rect and (now-unused) gradient <defs> are removed.

Usage: compose_card.py <stats.svg> <top-langs.svg> <out.svg>
"""
import re
import sys

STATS = sys.argv[1] if len(sys.argv) > 1 else "github-stats.svg"
LANGS = sys.argv[2] if len(sys.argv) > 2 else "github-top-langs.svg"
OUT = sys.argv[3] if len(sys.argv) > 3 else "github-stats-card.svg"

GAP = -24  # overlap the two cards' stacked paddings for a tighter single card


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def outer_dims(svg):
    head = svg[: svg.index(">", svg.index("<svg")) + 1]
    w = int(re.search(r'width="(\d+)"', head).group(1))
    h = int(re.search(r'height="(\d+)"', head).group(1))
    return w, h


def inner_content(svg):
    start = svg.index(">", svg.index("<svg")) + 1
    end = svg.rindex("</svg>")
    inner = svg[start:end]
    inner = re.sub(r'<rect\s+data-testid="card-bg".*?/>', "", inner, flags=re.S)
    inner = re.sub(r"<defs>.*?</defs>", "", inner, flags=re.S)
    return inner


stats, langs = read(STATS), read(LANGS)
sw, sh = outer_dims(stats)
lw, lh = outer_dims(langs)

W = max(sw, lw)
H = sh + GAP + lh
lx = (W - lw) // 2   # centre the narrower languages card
ly = sh + GAP

combined = f"""<svg
  width="{W}"
  height="{H}"
  viewBox="0 0 {W} {H}"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label="GitHub stats and most used languages"
>
  <defs>
    <linearGradient id="unified-card-bg" gradientTransform="rotate(30)" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#e96443" />
      <stop offset="100%" stop-color="#904e95" />
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" rx="4.5" width="{W - 1}" height="{H - 1}" fill="url(#unified-card-bg)" stroke="#e4e2e2" stroke-opacity="1.0" />
  <svg x="0" y="0" width="{sw}" height="{sh}" viewBox="0 0 {sw} {sh}">{inner_content(stats)}</svg>
  <svg x="{lx}" y="{ly}" width="{lw}" height="{lh}" viewBox="0 0 {lw} {lh}">{inner_content(langs)}</svg>
</svg>
"""

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(combined)
print(f"combined: {W}x{H}  |  stats {sw}x{sh}@(0,0)  langs {lw}x{lh}@({lx},{ly})")
