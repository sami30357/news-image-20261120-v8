#!/usr/bin/env python3
"""V8 renderer: a dense cream broadsheet for Friday 20 November 2026.
Draws entry.png (1024x1024) with Pillow only, no network, no reads of
other versions' code. Every drawn panel carries a fact: 2-sentence hero
bodies, verification chips on all 13 drawn stories, two-column briefs,
a big map with spread pins, and a region bar computed from the story
list so it can never miscount (V6's bar summed to 31, not 35)."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (179, 39, 30)
NAVY = (22, 35, 63)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
AMBER = (180, 83, 9)
GREY = (107, 114, 128)
LINE = (216, 208, 189)
CREAM2 = (238, 231, 214)
SKY = (183, 205, 224)
SEA = (146, 178, 205)

FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def F(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: F(FD + "DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F(FD + "DejaVuSerif.ttf", s)
SERIF_I = lambda s: F(FD + "DejaVuSerif-Italic.ttf", s)
SANS = lambda s: F(FD + "DejaVuSans.ttf", s)
SANS_B = lambda s: F(FD + "DejaVuSans-Bold.ttf", s)
SANS_O = lambda s: F(FD + "DejaVuSans-Oblique.ttf", s)

WARN = []


def wrap(text, font, width, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        WARN.append("OVERFLOW %r -> %d lines (max %d)" % (text[:40], len(lines), max_lines))
        lines = lines[:max_lines]
    return lines


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def rrect(d, box, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)


def chip(d, x, y, label, kind):
    """Verification chip: CONFIRMED green, OFFICIAL blue, REPORTED amber."""
    col = {"CONFIRMED": (34, 139, 34), "OFFICIAL": (31, 78, 121),
           "REPORTED": (146, 90, 10)}.get(kind, GREY)
    f = SANS_B(10)
    w = int(f.getlength(label)) + 10
    rrect(d, [x, y, x + w, y + 15], 3, fill=col)
    text(d, (x + 5, y + 2), label, f, fill=(255, 255, 255))
    return w


def label_chip(d, x, y, label, bg=RED):
    f = SANS_B(11)
    w = int(f.getlength(label)) + 12
    rrect(d, [x, y, x + w, y + 18], 2, fill=bg)
    text(d, (x + 6, y + 3), label, f, fill=(255, 255, 255))
    return w


def dashed_arc(d, cx, cy, rx, ry, a0, a1, fill, step=7, dot=3):
    a = a0
    while a <= a1:
        r = math.radians(a)
        x, y = cx + rx * math.cos(r), cy + ry * math.sin(r)
        d.ellipse([x - dot, y - dot, x + dot, y + dot], fill=fill)
        a += step


def skyline(d, x0, y0, x1, y1, lit=True):
    """Night skyline: dark buildings with lit windows."""
    import random
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    rnd = random.Random(20)
    x = x0
    while x < x1:
        bw = rnd.randint(14, 30)
        bh = rnd.randint(18, int((y1 - y0) * 0.75))
        d.rectangle([x, y1 - bh, x + bw, y1], fill=(12, 18, 34))
        if lit:
            for wy in range(y1 - bh + 4, y1 - 4, 9):
                for wx in range(x + 3, x + bw - 3, 8):
                    if rnd.random() < 0.45:
                        d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        x += bw + 2


def scene_kyiv(d, x, y, w, h):
    w, h = int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=(13, 22, 48))
    import random
    rnd = random.Random(7)
    for _ in range(46):
        sx, sy = x + rnd.randint(2, w - 2), y + rnd.randint(2, int(h * 0.45))
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(235, 230, 205))
    skyline(d, x + 4, y + h - 58, x + w - 4, y + h - 26)
    # river
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(24, 52, 92))
    # three arched bridges
    for bx in (x + 18, x + w // 2 - 52, x + w - 122):
        d.arc([bx, y + h - 52, bx + 104, y + h - 8], 180, 360,
              fill=(240, 236, 220), width=3)
        d.line([bx, y + h - 30, bx + 104, y + h - 30], fill=(240, 236, 220), width=2)
    # missile trails (dotted arcs, kept inside the panel) + fires
    dashed_arc(d, x + 100, y + h - 30, 58, 40, 200, 335, (255, 214, 90))
    dashed_arc(d, x + w - 100, y + h - 30, 55, 38, 205, 330, (255, 214, 90))
    for fx, fy in ((x + 62, y + h - 34), (x + w - 66, y + h - 34)):
        d.polygon([(fx, fy - 12), (fx - 7, fy + 4), (fx + 7, fy + 4)], fill=(255, 140, 40))
        d.ellipse([fx - 5, fy - 2, fx + 5, fy + 8], fill=(255, 200, 60))
    rrect(d, [x + 8, y + h - 24, x + 96, y + h - 6], 2, fill=(255, 255, 255))
    text(d, (x + 13, y + h - 21), "3 bridges hit", SANS_B(11), fill=INK)


def scene_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(203, 222, 235))
    # landmass (Odisha coast) left, sea right
    d.polygon([(x, y), (x + int(w * 0.42), y), (x + int(w * 0.34), y + h),
               (x, y + h)], fill=(214, 196, 158))
    d.polygon([(x + int(w * 0.42), y), (x + int(w * 0.46), y + int(h * 0.4)),
               (x + int(w * 0.34), y + h), (x + int(w * 0.30), y + h)],
              fill=(190, 172, 132))
    cx, cy = x + int(w * 0.62), y + int(h * 0.52)
    for r in (52, 40, 28, 16):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    # dashed landfall track
    dashed_arc(d, cx - 90, cy + 70, 95, 60, 300, 355, RED, step=6, dot=2)
    text(d, (x + 8, y + 6), "ODISHA", SANS_B(11), fill=(90, 60, 30))
    text(d, (x + 8, y + 20), "GOPALPUR", SANS_B(10), fill=(90, 60, 30))
    text(d, (x + 8, y + 34), "BAY OF BENGAL", SANS_B(10), fill=(60, 90, 120))
    rrect(d, [x + w - 128, y + h - 26, x + w - 8, y + h - 8], 2, fill=RED)
    text(d, (x + w - 122, y + h - 22), "Landfall · 7:30 am", SANS_B(11), fill=(255, 255, 255))


def scene_market(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    pts = [(x + 16, y + 34), (x + 60, y + 52), (x + 100, y + 44), (x + 140, y + 74),
           (x + 175, y + 66), (x + 205, y + 100)]
    d.line(pts, fill=(255, 80, 60), width=3, joint="curve")
    d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5],
              fill=(255, 80, 60))
    vals = [("TAIEX", "-6.2%"), ("NIKKEI", "-5.1%"), ("KOSPI", "-5.2%"),
            ("HANG SENG", "-1.9%")]
    f1, f2 = SANS_B(12), SANS_B(12)
    yy = y + 30
    for name, v in vals:
        text(d, (x + w - 96, yy), name, f1, fill=(220, 225, 235))
        text(d, (x + w - 8, yy), v, f2, fill=(255, 110, 90), anchor="ra")
        yy += 20
    rrect(d, [x + 8, y + h - 26, x + 132, y + h - 8], 2, fill=(255, 255, 255))
    text(d, (x + 13, y + h - 22), "Asia, Friday's close", SANS_B(11), fill=INK)

# ---- mid scenes (each ~185x62, one fact drawn inside) ----

def mid_uk_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 78, 121))
    # Union Jack (simplified)
    d.rectangle([x + 8, y + 10, x + 78, y + h - 10], fill=(18, 40, 90))
    d.rectangle([x + 8, y + h // 2 - 4, x + 78, y + h // 2 + 4], fill=(255, 255, 255))
    d.rectangle([x + 40, y + 10, x + 48, y + h - 10], fill=(255, 255, 255))
    d.rectangle([x + 8, y + h // 2 - 2, x + 78, y + h // 2 + 2], fill=(200, 30, 40))
    d.rectangle([x + 42, y + 10, x + 46, y + h - 10], fill=(200, 30, 40))
    # EU stars
    d.rectangle([x + 92, y + 10, x + w - 8, y + h - 10], fill=(0, 51, 153))
    import math as _m
    for k in range(12):
        a = _m.radians(k * 30 - 90)
        sx = x + 92 + (w - 100) // 2 + int(20 * _m.cos(a))
        sy = y + h // 2 + int(15 * _m.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 215, 0))
    rrect(d, [x + 8, y + h - 20, x + 62, y + h - 5], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + h - 17), "Agreed", SANS_B(10), fill=INK)


def mid_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 222, 178))
    d.ellipse([x + 110, y + h - 26, x + 170, y + h - 8], fill=(90, 70, 50))
    d.ellipse([x + 122, y + h - 22, x + 158, y + h - 12], fill=(60, 45, 30))
    # Kh-101 cruise missile, diagonal
    d.polygon([(x + 30, y + 46), (x + 120, y + 14), (x + 132, y + 20),
               (x + 42, y + 52)], fill=(240, 240, 240))
    d.polygon([(x + 120, y + 14), (x + 138, y + 8), (x + 132, y + 20)],
              fill=(200, 30, 40))
    d.polygon([(x + 30, y + 46), (x + 22, y + 40), (x + 26, y + 54)], fill=(180, 180, 180))
    rrect(d, [x + 8, y + 6, x + 96, y + 22], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + 9), "Kh-101 down", SANS_B(10), fill=INK)


def mid_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 214))
    d.ellipse([x + 12, y + 8, x + 62, y + h - 8], fill=(70, 140, 200))
    d.polygon([(x + 22, y + 22), (x + 38, y + 16), (x + 52, y + 26), (x + 44, y + 40),
               (x + 28, y + 38)], fill=(80, 180, 90))
    d.polygon([(x + 30, y + 44), (x + 46, y + 42), (x + 50, y + 52), (x + 34, y + 54)],
              fill=(80, 180, 90))
    # thermometer, empty (0 mentions)
    d.rectangle([x + 88, y + 10, x + 100, y + h - 18], fill=(255, 255, 255),
                outline=(150, 150, 150))
    d.ellipse([x + 82, y + h - 24, x + 106, y + h - 2], fill=(200, 30, 40))
    d.rectangle([x + 90, y + h - 16, x + 98, y + h - 8], fill=(200, 30, 40))
    # clock: last day
    d.ellipse([x + 122, y + 10, x + 162, y + 50], fill=(255, 255, 255),
              outline=(60, 60, 60))
    d.line([x + 142, y + 30, x + 142, y + 16], fill=INK, width=2)
    d.line([x + 142, y + 30, x + 152, y + 34], fill=INK, width=2)
    rrect(d, [x + 118, y + h - 22, x + w - 8, y + h - 6], 2, fill=RED)
    text(d, (x + 123, y + h - 19), "Last day", SANS_B(10), fill=(255, 255, 255))


def mid_cancer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 248))
    # capsule pill
    d.rounded_rectangle([x + 14, y + 14, x + 86, y + 38], radius=12, fill=(255, 255, 255),
                        outline=(120, 120, 120))
    d.rounded_rectangle([x + 14, y + 14, x + 50, y + 38], radius=12, fill=(30, 120, 190))
    d.line([x + 50, y + 14, x + 50, y + 38], fill=(120, 120, 120), width=1)
    text(d, (x + 100, y + 10), "60.7%", SANS_B(24), fill=(20, 90, 160))
    text(d, (x + 100, y + 38), "respond", SANS_B(12), fill=GREY)
    rrect(d, [x + 8, y + h - 20, x + 92, y + h - 5], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + h - 17), "Trial data", SANS_B(10), fill=INK)


def mid_mercury(d, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 26))
    import random
    rnd = random.Random(3)
    for _ in range(24):
        sx, sy = x + rnd.randint(2, w - 2), y + rnd.randint(2, h - 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # Mercury, cratered
    d.ellipse([x + w - 66, y + 6, x + w - 8, y + h - 6], fill=(150, 148, 140))
    for cx, cy, cr in ((x + w - 48, y + 18, 6), (x + w - 30, y + 34, 8),
                       (x + w - 52, y + 42, 4)):
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(120, 118, 110))
    # dotted approach trajectory + probe
    dashed_arc(d, x + 20, y + h - 8, 70, 34, 290, 350, (255, 214, 90), step=6, dot=2)
    d.ellipse([x + 62, y + h - 26, x + 70, y + h - 18], fill=(255, 214, 90))
    rrect(d, [x + 8, y + 6, x + 96, y + 22], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + 9), "8 years in flight", SANS_B(10), fill=INK)
    text(d, (x + w - 8, y + h - 20), "Capture Sat", SANS_B(10), fill=(255, 255, 255),
         anchor="ra")


def mid_senegal(d, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=(146, 178, 205))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(40, 90, 140))
    # capsized boat, tilted hull
    d.polygon([(x + 40, y + 26), (x + 130, y + 40), (x + 120, y + 52),
               (x + 48, y + 40)], fill=(120, 70, 30))
    d.polygon([(x + 78, y + 28), (x + 92, y + 52), (x + 84, y + 54)], fill=(90, 50, 20))
    for px, py in ((x + 20, y + 34), (x + 150, y + 30), (x + 140, y + 46), (x + 158, y + 48)):
        d.ellipse([px, py, px + 7, py + 7], fill=(30, 30, 30))
    for wx in range(x + 6, x + w - 6, 22):
        d.arc([wx, y + h - 18, wx + 18, y + h - 6], 180, 360, fill=(255, 255, 255), width=2)
    rrect(d, [x + 8, y + 6, x + 142, y + 22], 2, fill=RED)
    text(d, (x + 12, y + 9), "4 dead · dozens missing", SANS_B(9),
         fill=(255, 255, 255))


def mid_argentina(d, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 232))
    # risk gauge, fitted inside the 56px panel
    d.arc([x + 14, y + 4, x + 94, y + 50], 180, 360, fill=(200, 60, 40), width=6)
    d.arc([x + 14, y + 4, x + 94, y + 50], 180, 270, fill=(60, 160, 80), width=6)
    d.line([x + 54, y + 27, x + 78, y + 10], fill=RED, width=3)
    d.ellipse([x + 50, y + 23, x + 58, y + 31], fill=INK)
    text(d, (x + 104, y + 8), "1,070", SANS_B(18), fill=RED)
    text(d, (x + 104, y + 30), "+15%", SANS_B(12), fill=GREY)
    rrect(d, [x + 8, y + h - 20, x + 118, y + h - 5], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + h - 17), "First over 1,000 in 13 mo", SANS_B(10), fill=INK)


def mid_pakistan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 236, 222))
    # Pakistan flag
    d.rectangle([x + 10, y + 12, x + 82, y + h - 12], fill=(20, 90, 50))
    d.rectangle([x + 10, y + 12, x + 26, y + h - 12], fill=(255, 255, 255))
    d.ellipse([x + 38, y + 20, x + 58, y + 40], fill=(255, 255, 255))
    d.ellipse([x + 42, y + 20, x + 60, y + 40], fill=(20, 90, 50))
    # India flag
    d.rectangle([x + 96, y + 12, x + w - 10, y + h - 12], fill=(255, 255, 255),
                outline=(150, 150, 150))
    d.rectangle([x + 96, y + 12, x + w - 10, y + 24], fill=(255, 153, 51))
    d.rectangle([x + 96, y + h - 24, x + w - 10, y + h - 12], fill=(19, 136, 8))
    d.ellipse([x + 128, y + 24, x + 148, y + 44], fill=(255, 255, 255),
              outline=(0, 56, 147))
    rrect(d, [x + 8, y + h - 20, x + 96, y + h - 5], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + h - 17), "SCO forum", SANS_B(10), fill=INK)


def mid_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    # wet track + spray
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(60, 64, 78))
    d.line([x, y + h - 22, x + w, y + h - 22], fill=(255, 255, 255), width=2)
    # race car
    d.polygon([(x + 30, y + 34), (x + 70, y + 30), (x + 110, y + 34), (x + 150, y + 40),
               (x + 150, y + 46), (x + 30, y + 46)], fill=(180, 30, 40))
    d.polygon([(x + 70, y + 30), (x + 84, y + 18), (x + 104, y + 18), (x + 112, y + 30)],
              fill=(120, 20, 30))
    d.rectangle([x + 142, y + 20, x + 150, y + 34], fill=(200, 30, 40))
    for wx in (x + 48, x + 124):
        d.ellipse([wx, y + 42, wx + 18, y + 60], fill=(15, 15, 15))
        d.ellipse([wx + 5, y + 47, wx + 13, y + 55], fill=(120, 120, 120))
    # chequered flag on a white tab for contrast
    d.rectangle([x + w - 46, y + 6, x + w - 6, y + 26], fill=(255, 255, 255))
    for i in range(4):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + w - 44 + i * 9, y + 8 + j * 9, x + w - 35 + i * 9,
                             y + 17 + j * 9], fill=(20, 20, 20))
    rrect(d, [x + 8, y + 6, x + 92, y + 22], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + 9), "P1 Russell", SANS_B(10), fill=INK)


def mid_malawi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    # petrol pump
    d.rectangle([x + 14, y + 10, x + 52, y + h - 10], fill=(200, 30, 40))
    d.rectangle([x + 22, y + 20, x + 44, y + 34], fill=(255, 255, 255))
    text(d, (x + 24, y + 22), "20L", SANS_B(9), fill=INK)
    d.line([x + 52, y + 18, x + 66, y + 30], fill=INK, width=2)
    # queue of people
    for i, px in enumerate((78, 102, 126, 150)):
        d.ellipse([x + px, y + 16, x + px + 10, y + 26], fill=(40, 40, 40))
        d.rectangle([x + px - 1, y + 27, x + px + 11, y + h - 22],
                    fill=(60 + i * 20, 60, 90))
    rrect(d, [x + 8, y + h - 20, x + 110, y + h - 5], 2, fill=(255, 255, 255))
    text(d, (x + 12, y + h - 17), "20 litres a day", SANS_B(10), fill=INK)


MID_SCENES = {"uk_eu": mid_uk_eu, "poland": mid_poland, "cop31": mid_cop31,
              "cancer": mid_cancer, "mercury": mid_mercury, "senegal": mid_senegal,
              "argentina": mid_argentina, "pakistan": mid_pakistan,
              "f1": mid_f1, "malawi": mid_malawi}

# ---- story data: 35 verified Friday stories ----
# region codes: EU AS ME AF AM OC GL. The region bar is COMPUTED from
# this list (single source of truth) so it can never miscount.
HEROES = [
    dict(n=1, region="EU", place="KYIV, UKRAINE", field="WAR",
         head="Russian missiles hit three Kyiv bridges",
         body="About 110 missiles and 400 drones killed at least eight in the capital and cut power and water. Three crossings hit. (Reuters \u00b7 Kyiv Post)",
         chip="CONFIRMED", scene="kyiv"),
    dict(n=2, region="AS", place="ODISHA, INDIA", field="CYCLONE",
         head="Cyclone Akvan comes ashore in eastern India",
         body="The storm crossed near Gopalpur from about 8 am after 300,000+ were moved to shelters. No deaths; 209 mm of rain at Patrapur. (IMD \u00b7 NDTV)",
         chip="CONFIRMED", scene="akvan"),
    dict(n=3, region="GL", place="TAIPEI \u00b7 SEOUL \u00b7 TOKYO", field="MARKETS",
         head="AI sell-off sinks Asia's stock markets",
         body="Taiex fell 6.2% in its worst week since 1991 as chipmakers led the slide; Seoul \u22125.2%, Tokyo \u22125.1%. (Al Jazeera \u00b7 Reuters)",
         chip="CONFIRMED", scene="market"),
]

MIDS = [
    dict(n=4, region="EU", place="BRUSSELS", field="DIPLOMACY",
         head="UK and EU seal a \u201creset\u201d deal",
         body="Food trade, youth visas, carbon link. (Reuters)", chip="REPORTED",
         scene="uk_eu"),
    dict(n=5, region="EU", place="EASTERN POLAND", field="WAR",
         head="Russian missile lands in Poland",
         body="Kh-101 down; NATO jets scrambled. (Ukr. Pravda)", chip="REPORTED",
         scene="poland"),
    dict(n=6, region="GL", place="ANTALYA", field="CLIMATE",
         head="COP31 reaches its last day with no deal",
         body="Draft text leaves out fossil fuels. (AFP)", chip="REPORTED",
         scene="cop31"),
    dict(n=7, region="GL", place="HEALTH", field="TRIAL",
         head="Pancreatic cancer pill: 60.7% respond",
         body="Tumours shrank with chemo in 61 patients. (Reuters)", chip="REPORTED",
         scene="cancer"),
    dict(n=8, region="GL", place="SPACE", field="8 YEARS",
         head="BepiColombo reaches Mercury after 8 years",
         body="ESA/JAXA probe ends 6bn-mile trip. (ESA \u00b7 BBC)",
         chip="CONFIRMED", scene="mercury"),
    dict(n=9, region="AF", place="DAKAR", field="MIGRATION",
         head="Migrant boat capsizes off Senegal",
         body="Dozens missing; 4 dead. (Al Jazeera)",
         chip="REPORTED", scene="senegal"),
    dict(n=10, region="AM", place="BUENOS AIRES", field="MARKETS",
         head="Argentina's country risk jumps to 1,070",
         body="Up 15%; first close over 1,000 in 13 months. (JPM)", chip="REPORTED",
         scene="argentina"),
    dict(n=11, region="AS", place="NEW DELHI", field="DIPLOMACY",
         head="Pakistan PM visits New Delhi",
         body="First visit since the May 2025 clash. (PTI \u00b7 Dawn)", chip="CONFIRMED",
         scene="pakistan"),
    dict(n=12, region="AM", place="LAS VEGAS", field="FORMULA 1",
         head="Russell fastest in wet Las Vegas practice",
         body="Led practice 2 on 1:47.272. (F1)",
         chip="REPORTED", scene="f1"),
    dict(n=13, region="AF", place="BLANTYRE", field="FUEL",
         head="Malawi fuel crisis: night queues grow",
         body="Petrol $3.24 a litre; queues grow. (Al Jazeera)",
         chip="REPORTED", scene="malawi"),
]

BRIEFS = [
    (14, "Kenya", "Oil rig starts; crude due Dec 1", "Business Daily", "AF"),
    (15, "China", "Loan rates held an 18th month", "Xinhua", "AS"),
    (16, "Iraq", "Army enters a militia stronghold", "Reuters", "ME"),
    (17, "Bukele", "Files to run for a third term", "AP", "AM"),
    (18, "Italy", "General strike over the budget", "Reuters", "EU"),
    (19, "Japan", "CPI picks up to 2.3%", "Japan Times", "AS"),
    (20, "Phillips", "Hits 118 against India", "ICC", "OC"),
    (21, "Rohingya", "Weep and pray after ICJ ruling", "Al Jazeera", "AS"),
    (22, "Seoul", "Ruling party moves to impeach top judge", "Yonhap", "AS"),
    (23, "Brent", "$92.60 as Hormuz fears rise", "Reuters", "ME"),
    (24, "Houthi", "Riyadh missile intercepted", "Reuters", "ME"),
    (25, "Iran", "Two tankers hit naval mines (CLAIM)", "NDTV", "ME"),
    (26, "Erasca", "Drug: 44% of patients respond", "Reuters", "GL"),
    (27, "Antonelli", "Confirmed youngest F1 champion", "FIA", "GL"),
    (28, "Lviv", "Strike on a railway station kills two", "BBC", "EU"),
    (29, "Youth", "Protests spread to five countries", "Reuters", "GL"),
    (30, "US", "900,000 advanced chips approved for China", "WSJ", "AM"),
    (31, "Akvan", "423 teams, 9,341 shelters ready", "NDTV", "AS"),
    (32, "SoftBank", "Shares fall 14.6% in a day", "Al Jazeera", "AS"),
    (33, "COP31", "\u201c35 by 35\u201d clean-power goal kept", "Carbon Brief", "GL"),
    (34, "EU", "Calls the COP31 draft \u201cnot acceptable\u201d", "AFP", "EU"),
    (35, "Nvidia", "Subpoenaed over chips sent to China", "Reuters", "AM"),
]

STATS = [
    ("3", "bridges hit in Kyiv"),
    ("300,000+", "evacuated before Akvan"),
    ("\u22126.2%", "Taiex, Friday's close"),
    ("0", "fossil-fuel mentions in COP31 draft"),
    ("900,000", "US chips approved for China"),
    ("118", "runs by Glenn Phillips"),
]

REGIONS = [("EU", "Europe", (31, 78, 121)), ("AS", "Asia", (139, 30, 35)),
           ("ME", "Middle East", (122, 90, 30)), ("AF", "Africa", (34, 120, 70)),
           ("AM", "Americas", (110, 60, 130)), ("OC", "Oceania", (20, 130, 140)),
           ("GL", "Global", (90, 90, 90))]

# pin positions (lon, lat) for the drawn stories that happened somewhere
PINS = {1: (30.5, 50.4), 2: (84.9, 19.3), 3: (121.5, 25.0), 4: (4.35, 50.85),
        5: (22.0, 51.5), 6: (30.7, 36.9), 9: (-17.4, 14.7),
        10: (-58.4, -34.6), 11: (77.2, 28.6), 12: (-115.1, 36.2),
        13: (35.0, -15.8)}


def region_counts():
    counts = {code: 0 for code, _, _ in REGIONS}
    for s in HEROES + MIDS:
        counts[s["region"]] += 1
    for _, _, _, _, r in BRIEFS:
        counts[r] += 1
    assert sum(counts.values()) == 35, counts
    return counts


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    X0, X1 = 28, 996
    # ---- top line ----
    text(d, (X0, 12), "THE WORLD IN ONE DAY", SANS_B(13), fill=RED)
    text(d, (X1, 12), "35 STORIES \u00b7 7 REGIONS \u00b7 15 FIELDS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026",
         SANS_B(11), fill=INK, anchor="ra")
    d.line([X0, 34, X1, 34], fill=INK, width=2)
    # ---- masthead ----
    text(d, (W // 2, 40), "Friday 20 November 2026", SERIF_B(66), fill=INK, anchor="ma")
    text(d, (W // 2, 140),
         "Russian missiles hit Kyiv's bridges \u00b7 Cyclone Akvan strikes India \u00b7 An AI sell-off sinks Asia's markets \u00b7 UK and EU seal a deal",
         SERIF_I(19), fill=(60, 60, 60), anchor="ma")
    d.line([X0, 170, X1, 170], fill=INK, width=2)
    # ---- stat strip ----
    y = 178
    cw = (X1 - X0) / 6
    for i, (num, lab) in enumerate(STATS):
        cx = X0 + cw * i
        if i:
            d.line([cx, y + 2, cx, y + 50], fill=LINE, width=1)
        text(d, (cx + 10, y), num, SERIF_B(30), fill=INK)
        for j, ln in enumerate(wrap(lab, SANS(11), cw - 16, max_lines=2)):
            text(d, (cx + 10, y + 34 + j * 12), ln, SANS(11), fill=(70, 70, 70))
    # ---- region bar (computed) ----
    counts = region_counts()
    y = 238
    x = X0
    total_w = X1 - X0
    for code, name, col in REGIONS:
        w = total_w * counts[code] / 35
        d.rectangle([x, y, x + w - 1, y + 20], fill=col)
        lab = "%s %d" % (name, counts[code])
        f = SANS_B(11)
        if f.getlength(lab) <= w - 8:
            text(d, (x + w / 2, y + 4), lab, f, fill=(255, 255, 255), anchor="ma")
        else:
            # narrow segment (Oceania, 1 story): show the count only
            text(d, (x + w / 2, y + 4), str(counts[code]), f,
                 fill=(255, 255, 255), anchor="ma")
        x += w
    # ---- heroes ----
    y = 266
    hw = (X1 - X0 - 20) / 3
    hh = 120
    for i, s in enumerate(HEROES):
        hx = X0 + i * (hw + 10)
        if s["scene"] == "kyiv":
            scene_kyiv(d, hx, y, hw, hh)
        elif s["scene"] == "akvan":
            scene_akvan(d, hx, y, hw, hh)
        else:
            scene_market(d, hx, y, hw, hh)
        # verification chip inside the image, top right (leaders' caption spot)
        chip(d, hx + hw - 100, y + 6, s["chip"], s["chip"])
        ty = y + hh + 6
        text(d, (hx, ty), "%d \u00b7 %s \u00b7 %s" % (s["n"], s["place"], s["field"]),
             SANS_B(12), fill=RED)
        ty += 18
        for ln in wrap(s["head"], SERIF_B(21), hw, max_lines=2):
            text(d, (hx, ty), ln, SERIF_B(21), fill=INK)
            ty += 23
        for ln in wrap(s["body"], SANS(12), hw, max_lines=3):
            text(d, (hx, ty), ln, SANS(12), fill=(50, 50, 50))
            ty += 14
    # ---- mids: 2 rows x 5, row height 150 ----
    y = 510
    mw = (X1 - X0 - 40) / 5
    mh = 56
    for row in range(2):
        for col in range(5):
            s = MIDS[row * 5 + col]
            mx = X0 + col * (mw + 10)
            my = y + row * 150
            MID_SCENES[s["scene"]](d, mx, my, mw, mh)
            ty = my + mh + 4
            text(d, (mx, ty), "%d \u00b7 %s \u00b7 %s" % (s["n"], s["place"], s["field"]),
                 SANS_B(10), fill=RED)
            ty += 14
            for ln in wrap(s["head"], SERIF_B(15), mw, max_lines=2):
                text(d, (mx, ty), ln, SERIF_B(15), fill=INK)
                ty += 16
            for ln in wrap(s["body"], SANS(11), mw, max_lines=2):
                text(d, (mx, ty), ln, SANS(11), fill=(60, 60, 60))
                ty += 12
            chip(d, mx, ty + 2, s["chip"], s["chip"])
    return img, d


def draw_map(d, x, y, w, h):
    """Simplified world map with numbered pins for the drawn stories
    that happened somewhere (11 of the 13; 7 is a trial, 8 is space)."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 205))
    # rough continent outlines (lon -170..190 -> x, lat 75..-55 -> y)
    def X(lon):
        return x + (lon + 170) / 360 * w
    def Y(lat):
        return y + (75 - lat) / 130 * h
    def poly(pts, fill):
        d.polygon([(X(lo), Y(la)) for lo, la in pts], fill=fill)
    LAND = (206, 188, 152)
    poly([(-168, 66), (-140, 70), (-120, 72), (-95, 68), (-80, 60), (-60, 48),
          (-55, 42), (-70, 32), (-80, 26), (-97, 16), (-105, 20), (-120, 34),
          (-125, 48), (-150, 60), (-165, 60)], LAND)  # N America
    poly([(-80, 10), (-60, 5), (-50, -5), (-35, -8), (-40, -25), (-55, -35),
          (-65, -45), (-70, -30), (-75, -18), (-80, -5)], LAND)  # S America
    poly([(-18, 35), (-10, 37), (0, 36), (10, 37), (30, 36), (35, 30),
          (32, 12), (40, 5), (35, -18), (25, -30), (18, -35), (12, -18),
          (8, 4), (-8, 5), (-17, 15), (-17, 27)], LAND)  # Africa
    poly([(-10, 36), (-9, 43), (-2, 48), (0, 51), (8, 55), (18, 54),
          (28, 46), (30, 42), (23, 36), (12, 38), (3, 38)], LAND)  # Europe
    poly([(30, 42), (40, 44), (50, 46), (60, 52), (75, 55), (90, 60),
          (110, 62), (130, 60), (150, 60), (160, 55), (142, 45), (135, 35),
          (122, 30), (110, 20), (105, 8), (100, 6), (90, 15), (80, 8),
          (72, 20), (60, 25), (50, 30), (40, 36)], LAND)  # Asia
    poly([(114, -22), (124, -15), (134, -12), (142, -11), (150, -20),
          (153, -28), (146, -38), (135, -35), (124, -33), (114, -32)], LAND)  # Australia
    for n, (lon, lat) in PINS.items():
        px, py = X(lon), Y(lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        text(d, (px, py - 6), str(n), SANS_B(9), fill=(255, 255, 255), anchor="ma")


def draw_bottom(img, d):
    X0, X1 = 28, 996
    y = 818
    text(d, (X0, y), "WHERE IT HAPPENED", SANS_B(12), fill=RED)
    text(d, (X0 + 320, y), "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES",
         SANS_B(12), fill=RED)
    y += 18
    draw_map(d, X0, y, 300, 118)
    # briefs in two balanced columns
    bx = X0 + 320
    colw = (X1 - bx - 10) // 2
    fnum = SANS_B(11)
    fbody = SANS(10)
    for i, (n, who, what, src, _r) in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        bx2 = bx + col * (colw + 10)
        by = y + row * 11
        s = "%d %s \u2014 %s (%s)" % (n, who, what, src)
        if fbody.getlength(s) > colw - 4:
            WARN.append("BRIEF TOO LONG: %s" % s)
        text(d, (bx2, by), s, fbody, fill=(40, 40, 40))
    # ---- DATE CHECK ----
    y = 958
    d.rectangle([X0, y, X1, y + 44], outline=RED, width=2)
    text(d, (X0 + 8, y + 4), "DATE CHECK", SANS_B(11), fill=RED)
    dc = ("LEFT OUT \u2014 first reported Thursday 19 November: Anthropic's $83 IPO pricing & Nasdaq debut \u00b7 "
          "Wall Street \u22122% \u00b7 Dow under 50,000 \u00b7 the ICJ ruling itself \u00b7 Riyadh tower attack \u00b7 GTA VI midnight launch.  "
          "NOT YET \u2014 BepiColombo Mercury orbit capture (Saturday) \u00b7 COP31's final text \u00b7 the ATP Finals final (Sunday) \u00b7 Estonia's border closure (1 December).")
    for j, ln in enumerate(wrap(dc, SANS(11), X1 - X0 - 110, max_lines=3)):
        text(d, (X0 + 100, y + 3 + j * 13), ln, SANS(11), fill=INK)
    # ---- footer ----
    text(d, (X0, 1008),
         "Every story happened, or was first reported, on Friday 20 November 2026.",
         SANS(10), fill=GREY)
    text(d, (X1, 1008),
         "CONFIRMED 2+ outlets \u00b7 OFFICIAL on the record \u00b7 REPORTED one outlet \u00b7 Original drawings",
         SANS(10), fill=GREY, anchor="ra")


def main():
    img, d = draw()
    draw_bottom(img, d)
    # The grader runs with a read-only repo: write the poster straight
    # into its output directory when one is given, else next to render.py.
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    path = os.path.join(out, "entry.png")
    img.save(path, format="PNG")
    print("saved", path, img.size)
    print("region counts:", region_counts())
    if WARN:
        print("WARNINGS (%d):" % len(WARN))
        for w in WARN:
            print(" -", w)
    else:
        print("no fit warnings")


if __name__ == "__main__":
    main()
