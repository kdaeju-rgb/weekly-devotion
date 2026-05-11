#!/usr/bin/env python3
"""Generate 5 contemplative images for the devotional series via OpenAI gpt-image-1."""
import os
import base64
from pathlib import Path
from openai import OpenAI

OUT = Path("/Users/csh/Projects/claude-code-md-explainer/devotion-10/img")
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (
    "Minimalist editorial illustration, hand-drawn watercolor quality. "
    "Warm cream background tone (#faf9f5). Single soft coral accent color (#cc785c). "
    "Contemplative meditative mood. Korean church-friendly, suitable for youth devotional. "
    "Generous negative space, magazine editorial composition. "
    "NOT photorealistic, NOT digital art, NOT 3D render. "
    "No text, no letters, no faces visible. "
    "Aspect ratio 16:9, designed to sit in the right half of a slide with text on the left."
)

PROMPTS = {
    "day1": (
        "Two warm hands gently clasped together, representing family bond and unity. "
        "Soft watercolor lines, warm light. " + STYLE
    ),
    "day2": (
        "A simple ceramic bowl in soft watercolor, with golden warmth flowing out of it like quiet light, "
        "representing the exchange of poverty and abundance. Editorial illustration with negative space. "
        + STYLE
    ),
    "day3": (
        "A narrow path through soft dark trees with a single warm coral light at the far end, "
        "representing a hard road already walked through by someone who went first. Charcoal-warm watercolor. "
        + STYLE
    ),
    "day4": (
        "A simple linen garment gently draped, almost weightless, representing a new identity and clothing of righteousness. "
        "Soft cream and coral tones, contemplative. " + STYLE
    ),
    "day5": (
        "An unbroken delicate thread of warm coral light continuing across a soft dark expanse into dawn, "
        "representing love that cannot be severed. Editorial illustration. " + STYLE
    ),
}

def main():
    client = OpenAI()
    print(f"Generating {len(PROMPTS)} images...")
    for name, prompt in PROMPTS.items():
        out_path = OUT / f"{name}.png"
        if out_path.exists():
            print(f"  [skip] {name}.png already exists")
            continue
        print(f"  [gen ] {name}.png ...", flush=True)
        try:
            r = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1536x1024",
                quality="medium",
                n=1,
            )
            b64 = r.data[0].b64_json
            out_path.write_bytes(base64.b64decode(b64))
            print(f"         saved {out_path.stat().st_size // 1024} KB")
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
    print("Done.")

if __name__ == "__main__":
    main()
