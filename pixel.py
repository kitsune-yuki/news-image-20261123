#!/usr/bin/env python3
"""Draw the lead illustration as pixel art and save it as scene.png.

The scene is drawn on a tiny 234x48 grid, one pixel at a time, with a
small dusk palette, then scaled up with NEAREST so every pixel stays
crisp. Deterministic: a fixed seed, no network, no clock.

Run:  python3 pixel.py
Writes scene.png beside this file: 936x192.
"""
import random

from PIL import Image, ImageDraw

GW, GH = 234, 48
PX = 4

NAVY = (22, 32, 64)
DUSK1 = (58, 52, 96)
DUSK2 = (110, 62, 110)
DUSK3 = (210, 110, 58)
HORIZON = (255, 140, 50)
SUN = (255, 220, 120)
SEA1 = (52, 102, 132)
SEA2 = (36, 74, 106)
SEA3 = (12, 30, 52)
WAVE = (150, 200, 230)
CLOUD = (35, 44, 66)
CLOUD2 = (29, 31, 51)
HULL1 = (138, 51, 32)
HULL2 = (92, 31, 18)
HULL3 = (42, 14, 7)
RUST = (122, 58, 26)
DECK = (92, 85, 75)
RAIL = (138, 133, 120)
CREAM = (242, 234, 216)
CREAM_D = (184, 171, 144)
LIT = (255, 215, 106)
DARK_WIN = (28, 42, 58)
FUNNEL = (194, 59, 46)
BLACK = (18, 18, 18)
SMOKE1 = (34, 34, 34)
SMOKE2 = (58, 58, 58)
SMOKE3 = (85, 85, 85)
SMOKE4 = (119, 119, 119)
FIRE1 = (255, 90, 0)
FIRE2 = (255, 154, 31)
FIRE3 = (255, 210, 60)
FIRE4 = (255, 248, 208)
CHAR = (26, 26, 26)
YEL = (250, 210, 60)
REDC = (214, 70, 45)
BLUC = (70, 120, 205)
GRN = (110, 190, 90)
WHT = (245, 240, 228)

CONTAINERS = [YEL, GRN, REDC, BLUC, YEL, WHT]


def main():
    img = Image.new("RGB", (GW, GH), NAVY)
    d = ImageDraw.Draw(img)
    rnd = random.Random(42)

    def px(x, y, c):
        if 0 <= x < GW and 0 <= y < GH:
            img.putpixel((x, y), c)

    def rect(x0, y0, x1, y1, c):
        d.rectangle([x0, y0, x1, y1], fill=c)

    def dither_row(y, c1, c2):
        for x in range(GW):
            px(x, y, c1 if (x + y) % 2 == 0 else c2)

    # Sky bands, dusk from navy at the top to orange at the horizon.
    for y in range(0, 5):
        rect(0, y, GW - 1, y, NAVY)
    for y in range(5, 10):
        rect(0, y, GW - 1, y, DUSK1)
    dither_row(9, DUSK1, DUSK2)
    for y in range(10, 15):
        rect(0, y, GW - 1, y, DUSK2)
    dither_row(14, DUSK2, DUSK3)
    for y in range(15, 19):
        rect(0, y, GW - 1, y, DUSK3)
    dither_row(19, DUSK3, HORIZON)
    rect(0, 20, GW - 1, 20, HORIZON)

    # Sun, low on the left, with a sparse glow.
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            if abs(dx) + abs(dy) <= 7:
                px(24 + dx, 15 + dy, (255, 154, 60))
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            if abs(dx) + abs(dy) <= 5:
                px(24 + dx, 15 + dy, SUN)
    px(24, 15, FIRE4)

    # Storm clouds, dark blobs with dithered edges.
    for cx, cy, rx, ry, c in [
        (80, 6, 22, 3, CLOUD), (150, 5, 26, 3, CLOUD2),
        (55, 8, 16, 2, CLOUD2), (190, 7, 18, 2, CLOUD),
        (120, 9, 20, 2, CLOUD),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)
    for _ in range(40):
        x = rnd.randint(0, GW - 1)
        y = rnd.randint(2, 10)
        px(x, y, CLOUD if (x + y) % 2 else DUSK1)

    # Birds.
    for bx, by in [(60, 6), (66, 5)]:
        px(bx, by, BLACK)
        px(bx + 1, by + 1, BLACK)
        px(bx + 2, by, BLACK)

    # Mountains on the right horizon.
    for x in range(200, GW):
        h = max(0, 20 - abs(x - 217) // 2)
        for y in range(20 - h, 21):
            px(x, y, (28, 39, 51))

    # Sea.
    for y in range(21, 27):
        rect(0, y, GW - 1, y, SEA1)
    for y in range(27, 36):
        rect(0, y, GW - 1, y, SEA2)
    for y in range(36, GH):
        rect(0, y, GW - 1, y, SEA3)
    for _ in range(130):
        x = rnd.randint(0, GW - 1)
        y = rnd.randint(22, 46)
        px(x, y, WAVE)
        if rnd.random() < 0.5:
            px(x + 1, y, WAVE)

    # Distant warships on the horizon.
    for sx in (20, 222):
        rect(sx, 19, sx + 8, 20, (13, 24, 38))
        px(sx + 2, 18, (13, 24, 38))
        px(sx + 5, 17, (13, 24, 38))

    # A small tugboat crossing on the left.
    rect(8, 38, 22, 41, (20, 20, 26))
    rect(12, 35, 18, 37, CREAM)
    px(14, 36, DARK_WIN)
    px(10, 34, SMOKE3)
    px(11, 33, SMOKE4)
    for x in range(6, 24, 3):
        px(x, 42, WAVE)

    # The tanker: deck, hull, rust streaks, foam at the waterline.
    rect(30, 29, 225, 29, DECK)
    for x in range(33, 224, 8):
        px(x, 28, RAIL)
    for y, c in [(30, HULL1), (31, HULL1), (32, HULL1), (33, HULL2),
                 (34, HULL2), (35, HULL2), (36, HULL2), (37, HULL3),
                 (38, HULL3)]:
        x0 = 30 if y < 34 else 31
        x1 = 225 if y < 34 else 224
        rect(x0, y, x1, y, c)
    for sx in (60, 105, 150):
        for y in range(31, 37):
            if (y + sx) % 2 == 0:
                px(sx, y, RUST)
    for x in (31, 32, 223, 224):
        px(x, 38, (216, 230, 238))
    for x in range(35, 220, 9):
        px(x, 39, WAVE)

    # Containers, each with a light top edge and a dark side.
    for i, col in enumerate(CONTAINERS):
        x0 = 48 + i * 27
        if i >= 4:
            col = CHAR
        rect(x0, 25, x0 + 24, 25, (255, 255, 255) if col is WHT else col)
        rect(x0, 26, x0 + 24, 27, col)
        rect(x0, 28, x0 + 24, 28, (60, 60, 60) if col is CHAR else col)
        px(x0 + 24, 26, BLACK)
        px(x0 + 24, 27, BLACK)
    px(209, 25, FIRE2)
    px(210, 26, FIRE2)

    # Bridge tower with lit and dark windows, funnel and mast.
    rect(34, 22, 48, 28, CREAM)
    rect(34, 28, 48, 28, CREAM_D)
    for wx in (36, 40, 44):
        px(wx, 24, LIT if wx != 40 else DARK_WIN)
        px(wx, 26, DARK_WIN if wx != 40 else LIT)
    rect(30, 24, 33, 28, FUNNEL)
    rect(30, 24, 33, 24, BLACK)
    px(41, 20, BLACK)
    px(41, 19, BLACK)
    px(41, 18, FIRE1)

    # Deck crane.
    for i in range(7):
        px(112 + i, 29 - i, (58, 58, 58))
    px(119, 22, (58, 58, 58))
    px(119, 23, (58, 58, 58))
    rect(118, 24, 120, 26, FUNNEL)

    # Lifeboat on the side.
    rect(56, 31, 64, 32, (255, 122, 26))
    px(56, 31, BLACK)
    px(64, 31, BLACK)

    # Fire: layered flames over the charred containers, with glow.
    for dx in range(-18, 19):
        for dy in range(-10, 11):
            if abs(dx) + abs(dy) <= 17 and rnd.random() < 0.5:
                px(189 + dx, 22 + dy, FIRE2)
    for dx, dy in [(0, 0), (-2, 1), (2, 1), (-4, 2), (4, 2), (-1, -2),
                   (1, -2), (-3, -1), (3, -1), (0, 2), (-5, 3), (5, 3),
                   (-6, 1), (6, 1), (-2, -3), (2, -3), (0, -4)]:
        px(189 + dx, 24 + dy, FIRE1)
    for dx, dy in [(0, 1), (-2, 2), (2, 2), (0, -1), (-1, 0), (1, 0),
                   (-3, 1), (3, 1), (0, 3)]:
        px(189 + dx, 26 + dy, FIRE3)
    for dx, dy in [(0, 0), (-1, 1), (1, 1), (0, 2), (-1, 0), (1, 0)]:
        px(189 + dx, 27 + dy, FIRE4)

    # Warm rim light from the fire on the hull top edge.
    for x in range(168, 216, 2):
        px(x, 30, FIRE2)
    # Lit windows all along the bridge, warmed by the fire.
    for wx in (36, 40, 44):
        px(wx, 24, LIT)
        px(wx, 26, LIT)

    # Smoke: a thick column drifting left as it rises.
    for cx, cy, rx, ry, c in [
        (189, 18, 9, 6, SMOKE1), (185, 14, 10, 6, SMOKE1),
        (181, 10, 11, 6, SMOKE2), (175, 6, 10, 5, SMOKE2),
        (169, 3, 9, 4, SMOKE3), (163, 1, 7, 3, SMOKE3),
        (187, 16, 5, 3, SMOKE2), (179, 12, 5, 3, SMOKE3),
        (173, 8, 4, 3, SMOKE4), (167, 4, 4, 2, SMOKE4),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)
    for _ in range(60):
        x = rnd.randint(150, 205)
        y = rnd.randint(0, 20)
        if rnd.random() < 0.6:
            px(x, y, SMOKE4 if rnd.random() < 0.5 else SMOKE3)
    # Orange rim light on the smoke, on the side facing the fire.
    for x, y in [(193, 18), (194, 16), (192, 14), (190, 12), (188, 10),
                 (195, 20), (193, 22), (186, 8), (184, 6)]:
        px(x, y, FIRE2 if (x + y) % 2 else FIRE1)

    # Missile trails arcing into the fire.
    for i in range(12):
        px(199 + i, 6 + i // 2, FIRE2 if i % 2 else FIRE3)
    for i in range(10):
        px(209 + i, 4 + i // 3, FIRE3 if i % 2 else FIRE2)
    px(199, 6, FIRE4)
    px(209, 4, FIRE4)

    # Fire reflection on the water, fading downward.
    for y in range(30, 47):
        for x in range(180, 200):
            if rnd.random() < max(0.2, 0.85 - (y - 30) * 0.06):
                px(x, y, FIRE2 if (x + y) % 3 else FIRE1)

    big = img.resize((GW * PX, GH * PX), Image.NEAREST)
    big.save("scene.png", format="PNG", optimize=True)
    print("wrote scene.png", big.size)


if __name__ == "__main__":
    main()
