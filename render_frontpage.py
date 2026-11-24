#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Fresh rebuild for the news-image-20261124 bounty, written in this session.
Pillow only, no network, no randomness: the same script always writes
identical bytes. New broadsheet layout (masthead, lead with a drawn market
chart, chessboard panel, three-column middle, footer strip).

Stories — events of, or first reported on, Tuesday 24 November 2026,
verified by public web search on 24 Nov 2026 (sources in brackets):
- LEAD: Jensen Huang's return to Nvidia sparks an AI stock rally across
  Asia and Europe; the US is investigating Iran over cyberattacks on
  energy tankers. [Morningstar / Dow Jones EMEA Morning Briefing, 24 Nov]
- Chess: the World Chess Championship begins in Geneva — defending
  champion D. Gukesh vs challenger Javokhir Sindarov, 14 games, $2.5m.
  [Reporter Post; DD News, 24 Nov]
- Indonesia: rescue operations continue after a factory fire leaves
  workers dead and missing. [Careerindia news bulletin, 24 Nov]
- Climate: COP31 ends in deadlock with no deal; Pacific islands get no
  relief. [PINA, 24 Nov]
- Tech: Cisco and OpenAI launch an open-source project to safeguard
  agentic AI. [Morningstar / Dow Jones, 24 Nov]
- Also today: India-New Zealand Wellington Test ends in a draw; Modi and
  Nepal PM Balendra Shah discuss closer ties; BepiColombo is safe in
  orbit around Mercury after a thruster glitch; about 12,000 people
  evacuated from a Manchester arena show over a mystery substance.
  [Careerindia; Morningstar; Reuters; news summaries, 24 Nov]
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 244, 228)
INK = (24, 24, 24)
NAVY = (18, 38, 66)
GREEN = (16, 122, 62)
RED = (178, 34, 34)
GREY = (96, 96, 96)
RULE = (24, 24, 24)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 34
x0, x1 = M, W - M


def text_w(s, f):
    return d.textlength(s, font=f)


def wrap_px(s, f, width):
    out = []
    for para_text in s.split("\n"):
        cur = ""
        for w in para_text.split():
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


def para(x, y, s, f, width, leading=1.28, fill=INK):
    lh = int(f.size * leading)
    for ln in wrap_px(s, f, width):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rule(y, width=2):
    d.line([(x0, y), (x1, y)], fill=RULE, width=width)
    return y


d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

# ---- masthead ----
y = 24
f_mast = font(SERIF_B, 66)
d.text((x0, y), "THE WORLD", font=f_mast, fill=NAVY)
d.text((x1 - 150, y + 20), "ONE DAY", font=font(SANS_B, 24), fill=RED)
y = 108
rule(y)
y += 8
d.text((x0, y), "TUESDAY, 24 NOVEMBER 2026", font=font(SANS_B, 22), fill=INK)
d.text((x1 - 300, y), "THE DAY IN FULL", font=font(SANS, 22), fill=GREY)
y += 32
rule(y, width=3)

# ---- lead story (left) + chess panel (right) ----
y += 14
top = y
lead_x = x0
lead_w = 590
d.text((lead_x, y), "AI RALLY AFTER", font=font(SERIF_B, 38), fill=INK)
y += 44
d.text((lead_x, y), "HUANG'S RETURN", font=font(SERIF_B, 38), fill=INK)
y += 48
y = para(lead_x, y,
         "Nvidia reinstated Jensen Huang as chief executive on Monday, "
         "and AI stocks rallied across Asia and Europe on Tuesday as risk "
         "appetite returned. The board cited input from senior levels of "
         "the US government.",
         font(SERIF, 20), lead_w, leading=1.3)
y += 4
# Drawn market chart: rising green line with arrowhead — code-drawn.
cx, cy, cw, ch = lead_x, y, 580, 118
d.rectangle([cx, cy, cx + cw, cy + ch], outline=GREY, width=1)
pts = [(cx + 10 + i * 57, cy + ch - 26 - v) for i, v in
       enumerate([0, 8, 4, 22, 18, 38, 34, 58, 52, 78, 92])]
for a, b in zip(pts, pts[1:]):
    d.line([a, b], fill=GREEN, width=5)
d.polygon([(pts[-1][0], pts[-1][1] - 12), (pts[-1][0] + 14, pts[-1][1] + 2),
           (pts[-1][0] - 2, pts[-1][1] + 10)], fill=GREEN)
d.text((cx + 6, cy + 5), "AI STOCKS, TUESDAY", font=font(SANS_B, 14), fill=GREEN)
d.text((cx + cw - 110, cy + ch - 22), "UP SHARPLY", font=font(SANS_B, 14), fill=GREEN)
y = cy + ch + 10
y = para(lead_x, y,
         "Also: the US is investigating Iran as a possible culprit in "
         "dozens of cyberattacks on energy tankers.",
         font(SERIF, 19), lead_w, leading=1.28)
lead_bottom = y

# ---- chess panel (right column) ----
rx = lead_x + lead_w + 24
ry = top
d.rectangle([rx, ry, x1, lead_bottom], outline=NAVY, width=2)
d.text((rx + 12, ry + 10), "CHESS CROWN", font=font(SANS_B, 19), fill=NAVY)
d.text((rx + 12, ry + 34), "ON THE LINE", font=font(SANS_B, 19), fill=NAVY)
bx, by, sq = rx + 12, ry + 64, 26
for r in range(8):
    for c in range(8):
        fill = (240, 234, 220) if (r + c) % 2 == 0 else NAVY
        d.rectangle([bx + c * sq, by + r * sq,
                     bx + (c + 1) * sq, by + (r + 1) * sq], fill=fill)
d.text((bx + 2 * sq + 4, by + 2), "K", font=font(SERIF_B, 20), fill=INK)
d.text((bx + 6 * sq + 4, by + 5 * sq + 2), "K", font=font(SERIF_B, 20),
       fill=(240, 234, 220))
ty = by + 8 * sq + 8
ty = para(rx + 12, ty,
          "World Chess Championship begins in Geneva: Gukesh defends his "
          "crown against Sindarov — 14 games, $2.5m.",
          font(SERIF, 17), x1 - rx - 24, leading=1.28)

# ---- middle band: three columns ----
y = lead_bottom + 14
rule(y, width=3)
y += 12
col_w = (x1 - x0 - 48) // 3
cols = [
    ("INDONESIA", "Factory fire rescue",
     "Rescue operations continue after a major fire at an industrial "
     "facility, with casualties and workers still missing."),
    ("CLIMATE", "COP31 ends in deadlock",
     "Climate talks end with no deal and no relief for Pacific islands "
     "after the collapse of the Antalya pact."),
    ("TECH", "Safeguarding agentic AI",
     "Cisco and OpenAI launch an open-source project to safeguard "
     "agentic AI and prevent cyberattacks."),
]
ends = []
for i, (kicker, head, body) in enumerate(cols):
    cx = x0 + i * (col_w + 24)
    d.text((cx, y), kicker, font=font(SANS_B, 16), fill=RED)
    yy = para(cx, y + 22, head, font(SERIF_B, 23), col_w, leading=1.12)
    yy = para(cx, yy + 4, body, font(SERIF, 18), col_w, leading=1.26)
    ends.append(yy)
    if i < 2:
        d.line([(cx + col_w + 12, y), (cx + col_w + 12, yy)],
               fill=GREY, width=1)
mid_bottom = max(ends)

# ---- footer strip: also today ----
y = mid_bottom + 14
rule(y, width=3)
y += 10
d.text((x0, y), "ALSO TODAY", font=font(SANS_B, 19), fill=NAVY)
y += 28
y = para(x0, y,
         "India–New Zealand Wellington Test ends in a draw  •  Modi and "
         "Nepal PM Balendra Shah discuss closer ties  •  BepiColombo safe "
         "in orbit around Mercury after a thruster glitch  •  About 12,000 "
         "evacuated from a Manchester arena show.",
         font(SERIF, 18), x1 - x0, leading=1.28)
y += 8
rule(y, width=1)
y += 6
d.text((x0, y), "Sources: Morningstar / Dow Jones, Reuters, Reporter Post, DD News, "
                "Careerindia, PINA  •  All graphics drawn — no photographs",
       font=font(SANS, 13), fill=GREY)
y += 20
assert y <= 1010, f"layout overflow: final y={y}"
print(f"final y = {y}")

img.save("entry.png", format="PNG")
print("saved entry.png", img.size)
