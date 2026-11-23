#!/usr/bin/env python3
"""Compose the front page (entry.png) from the pixel-art scene and
the day's news text.

Run:  python3 pixel.py && python3 compose.py
Writes entry.png beside this file: 1024x1024, deterministic, no
network, no clock, no randomness. Uses only Pillow and the DejaVu
fonts already on this machine; the entry program (main.py) only
copies the finished image, so the grader needs neither.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
CARD = (255, 255, 255)
GREY = (90, 86, 78)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            trial = (line + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, leading=1.28):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def card(draw, box, accent=RED):
    draw.rectangle(box, fill=CARD, outline=INK, width=2)
    draw.rectangle([box[0], box[1], box[2], box[1] + 8], fill=accent)


def story(draw, box, kicker, headline, body, accent=RED):
    x0, y0, x1, y1 = box
    card(draw, box, accent)
    draw.text((x0 + 16, y0 + 14), kicker, font=font(SANS_B, 16), fill=accent)
    y = para(draw, (x0 + 16, y0 + 38), headline,
             font(SERIF_B, 23), x1 - x0 - 32, leading=1.1)
    para(draw, (x0 + 16, y + 6), body, font(SANS, 15),
         x1 - x0 - 32, fill=(40, 38, 34), leading=1.25)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=4)

    d.rectangle([10, 10, W - 11, 138], fill=INK)
    d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 56),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 96), "ONE IMAGE  •  THE WHOLE DAY'S NEWS",
           font=font(SANS_B, 20), fill=(240, 200, 60), anchor="ma")

    d.text((W // 2, 152), "MONDAY  23  NOVEMBER  2026",
           font=font(SERIF_B, 36), fill=RED, anchor="ma")
    d.line([60, 200, 320, 200], fill=INK, width=2)
    d.line([704, 200, 964, 200], fill=INK, width=2)

    # Lead story: the pixel-art illustration of the burning tanker.
    lead = (28, 216, 996, 568)
    card(d, lead, RED)
    scene = Image.open("scene.png").convert("RGB")
    img.paste(scene, (44, 232))
    d.rectangle([44, 394, 380, 424], fill=(10, 20, 35))
    d.text((56, 400), "STRAIT OF HORMUZ  •  BAHRAIN",
           font=font(SANS_B, 17), fill=(255, 255, 255))
    d.text((46, 448), "LEAD  •  THE GULF WAR WIDENS",
           font=font(SANS_B, 20), fill=RED)
    d.text((46, 478), "IRAN HITS U.S. BASES AND GULF TANKERS",
           font=font(SERIF_B, 32), fill=INK)
    para(d, (46, 512),
         "Iran fired missiles and drones at U.S. positions in Bahrain and "
         "struck tankers in the Strait of Hormuz. Trump: Iran wants a deal "
         "— but not one “acceptable” to him.",
         font(SANS, 19), 920, fill=(40, 38, 34), leading=1.28)

    gx, gy, gw, gh, gap = 28, 584, 474, 148, 20
    stories = [
        ("CLIMATE  •  COP31, TURKEY",
         "CLIMATE TALKS\nCOLLAPSE",
         "COP31 in Antalya ends with no deal after the longest "
         "climate summit ever.",
         RED),
        ("WAR IN UKRAINE",
         "STRIKES KILL 15;\nA WARSHIP SINKS",
         "Russian strikes kill 15 in Dymer, near Kyiv. Ukraine "
         "says sea drones sank a Russian warship in Libya.",
         NAVY),
        ("GAZA",
         "GAZA: A TOXIC\nWASTELAND",
         "An Israeli strike kills three in Gaza. Oxfam finds "
         "toxic contamination across 99% of the territory.",
         RED),
        ("U.S. POLITICS",
         "DEMOCRATS WIN\nBIG IN THE HOUSE",
         "Democrats take their largest House majority in decades "
         "— at least 258 seats.",
         NAVY),
    ]
    for i, (kicker, head, body, accent) in enumerate(stories):
        box = (gx + (i % 2) * (gw + gap), gy + (i // 2) * (gh + gap),
               gx + (i % 2) * (gw + gap) + gw, gy + (i // 2) * (gh + gap) + gh)
        story(d, box, kicker, head, body, accent)

    also = (28, 908, 996, 988)
    card(d, also, NAVY)
    d.text((46, 920), "ALSO TODAY", font=font(SANS_B, 19), fill=NAVY)
    para(d, (46, 944),
         "Mexico captures Sinaloa cartel boss “Chapo Isidro”  •  "
         "Indonesia candy-factory fire kills 3  •  "
         "South Korea minister quits in AI exam scandal",
         font(SANS, 17), 932, fill=(40, 38, 34), leading=1.3)

    d.text((W // 2, 996), "SUMMED UP IN ONE IMAGE  •  23 NOVEMBER 2026",
           font=font(SANS_B, 17), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
