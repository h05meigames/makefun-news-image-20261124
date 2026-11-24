#!/usr/bin/env python3
"""Draw the 24 November 2026 news front page (1024x1024 PNG).

Fresh render for the news-image-20261124 bounty. Pillow only, no network,
no randomness: the same script always writes identical bytes.

Stories (verified by web search on 24 Nov 2026, sources: BBC, Reuters,
The Times of India / Education Times, Jagran Josh, Disclosure News):
- LEAD: Nvidia reinstates CEO Jensen Huang after an affair with an alleged
  spy; Donald Trump says "I made the deal". (BBC)
- UK-EU: Burnham hails a "landmark" UK-EU deal, saying it could make the
  next decade "much better". (BBC)
- Gaza: Israeli attacks have turned Gaza into a "toxic wasteland", Oxfam
  and the Conflict and Environment Observatory say. (BBC / Oxfam)
- Indonesia: factory fire death toll rises to 24; rescuers still search
  for around 30 missing workers. (Times of India / Lexington Herald Leader)
- India-Nepal: India pledges $1.6bn to Nepal in a reset of ties; PM Modi
  and Nepal PM Balendra Shah flag off the Saryu-Kamala Express. (BBC)
- Manchester: US rapper postpones arena shows after the Co-op Live
  evacuation over an unknown substance. (BBC)
- Also today: Carlos Alcaraz wins a maiden ATP Finals title; the World
  Chess Championship begins in Geneva (Gukesh defends vs Sindarov); Max
  Verstappen wins the Las Vegas Grand Prix; the NHS launches the world's
  largest AI breast-cancer screening trial; Tyson Fury reveals a
  schizophrenia diagnosis; BepiColombo enters orbit around Mercury.
"""

import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 246, 227)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
GREEN = (76, 185, 0)
DARKGREEN = (11, 122, 62)
RED = (185, 28, 28)
GOLD = (180, 130, 29)
GREY = (90, 90, 90)
RULE = (26, 26, 26)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36
x0, x1 = M, W - M


def text_w(s, f):
    return d.textlength(s, font=f)


def wrap(s, f, width):
    out = []
    for para in s.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if text_w(trial, f) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


def para(x, y, s, f, width, fill=INK, leading=1.28):
    lh = int(f.size * leading)
    for ln in wrap(s, f, width):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def hline(y, width=2):
    d.line([(x0, y), (x1, y)], fill=RULE, width=width)
    return y + width


def check_y(y, label):
    assert y <= 1010, f"overflow at {label}: y={y}"
    return y


# ---------- top dateline bar ----------
y = 20
f_date = font(SANS_B, 19)
d.text((x0, y), "TUESDAY 24 NOVEMBER 2026", font=f_date, fill=NAVY)
right = "THE DAY IN ONE PICTURE"
d.text((x1 - text_w(right, f_date), y), right, font=f_date, fill=NAVY)
y = check_y(y + 26, "dateline")
y = hline(y, width=3)

# ---------- masthead ----------
y += 4
f_mast = font(SERIF_B, 84)
title = "THE WORLD"
d.text(((W - text_w(title, f_mast)) / 2, y), title, font=f_mast, fill=NAVY)
y = check_y(y + 92, "masthead")
f_tag = font(SERIF, 21)
tag = "Sum up Tuesday's world news in a single image"
d.text(((W - text_w(tag, f_tag)) / 2, y), tag, font=f_tag, fill=GREY)
y = check_y(y + 26, "tagline")
y = hline(y + 2, width=3)

# ---------- LEAD: Nvidia ----------
y += 6
f_kick = font(SANS_B, 19)
d.text((x0, y), "LEAD  •  TECHNOLOGY", font=f_kick, fill=DARKGREEN)
y += 24
lead_top = y
f_lead = font(SERIF_B, 44)
for ln in ["HUANG IS BACK:", "NVIDIA REINSTATES"]:
    d.text((x0, y), ln, font=f_lead, fill=INK)
    y += 50
y += 2
f_sub = font(SERIF, 22)
y = para(x0, y,
         "its chief executive — days after his shock\n"
         "removal over an affair with an alleged spy.",
         f_sub, 560)
y += 6
f_body = font(SANS, 19)
y = para(x0, y,
         "Donald Trump says he brokered the return:\n"
         "\u201cI made the deal.\u201d A week of turmoil ends.",
         f_body, 560)

# chip graphic, right of lead text
gx, gy = 640, lead_top - 4
gw, gh = 316, 168
d.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=18,
                    fill=(18, 38, 32), outline=GREEN, width=4)
for i in range(5):
    px = gx + 40 + i * 56
    d.line([(px, gy - 14), (px, gy)], fill=GREEN, width=6)
    d.line([(px, gy + gh), (px, gy + gh + 14)], fill=GREEN, width=6)
    py = gy + 32 + i * 34
    d.line([(gx - 14, py), (gx, py)], fill=GREEN, width=6)
    d.line([(gx + gw, py), (gx + gw + 14, py)], fill=GREEN, width=6)
f_chip = font(SANS_B, 54)
chip_txt = "NVDA"
d.text((gx + (gw - text_w(chip_txt, f_chip)) / 2, gy + 36),
       chip_txt, font=f_chip, fill=GREEN)
f_chip2 = font(SANS_B, 22)
ct2 = "CEO RETURNS"
d.text((gx + (gw - text_w(ct2, f_chip2)) / 2, gy + 100),
       ct2, font=f_chip2, fill=(253, 246, 227))
f_arrow = font(SANS_B, 18)
at = "\u21a9 U-TURN"
d.text((gx + (gw - text_w(at, f_arrow)) / 2, gy + 134),
       at, font=f_arrow, fill=(255, 120, 90))

y = max(y, gy + gh + 8)
y = check_y(y, "lead")
y = hline(y + 4, width=2)


def panel(x, y, w, kick, headline, body, accent):
    d.text((x, y), kick, font=font(SANS_B, 17), fill=accent)
    y2 = y + 23
    y2 = para(x, y2, headline, font(SERIF_B, 25), w, leading=1.12)
    y2 += 3
    y2 = para(x, y2, body, font(SANS, 17), w, leading=1.28)
    return y2


col_w = (x1 - x0 - 28) // 2

# ---------- Row 2 ----------
y += 6
row2_top = y
end_a = panel(x0, y, col_w, "BRITAIN  •  EUROPE",
              "UK and EU strike\n\u201clandmark\u201d deal",
              "Burnham says the deal could make the\n"
              "next decade \u201cmuch better\u201d.",
              NAVY)
sx, sy = x0 + col_w - 88, row2_top + 56
for i in range(12):
    ang = 2 * math.pi * i / 12 - math.pi / 2
    cx = sx + 40 + int(32 * math.cos(ang))
    cy = sy + 40 + int(32 * math.sin(ang))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)
d.text((sx + 24, sy + 31), "EU", font=font(SANS_B, 24), fill=NAVY)
end_b = panel(x0 + col_w + 28, y, col_w, "GAZA  •  ENVIRONMENT",
              "Gaza a \u201ctoxic\nwasteland\u201d, Oxfam warns",
              "Israeli attacks have left air, soil and\n"
              "water dangerous for decades.",
              RED)
tx, ty = x0 + col_w + 28 + col_w - 92, row2_top + 62
d.polygon([(tx + 40, ty), (tx + 80, ty + 68), (tx, ty + 68)],
          outline=RED, width=5)
d.text((tx + 33, ty + 22), "!", font=font(SANS_B, 36), fill=RED)
y = check_y(max(end_a, end_b) + 8, "row2")
y = hline(y, width=1)

# ---------- Row 3 ----------
y += 6
row3_top = y
end_a = panel(x0, y, col_w, "INDONESIA",
              "Factory fire toll\nrises to 24",
              "Rescuers still search for around 30\n"
              "missing workers in Banten.",
              RED)
fx, fy = x0 + col_w - 80, row3_top + 48
d.polygon([(fx + 32, fy), (fx + 58, fy + 32), (fx + 48, fy + 28),
           (fx + 62, fy + 62), (fx + 32, fy + 82), (fx + 2, fy + 62),
           (fx + 16, fy + 28), (fx + 6, fy + 32)],
          fill=(232, 90, 12))
d.ellipse([fx + 21, fy + 44, fx + 43, fy + 66], fill=(255, 190, 0))
end_b = panel(x0 + col_w + 28, y, col_w, "INDIA  •  NEPAL",
              "India pledges $1.6bn\nto Nepal",
              "Modi and Nepal's PM flag off the\n"
              "Saryu-Kamala Express.",
              DARKGREEN)
mx, my = x0 + col_w + 28 + col_w - 116, row3_top + 52
d.polygon([(mx, my + 72), (mx + 38, my), (mx + 76, my + 72)],
          fill=NAVY)
d.polygon([(mx + 42, my + 72), (mx + 80, my + 12), (mx + 114, my + 72)],
          fill=(70, 90, 130))
d.polygon([(mx + 31, my + 14), (mx + 38, my), (mx + 45, my + 14)],
          fill=(255, 255, 255))
y = check_y(max(end_a, end_b) + 8, "row3")
y = hline(y, width=1)

# ---------- Row 4: Manchester + By numbers ----------
y += 6
row4_top = y
end_a = panel(x0, y, col_w, "MANCHESTER",
              "Arena evacuated;\nrapper postpones shows",
              "Two Co-op Live shows called off after\n"
              "an unknown substance forced a clear-out.",
              NAVY)
bx = x0 + col_w + 28
by = y
bw = col_w
bh = 126
d.rectangle([bx, by, bx + bw, by + bh], outline=NAVY, width=3)
d.rectangle([bx, by, bx + bw, by + 32], fill=NAVY)
d.text((bx + 12, by + 6), "THE DAY BY NUMBERS",
       font=font(SANS_B, 17), fill=(253, 246, 227))
nums = [("24", "dead in the Indonesia factory fire"),
        ("$1.6bn", "India's pledge to Nepal"),
        ("2", "Manchester arena shows postponed"),
        ("1st", "ATP Finals title for Alcaraz")]
ny = by + 36
for n, label in nums:
    d.text((bx + 12, ny), n, font=font(SANS_B, 19), fill=RED)
    d.text((bx + 88, ny + 1), label, font=font(SANS, 18), fill=INK)
    ny += 20
y = check_y(max(end_a, by + bh) + 8, "row4")
y = hline(y, width=2)

# ---------- Also today strip (two columns) ----------
y += 6
d.text((x0, y), "ALSO TODAY", font=font(SANS_B, 19), fill=NAVY)
y += 26
f_item = font(SANS, 17)
col2_x = x0 + col_w + 28
left_items = [
    "Alcaraz wins a maiden ATP Finals title.",
    "Chess Championship begins in Geneva.",
    "Verstappen wins the Las Vegas GP.",
]
right_items = [
    "NHS launches huge AI breast-cancer trial.",
    "Tyson Fury reveals schizophrenia diagnosis.",
    "BepiColombo enters orbit around Mercury.",
]
iy = y
for it in left_items:
    d.text((x0 + 12, iy), "\u2022", font=f_item, fill=NAVY)
    iy = para(x0 + 30, iy, it, f_item, col_w - 30, leading=1.22)
    iy += 3
jy = y
for it in right_items:
    d.text((col2_x + 12, jy), "\u2022", font=f_item, fill=NAVY)
    jy = para(col2_x + 30, jy, it, f_item, col_w - 30, leading=1.22)
    jy += 3
y = check_y(max(iy, jy), "also today")
y = hline(y + 4, width=2)

# ---------- footer ----------
y += 6
f_foot = font(SANS, 15)
foot = ("Sources: BBC, Reuters, The Times of India, Jagran Josh, Disclosure News  •  "
        "All graphics drawn — no photographs")
d.text((x0, y), foot, font=f_foot, fill=GREY)
y += 18
f_foot2 = font(SANS_B, 14)
f2 = "THE WORLD — 24 NOVEMBER 2026  •  Drawn with Pillow, no network, no randomness"
d.text(((W - text_w(f2, f_foot2)) / 2, y), f2, font=f_foot2, fill=NAVY)
y += 20
assert y <= 1024, f"final y {y} exceeds 1024"
print(f"final y = {y}")

img.save("entry.png", optimize=True)
print("saved entry.png")
