#!/usr/bin/env python3
"""Generate 5 minimal SVG line illustrations + PNG conversions for the devotional series.

Style: single coral stroke (#cc785c) on transparent background, claude.com aesthetic.
Each SVG is 1024×1024 square; PNG output for embedding into PPTX.
"""
import cairosvg
from pathlib import Path

OUT = Path("/Users/csh/Projects/claude-code-md-explainer/devotion-10/img")
OUT.mkdir(parents=True, exist_ok=True)

CORAL = "#cc785c"

SVGS = {
    # Day 1: two intersecting rings — family bond
    "day1": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <circle cx="400" cy="512" r="240" stroke="{CORAL}" stroke-width="5" fill="none"/>
  <circle cx="624" cy="512" r="240" stroke="{CORAL}" stroke-width="5" fill="none" opacity="0.55"/>
</svg>''',

    # Day 2: bowl with rays of warmth — exchange
    "day2": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <path d="M 320 640 Q 512 800 704 640" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <line x1="320" y1="640" x2="290" y2="560" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>
  <line x1="704" y1="640" x2="734" y2="560" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>
  <line x1="512" y1="520" x2="512" y2="300" stroke="{CORAL}" stroke-width="3" stroke-linecap="round" opacity="0.45"/>
  <line x1="412" y1="520" x2="362" y2="340" stroke="{CORAL}" stroke-width="3" stroke-linecap="round" opacity="0.45"/>
  <line x1="612" y1="520" x2="662" y2="340" stroke="{CORAL}" stroke-width="3" stroke-linecap="round" opacity="0.45"/>
</svg>''',

    # Day 3: convergent path with distant light — way through
    "day3": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <line x1="240" y1="920" x2="476" y2="380" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>
  <line x1="784" y1="920" x2="548" y2="380" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>
  <circle cx="512" cy="340" r="46" fill="{CORAL}"/>
  <circle cx="512" cy="340" r="92" stroke="{CORAL}" stroke-width="3" fill="none" opacity="0.4"/>
  <circle cx="512" cy="340" r="138" stroke="{CORAL}" stroke-width="2" fill="none" opacity="0.22"/>
</svg>''',

    # Day 4: draped fabric — new garment / identity
    "day4": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <path d="M 240 200 Q 340 470 270 830" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.45"/>
  <path d="M 408 200 Q 520 480 466 850" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.75"/>
  <path d="M 580 200 Q 690 480 624 850" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.9"/>
  <path d="M 740 200 Q 826 470 758 830" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.55"/>
</svg>''',

    # Day 5: unbroken thread — love that cannot be severed
    "day5": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <path d="M 80 512 C 280 280 480 740 700 512 S 920 280 1000 512"
        stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <circle cx="940" cy="512" r="22" fill="{CORAL}"/>
  <circle cx="940" cy="512" r="50" stroke="{CORAL}" stroke-width="2" fill="none" opacity="0.35"/>
</svg>''',
}

for name, svg in SVGS.items():
    svg_path = OUT / f"{name}.svg"
    png_path = OUT / f"{name}.png"
    svg_path.write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(png_path), output_width=1024, output_height=1024)
    print(f"  generated {name}.svg + {name}.png ({png_path.stat().st_size // 1024} KB)")

print("Done.")
