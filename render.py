#!/usr/bin/env python3
"""Render the news-image-20261125 entry: a 1024x1024 newspaper front page
summing up world news of Wednesday 25 November 2026.

Run: python3 render.py  -> writes entry.png next to this file.
Deterministic: fixed layout, fixed text, fixed palette; no randomness,
no network, no timestamps in the output.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
NAVY = (16, 38, 63)
NAVY_LT = (30, 58, 88)
RED = (179, 39, 30)
GOLD = (232, 199, 102)
INK = (24, 24, 24)
GREY = (90, 90, 90)
SEA = (20, 50, 74)
SKY = (44, 62, 85)
ORANGE = (232, 151, 63)
YELLOW = (245, 196, 66)
PURPLE = (106, 46, 122)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill, x0=0, x1=W):
    tw = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)


def burst(draw, cx, cy, r1, r2, n, fill):
    """Jagged starburst polygon centred on (cx, cy)."""
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_sea_scene(draw, x0, y0, x1, y1):
    """Lead art: a cargo ship at dusk, struck by a drone, exploding."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # dusk band on the horizon
    draw.rectangle([x0, y1 - 90, x1, y1 - 55], fill=(214, 128, 58))
    draw.rectangle([x0, y1 - 55, x1, y1], fill=SEA)
    # waves
    for i, wx in enumerate(range(x0 + 10, x1 - 10, 46)):
        wy = y1 - 34 + (i % 2) * 10
        draw.arc([wx, wy, wx + 44, wy + 16], 180, 360, fill=(120, 170, 205), width=3)
    # ship silhouette (dark hull + superstructure)
    hx0, hx1 = x0 + 120, x0 + 560
    hy = y1 - 78
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 46, hy + 46), (hx0 + 18, hy + 46)],
                 fill=(12, 20, 30))
    draw.rectangle([hx0 + 150, hy - 52, hx0 + 330, hy], fill=(12, 20, 30))
    draw.rectangle([hx0 + 210, hy - 88, hx0 + 260, hy - 52], fill=(12, 20, 30))
    draw.rectangle([hx0 + 300, hy - 70, hx0 + 312, hy - 52], fill=(12, 20, 30))
    # containers
    for i, cx in enumerate(range(hx0 + 40, hx0 + 140, 34)):
        draw.rectangle([cx, hy - 26, cx + 30, hy], fill=(150, 60, 40) if i % 2 else (60, 110, 90))
    # explosion above the stern
    ex, ey = hx0 + 60, hy - 110
    burst(draw, ex, ey, 74, 30, 10, ORANGE)
    burst(draw, ex, ey, 46, 18, 10, YELLOW)
    burst(draw, ex, ey, 22, 9, 8, (255, 240, 180))
    # smoke puffs
    for sx, sy, sr in [(ex - 66, ey - 46, 26), (ex + 58, ey - 58, 30),
                       (ex + 96, ey - 20, 22), (ex - 96, ey - 8, 20)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(70, 74, 80))
    # small drone in the sky
    dx, dy = x1 - 130, y0 + 52
    draw.ellipse([dx - 22, dy - 8, dx + 22, dy + 8], fill=(16, 16, 16))
    draw.line([dx - 34, dy - 16, dx - 14, dy - 4], fill=(16, 16, 16), width=3)
    draw.line([dx + 14, dy - 4, dx + 34, dy - 16], fill=(16, 16, 16), width=3)
    draw.ellipse([dx - 40, dy - 22, dx - 28, dy - 12], fill=(16, 16, 16))
    draw.ellipse([dx + 28, dy - 22, dx + 40, dy - 12], fill=(16, 16, 16))
    # gulls
    for gx, gy in [(x0 + 700, y0 + 60), (x0 + 760, y0 + 90), (x0 + 660, y0 + 110)]:
        draw.arc([gx, gy, gx + 18, gy + 10], 200, 340, fill=(20, 20, 20), width=3)
        draw.arc([gx + 18, gy, gx + 36, gy + 10], 200, 340, fill=(20, 20, 20), width=3)


def draw_tower(draw, x0, y0, x1, y1):
    """Riyadh tower at dusk, struck at the top."""
    draw.rectangle([x0, y0, x1, y1], fill=(58, 44, 66))
    draw.rectangle([x0, y1 - 70, x1, y1], fill=(38, 30, 44))
    # tower: tapering silhouette with a pointed top
    tx = (x0 + x1) // 2
    draw.polygon([(tx - 52, y1 - 70), (tx - 30, y0 + 46), (tx + 30, y0 + 46),
                  (tx + 52, y1 - 70)], fill=(18, 16, 24))
    draw.polygon([(tx - 30, y0 + 46), (tx, y0 + 8), (tx + 30, y0 + 46)], fill=(18, 16, 24))
    # lit windows
    for wy in range(y0 + 70, y1 - 84, 22):
        for wx in (-18, 0, 18):
            draw.rectangle([tx + wx - 5, wy, tx + wx + 5, wy + 9],
                           fill=(240, 200, 90))
    # blast at the crown
    burst(draw, tx, y0 + 40, 34, 14, 9, ORANGE)
    burst(draw, tx, y0 + 40, 20, 8, 9, YELLOW)
    # ground line
    draw.rectangle([x0, y1 - 70, x1, y1 - 66], fill=(120, 90, 110))


def draw_court(draw, x0, y0, x1, y1):
    """Courthouse pediment and columns (Huawei verdict)."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 226, 210))
    cx = (x0 + x1) // 2
    # pediment (apex up)
    draw.polygon([(cx - 62, y0 + 66), (cx + 62, y0 + 66), (cx, y0 + 26)],
                 fill=NAVY)
    # columns
    for i in range(4):
        colx = x0 + 22 + i * 30
        draw.rectangle([colx, y0 + 76, colx + 14, y1 - 34], fill=NAVY)
    # base and steps
    draw.rectangle([x0 + 12, y1 - 34, x1 - 12, y1 - 26], fill=NAVY)
    draw.rectangle([x0 + 6, y1 - 24, x1 - 6, y1 - 16], fill=(120, 120, 120))
    # gavel: head + handle
    draw.line([x0 + 96, y0 + 96, x0 + 128, y0 + 128], fill=RED, width=7)
    draw.rectangle([x0 + 88, y0 + 84, x0 + 112, y0 + 104], fill=RED)


def draw_turkey(draw, x0, y0, x1, y1):
    """Flat-style turkey for the Thanksgiving pardon."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 222, 190))
    cx, cy = (x0 + x1) // 2, y1 - 62
    # fanned tail
    for i, ang in enumerate(range(-60, 61, 24)):
        a = math.radians(ang - 90)
        ex = cx + 62 * math.cos(a)
        ey = cy - 26 + 62 * math.sin(a)
        draw.line([cx, cy - 20, ex, ey], fill=(150, 90, 40), width=12)
        draw.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=(120, 60, 30))
    # body
    draw.ellipse([cx - 40, cy - 34, cx + 40, cy + 34], fill=(122, 74, 38))
    # wing
    draw.ellipse([cx - 30, cy - 12, cx + 6, cy + 22], fill=(96, 56, 28))
    # neck + head
    draw.line([cx + 26, cy - 24, cx + 40, cy - 62], fill=(122, 74, 38), width=12)
    draw.ellipse([cx + 28, cy - 78, cx + 54, cy - 52], fill=(122, 74, 38))
    # beak + wattle
    draw.polygon([(cx + 52, cy - 66), (cx + 68, cy - 60), (cx + 52, cy - 58)],
                 fill=(230, 150, 40))
    draw.ellipse([cx + 38, cy - 52, cx + 46, cy - 38], fill=RED)


def draw_quake(draw, x0, y0, x1, y1):
    """Himalayan peaks under a seismograph trace (Nepal quake)."""
    draw.rectangle([x0, y0, x1, y1], fill=(206, 222, 232))
    # mountains
    draw.polygon([(x0, y1), (x0 + 34, y0 + 66), (x0 + 74, y1)], fill=(70, 90, 110))
    draw.polygon([(x0 + 44, y1), (x0 + 96, y0 + 34), (x0 + 150, y1)],
                 fill=(46, 66, 88))
    # snow caps
    draw.polygon([(x0 + 26, y0 + 80), (x0 + 34, y0 + 66), (x0 + 42, y0 + 80)],
                 fill=(255, 255, 255))
    draw.polygon([(x0 + 84, y0 + 54), (x0 + 96, y0 + 34), (x0 + 108, y0 + 54)],
                 fill=(255, 255, 255))
    # crack in the ground
    draw.line([(x0 + 10, y1 - 26), (x0 + 44, y1 - 38), (x0 + 70, y1 - 24),
               (x0 + 104, y1 - 40), (x0 + 140, y1 - 26)], fill=(60, 50, 44), width=4)
    # seismograph trace across the sky
    pts = [(x0 + 8, y0 + 34), (x0 + 30, y0 + 34), (x0 + 40, y0 + 18),
           (x0 + 50, y0 + 52), (x0 + 60, y0 + 26), (x0 + 72, y0 + 44),
           (x0 + 84, y0 + 20), (x0 + 96, y0 + 56), (x0 + 106, y0 + 30),
           (x0 + 118, y0 + 40), (x0 + 142, y0 + 40)]
    draw.line(pts, fill=RED, width=4, joint="curve")


def panel(draw, x0, y0, x1, y1, art_fn, kicker, headline, sub):
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255),
                   outline=NAVY, width=2)
    art_fn(draw, x0 + 2, y0 + 2, x0 + 152, y1 - 2)
    tx = x0 + 166
    tw = x1 - tx - 12
    draw.text((tx, y0 + 12), kicker, font=SANS_B(17), fill=RED)
    y = y0 + 36
    for line in wrap(draw, headline, SANS_B(27), tw):
        draw.text((tx, y), line, font=SANS_B(27), fill=INK)
        y += 32
    for line in wrap(draw, sub, SANS(19), tw):
        draw.text((tx, y + 2), line, font=SANS(19), fill=GREY)
        y += 24


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 116, W, 122], fill=GOLD)
    center(d, 18, "THE WORLD IN ONE IMAGE", SERIF_B(56), (255, 255, 255))
    center(d, 80, "WEDNESDAY  •  25 NOVEMBER 2026", SANS_B(27), GOLD)

    # ---- lead story: sea strike ----
    d.rectangle([24, 136, 1000, 500], fill=(255, 255, 255), outline=NAVY, width=2)
    draw_sea_scene(d, 26, 138, 998, 386)
    d.text((40, 398), "UKRAINE HITS RUSSIAN SHIPS AT SEA", font=SANS_B(40), fill=INK)
    d.text((40, 448), "Zelenskyy confirms drone strikes in the Gulf of Finland and off Libya —",
           font=SANS(22), fill=GREY)
    d.text((40, 474), "Putin vows retaliation after attacks on Russian oil plants.",
           font=SANS(22), fill=GREY)

    # ---- four stories, 2 x 2 ----
    cells = [
        (24, 516, draw_tower, "MIDDLE EAST",
         "HOUTHIS STRIKE RIYADH TOWER",
         "Missile hits the capital's tallest tower; 11 wounded."),
        (512, 516, draw_court, "UNITED STATES",
         "HUAWEI CONVICTED IN U.S. COURT",
         "Jury finds the Chinese firm guilty over Iran business."),
        (24, 724, draw_turkey, "WASHINGTON",
         "TRUMP PARDONS THE TURKEYS",
         "\u201cFreedom\u201d and \u201cFeathers\u201d spared at the Thanksgiving ceremony."),
        (512, 724, draw_quake, "ASIA",
         "QUAKE SHAKES NEPAL",
         "5.6-magnitude tremor hits Koshi Province near the China border."),
    ]
    for x0, y0, fn, kick, head, sub in cells:
        panel(d, x0, y0, x0 + 488, y0 + 192, fn, kick, head, sub)

    # ---- ribbon: the day's observance ----
    d.rectangle([24, 932, 1000, 978], fill=PURPLE)
    center(d, 946, "ALSO TODAY — INTERNATIONAL DAY TO END VIOLENCE AGAINST WOMEN",
           SANS_B(18), (255, 255, 255))

    # ---- footer ----
    center(d, 990, "WORLD NEWS  •  WEDNESDAY 25 NOVEMBER 2026  •  SOURCES: REUTERS, RFE/RL",
           SANS(15), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
