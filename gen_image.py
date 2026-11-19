#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

One image, six stories, drawn with Pillow. Run: python3 gen_image.py
Writes entry.png next to this file. Kept in the repo so the picture is
reproducible; the graded program (main.ts) only copies entry.png.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 42, 68)
NAVY2 = (21, 58, 92)
RED = (178, 34, 34)
PAPER = (247, 243, 234)
INK = (24, 24, 24)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
GOLD = (201, 162, 39)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, kind, cx, cy, r, color):
    """Small geometric pictogram inside a coloured disc."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    fg = WHITE
    if kind == "summit":  # three flags
        for i, dx in enumerate((-24, 0, 24)):
            draw.line([(cx + dx, cy - 22), (cx + dx, cy + 22)], fill=fg, width=4)
            draw.polygon([(cx + dx, cy - 22), (cx + dx + 16, cy - 16),
                          (cx + dx, cy - 10)], fill=fg)
    elif kind == "bridge":  # bridge arch over water
        draw.arc([cx - 30, cy - 18, cx + 30, cy + 26], 180, 360, fill=fg, width=6)
        draw.line([(cx - 34, cy + 8), (cx + 34, cy + 8)], fill=fg, width=5)
        draw.line([(cx - 30, cy - 2), (cx - 30, cy + 8)], fill=fg, width=4)
        draw.line([(cx + 30, cy - 2), (cx + 30, cy + 8)], fill=fg, width=4)
        draw.line([(cx - 34, cy + 22), (cx + 34, cy + 22)], fill=fg, width=3)
    elif kind == "scales":  # scales of justice
        draw.line([(cx, cy - 24), (cx, cy + 22)], fill=fg, width=5)
        draw.line([(cx - 24, cy - 16), (cx + 24, cy - 16)], fill=fg, width=5)
        draw.line([(cx - 24, cy - 16), (cx - 30, cy + 6)], fill=fg, width=4)
        draw.line([(cx - 24, cy - 16), (cx - 18, cy + 6)], fill=fg, width=4)
        draw.arc([cx - 32, cy - 2, cx - 16, cy + 14], 0, 180, fill=fg, width=4)
        draw.line([(cx + 24, cy - 16), (cx + 30, cy + 6)], fill=fg, width=4)
        draw.line([(cx + 24, cy - 16), (cx + 18, cy + 6)], fill=fg, width=4)
        draw.arc([cx + 16, cy - 2, cx + 32, cy + 14], 0, 180, fill=fg, width=4)
        draw.line([(cx - 12, cy + 22), (cx + 12, cy + 22)], fill=fg, width=5)
    elif kind == "chart":  # rising bars + arrow
        for i, h in enumerate((14, 24, 34)):
            x0 = cx - 26 + i * 18
            draw.rectangle([x0, cy + 22 - h, x0 + 12, cy + 22], fill=fg)
        draw.line([(cx - 28, cy - 8), (cx - 6, cy - 18), (cx + 8, cy - 26),
                   (cx + 28, cy - 30)], fill=fg, width=5)
        draw.polygon([(cx + 28, cy - 30), (cx + 16, cy - 30), (cx + 28, cy - 18)],
                     fill=fg)
    elif kind == "flame":  # flame
        draw.polygon([(cx, cy - 28), (cx + 16, cy - 6), (cx + 10, cy + 8),
                      (cx + 20, cy + 2), (cx + 12, cy + 24), (cx - 12, cy + 24),
                      (cx - 20, cy + 2), (cx - 10, cy + 8), (cx - 16, cy - 6)],
                     fill=fg)
    elif kind == "leaf":  # leaf / globe
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=fg, width=5)
        draw.line([(cx - 24, cy), (cx + 24, cy)], fill=fg, width=4)
        draw.arc([cx - 12, cy - 24, cx + 12, cy + 24], 270, 90, fill=fg, width=4)
        draw.arc([cx - 12, cy - 24, cx + 12, cy + 24], 90, 270, fill=fg, width=4)


STORIES = [
    ("ASIA", (150, 96, 0), "summit",
     "Trump, Xi and Putin hold\nfirst three-way summit",
     "The leaders of the US, China and Russia met in Shenzhen, on the "
     "sidelines of APEC, to talk nuclear arms, Ukraine and trade."),
    ("UKRAINE", (21, 58, 92), "bridge",
     "Third strike in four days\nhalts Kerch Bridge rail",
     "An overnight drone attack halted trains on the bridge to "
     "Crimea. Russia said no one was hurt; services were due back by 4 p.m."),
    ("JUSTICE", (120, 40, 140), "scales",
     "ICJ: Myanmar guilty of\nRohingya genocide",
     "The ICJ ruled 9-6 that Myanmar's 2017 crackdown was genocide. "
     "The final judgment cannot be appealed."),
    ("MARKETS", (34, 110, 70), "chart",
     "Anthropic debuts on\nNasdaq as ANT",
     "The Claude maker's shares start trading today after a record "
     "$81.3bn offering priced at $83, above its $70-$78 range."),
    ("BANGLADESH", (178, 34, 34), "flame",
     "Unrest spreads as\nYunus home is torched",
     "Unrest spread to 28 districts as the ancestral home of interim "
     "leader Muhammad Yunus was set ablaze amid protests."),
    ("CLIMATE", (34, 110, 110), "leaf",
     "COP31 ministers race to\nunblock talks in Antalya",
     "Ministers met in informal session to bridge gaps and agree a final "
     "text before the summit closes."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=RED)
    d.text((32, 14), "THE WORLD IN ONE DAY",
           font=font(SANS_B, 26), fill=GOLD)
    d.text((32, 48), "THURSDAY, 19 NOVEMBER 2026",
           font=font(SERIF_B, 46), fill=WHITE)
    d.text((32, 116), "Six stories that defined the day  •  From Shenzhen to The Hague",
           font=font(SANS, 24), fill=(200, 210, 220))

    # --- story grid: 2 cols x 3 rows ---
    mx, my, gap = 16, 170, 16
    cw = (W - 2 * mx - gap) // 2
    ch = 238
    for i, (kicker, color, icon, head, body) in enumerate(STORIES):
        x = mx + (i % 2) * (cw + gap)
        y = my + (i // 2) * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=WHITE,
                    outline=(210, 205, 195), width=2)
        d.rectangle([x, y, x + cw, y + 8], fill=color)
        d.text((x + 16, y + 20), kicker, font=font(SANS_B, 20), fill=color)
        draw_icon(d, icon, x + cw - 52, y + 52, 36, color)
        hy = y + 48
        for line in head.split("\n"):
            d.text((x + 16, hy), line, font=font(SANS_B, 27), fill=INK)
            hy += 34
        by = hy + 10
        for line in wrap(d, body, font(SANS, 20), cw - 32):
            d.text((x + 16, by), line, font=font(SANS, 20), fill=(60, 60, 60))
            by += 27

    # --- footer ticker ---
    d.rectangle([0, 948, W, H], fill=NAVY2)
    d.text((32, 956), "ALSO TODAY:",
           font=font(SANS_B, 20), fill=GOLD)
    d.text((196, 957), "Houthi missile damages Saudi wealth fund tower in Riyadh",
           font=font(SANS, 17), fill=WHITE)
    d.text((32, 980), "Israel launches ground operation near Nuseirat  •  IAEA: North "
           "Korea expanded uranium enrichment",
           font=font(SANS, 17), fill=WHITE)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
