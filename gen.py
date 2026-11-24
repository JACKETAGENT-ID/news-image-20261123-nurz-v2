#!/usr/bin/env python3
"""Draw entry.png: a globe-centred 'news radar' for Monday 23 November 2026.

Six story tiles orbit a stylised globe under one big date banner.
Pillow + system DejaVu fonts only; no network, no downloaded images.
Deterministic: fixed shapes, fixed text, no timestamps, no randomness.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.environ.get("GEN_OUT", "entry.png")

NAVY = (11, 29, 51)
PANEL = (16, 44, 74)
PANEL_EDGE = (58, 110, 158)
INK = (240, 244, 248)
MUTED = (176, 196, 214)
RED = (214, 48, 49)
GOLD = (232, 180, 60)
OCEAN = (30, 111, 168)
LAND = (86, 168, 110)
LAND2 = (64, 140, 120)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
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


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN, outline=(120, 190, 230), width=4)
    # Abstract continents: rough polygons, deliberately simplified.
    d.polygon([(cx - 118, cy - 30), (cx - 78, cy - 72), (cx - 52, cy - 58),
               (cx - 58, cy - 8), (cx - 84, cy + 18), (cx - 108, cy + 6)], fill=LAND)
    d.polygon([(cx - 96, cy + 52), (cx - 70, cy + 44), (cx - 62, cy + 78),
               (cx - 88, cy + 92), (cx - 104, cy + 74)], fill=LAND)
    d.polygon([(cx - 30, cy - 82), (cx + 6, cy - 96), (cx + 34, cy - 70),
               (cx + 26, cy - 34), (cx - 6, cy - 40), (cx - 26, cy - 58)], fill=LAND2)
    d.polygon([(cx + 8, cy - 6), (cx + 52, cy - 22), (cx + 78, cy + 6),
               (cx + 58, cy + 44), (cx + 22, cy + 52), (cx + 2, cy + 26)], fill=LAND)
    d.polygon([(cx + 66, cy + 66), (cx + 104, cy + 58), (cx + 112, cy + 88),
               (cx + 84, cy + 104), (cx + 62, cy + 92)], fill=LAND2)
    # Latitude / longitude hints.
    d.ellipse([cx - r, cy - 26, cx + r, cy + 26], outline=(255, 255, 255, 90), width=2)
    d.ellipse([cx - 52, cy - r, cx + 52, cy + r], outline=(255, 255, 255, 90), width=2)
    # Orbit ring with three satellite dots.
    d.ellipse([cx - r - 34, cy - r - 34, cx + r + 34, cy + r + 34],
              outline=(232, 180, 60), width=3)
    for ang in (35, 155, 285):
        a = math.radians(ang)
        x = cx + int((r + 34) * math.cos(a))
        y = cy + int((r + 34) * math.sin(a))
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=GOLD, outline=NAVY, width=2)


def tile(d, x, y, w, h, accent, kicker, headline, body):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                        outline=PANEL_EDGE, width=2)
    d.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)
    d.text((x + 16, y + 20), kicker, font=F_SANS_B(16), fill=accent)
    hl = wrap(d, headline, F_SANS_B(26), w - 32)
    ty = y + 46
    for line in hl:
        d.text((x + 16, ty), line, font=F_SANS_B(26), fill=INK)
        ty += 30
    bl = wrap(d, body, F_SANS(19), w - 32)
    for line in bl[:3]:
        d.text((x + 16, ty + 6), line, font=F_SANS(19), fill=MUTED)
        ty += 23


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    # Faint dot grid.
    for gx in range(24, W, 48):
        for gy in range(24, H, 48):
            d.ellipse([gx, gy, gx + 2, gy + 2], fill=(24, 58, 96))

    # ---- Masthead ----
    d.text((48, 26), "THE WORLD TODAY  •  NEWS RADAR", font=F_SANS_B(24), fill=GOLD)
    d.text((48, 58), "MONDAY 23 NOVEMBER 2026", font=F_SERIF_B(44), fill=INK)
    d.rectangle([48, 132, 976, 138], fill=RED)
    d.text((48, 150), "Six stories that defined the day — from Antalya to Anfield",
           font=F_SANS(24), fill=MUTED)

    # ---- Globe (centre) ----
    draw_globe(d, 512, 330, 118)
    d.text((48, 196), "COP31\nANTALYA", font=F_SANS_B(20), fill=(150, 200, 240),
           align="left")
    d.text((800, 196), "WAR IN\nEUROPE", font=F_SANS_B(20), fill=(150, 200, 240),
           align="right")
    d.text((48, 400), "GULF\nTENSIONS", font=F_SANS_B(20), fill=(150, 200, 240))
    d.text((800, 400), "SPORT\n& MONEY", font=F_SANS_B(20), fill=(150, 200, 240),
           align="right")

    # ---- Six story tiles: 3 x 2 ----
    tiles = [
        ((214, 48, 49), "CLIMATE  •  ANTALYA, TURKEY",
         "COP31 TALKS COLLAPSE",
         "EU rejects a deal with no fossil-fuel phase-out; no agreement at all."),
        ((232, 180, 60), "WAR  •  KYIV REGION, UKRAINE",
         "14 DEAD IN KYIV REGION",
         "Russian drone hits flats in Dymer; a boy, 7, is pulled alive from the rubble."),
        ((90, 170, 230), "WAR AT SEA  •  BENGHAZI, LIBYA",
         "WARSHIP SUNK OFF LIBYA",
         "Ukrainian sea drones hit Russian corvette Merkury and cargo ship Angara."),
        ((230, 120, 60), "GULF  •  RED SEA & BAHRAIN",
         "GULF STRIKES WIDEN",
         "Houthis claim a Saudi refinery hit; Iran strikes Bahrain; oil holds near $92 a barrel."),
        ((86, 168, 110), "SPORT  •  ENGLAND & TURIN",
         "LIVERPOOL 4–0 UNITED",
         "Pochettino's debut ends in a rout at Anfield; Alcaraz wins his first ATP Finals."),
        ((170, 130, 200), "WORLD  •  JAVA & ZURICH",
         "24 DEAD IN JAVA FACTORY FIRE",
         "FIFA confirms UK as 2035 Women's World Cup host; gold above $3,600."),
    ]
    tw, th, gap = 304, 204, 16
    x0, y0 = 40, 480
    for i, (accent, kicker, head, body) in enumerate(tiles):
        x = x0 + (i % 3) * (tw + gap)
        y = y0 + (i // 3) * (th + gap)
        tile(d, x, y, tw, th, accent, kicker, head, body)

    # ---- Bottom ticker ----
    d.rectangle([0, 926, W, H], fill=(120, 20, 22))
    d.text((40, 944), "ALSO TODAY", font=F_SANS_B(22), fill=GOLD)
    d.text((40, 972), "US extradition order for 'El Chapo Isidro'  •  2031 Women's World Cup: USA & Mexico",
           font=F_SANS(21), fill=INK)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
