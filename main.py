#!/usr/bin/env python3
"""news-image-20261120: one image summing up Friday 20 November 2026.

Draws a newspaper front page with PIL only: no network, no external
images, no timestamps. Two runs produce byte-identical output.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (252, 248, 236)
INK = (26, 26, 26)
MUTED = (90, 84, 70)
RED = (164, 18, 32)
NAVY = (31, 58, 95)
GOLD = (176, 106, 0)
GREEN = (46, 107, 79)
PURPLE = (107, 78, 138)
BROWN = (138, 90, 31)
SEA = (214, 228, 232)
LAND = (232, 214, 166)
RULE = (26, 26, 26)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_IT = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, fnt, width, max_lines):
    lines = wrap(text, fnt, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and fnt.getlength(lines[-1] + "…") > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


REGION_COLOR = {
    "EUROPE": NAVY,
    "ASIA": RED,
    "N. AMERICA": GREEN,
    "MIDDLE EAST": GOLD,
    "S. AMERICA": PURPLE,
    "AFRICA": BROWN,
}

# ---------------------------------------------------------------- stories
# Each panel: region, topic, chip, headline, detail, art kind, map (lon, lat)
PANELS = [
    ("EUROPE", "CONFLICT", "CONFIRMED — AP",
     "Russian missiles land in Poland",
     "Two missiles and a drone come down in SE Poland; NATO calls it a grave violation.",
     "missile", (19.0, 52.0)),
    ("EUROPE", "CONFLICT", "CONFIRMED — CNN",
     "Russia's biggest air raid of 2026",
     "110+ missiles, 400+ drones hit Ukraine overnight; at least 8 killed.",
     "barrage", (30.5, 50.4)),
    ("ASIA", "DIPLOMACY", "CONFIRMED — REUTERS",
     "The day after Shenzhen",
     "Trump, Xi, Putin met Thu; on Fri Trump faces the press on their nuclear-risk pledge.",
     "summit", (114.0, 22.5)),
    ("ASIA", "JUSTICE", "CONFIRMED — REUTERS",
     "Myanmar calls ICJ verdict 'unfair'",
     "Fri reaction: Myanmar committed genocide against the Rohingya, 9–6.",
     "court", (96.0, 21.0)),
    ("N. AMERICA", "MARKETS", "CONFIRMED — AP",
     "Wall Street sinks into correction",
     "S&P 500 falls 3.7% to 6,910; Nasdaq drops 5.3%, turning negative for the year.",
     "market", (-74.0, 40.7)),
    ("MIDDLE EAST", "CONFLICT", "CONFIRMED — REUTERS",
     "Houthi missiles hit Riyadh tower",
     "Strikes damage the PIF tower in the financial district; Saudi jets hit Hodeidah.",
     "tower", (46.7, 24.6)),
    ("EUROPE", "CLIMATE", "CONFIRMED — REUTERS",
     "COP31 runs into overtime",
     "Draft drops any fossil-fuel phase-out and a $120bn target; talks spill past Friday.",
     "climate", (30.7, 36.9)),
    ("S. AMERICA", "DISASTER", "CONFIRMED — USGS",
     "M6.7 quake shakes central Peru",
     "7:09 pm near Junin, felt in Lima; deep quake, no casualties or damage reported.",
     "quake", (-76.0, -10.0)),
    ("N. AMERICA", "HEALTH", "CONFIRMED — CDC",
     "US measles cases reach 5,838",
     "CDC's Fri update: 43 outbreaks in 2026; US measles-free status lost on 17 Nov.",
     "virus", (-77.0, 38.9)),
    ("N. AMERICA", "TECH", "CONFIRMED — REUTERS",
     "Anthropic slides after record IPO",
     "Shares fall about 10% on Fri after Thu's $81.3bn debut closed up 17% at $97.17.",
     "chip", (-122.4, 37.8)),
    ("EUROPE", "POLITICS", "CONFIRMED — REUTERS",
     "UK and EU sign new deals",
     "Pacts on food trade, carbon markets and youth mobility — a reset step for both sides.",
     "deals", (4.35, 50.85)),
    ("N. AMERICA", "JUSTICE", "CONFIRMED — AP",
     "Palisades Fire: man convicted",
     "LA jury finds Jonathan Rinderknecht guilty of starting the January wildfire.",
     "fire", (-118.2, 34.0)),
    ("ASIA", "POLITICS", "CONFIRMED — AP",
     "Violence flares in Bangladesh",
     "Political clashes break out ahead of Sheikh Hasina's return; streets tense in Dhaka.",
     "protest", (90.4, 23.8)),
    ("EUROPE", "SECURITY", "CONFIRMED — REUTERS",
     "Estonia to shut Russia crossings",
     "Tallinn orders border crossings shut after a sabotage attack, officials say.",
     "border", (25.0, 58.5)),
    ("AFRICA", "DISASTER", "CONFIRMED — AP",
     "Funeral boat capsizes in Nigeria",
     "A boat carrying mourners overturns in Bayelsa State; a rescue is under way.",
     "boat", (6.3, 4.8)),
    ("EUROPE", "SPORT", "CONFIRMED — AP",
     "Alcaraz stays perfect in Turin",
     "Carlos Alcaraz beats Flavio Cobolli to stay unbeaten in his ATP Finals group.",
     "tennis", (7.7, 45.0)),
]

ALSO_ON = [
    "Russia invites Europeans to Moscow for talks",
    "Zelenskyy calls Putin a killer after the barrage",
    "Israeli strikes kill Palestinians in Gaza",
    "Iran war nears its ninth month; Trump in no rush",
    "Iraqi forces enter Jurf al-Nasr, first time in 12 years",
    "Texas execution lasting an hour draws scrutiny",
    "Judge approves $7.25bn Bayer Roundup settlement",
    "Indian man jailed 19 years over Sikh murder plot",
    "Migrant boat capsizes off the Senegal coast",
    "Japan core inflation rises to its high for the year",
    "Argentina bonds slide into distress",
    "Philippines and Chile sign a free-trade deal",
    "Lufthansa to cut up to 1,000 jobs on fuel costs",
    "BepiColombo closes on Mercury; capture due 21 Nov",
    "Lauren Price becomes undisputed welterweight champ",
    "A Lim Kim makes a hole-in-one at the LPGA finale",
    "Pill hailed as breakthrough for pancreatic cancer",
    "Trump threatens 'tremendous tax' on AI centres abroad",
    "Haitian forces kill 34 suspected gang members",
    "Bukele registers for a third term in El Salvador",
    "Saudi Arabia and Japan agree an oil stockpile deal",
    "Bitcoin slips below $60,000; gold nears $3,500",
    "Taiwan's Taiex suffers its worst week since 1990",
    "Dow falls 950 points; VIX highest since April 2025",
    "Traders price 98% chance of a Fed rise in December",
    "Sensex rises 2.3% as Asia's sell-off spares India",
    "Brent crude holds near $90 a barrel",
    "France seeks UN Security Council meeting on Kyiv",
    "Austrian embassy hit in Kyiv barrage; Dutch mission hurt",
    "Polish and NATO jets scrambled; Patriots activated",
    "Panama may block a COP31 deal without a phase-out",
    "US consumer sentiment data lands as markets slide",
    "South Korea exam hit by a cheating scandal",
    "Three Kyiv bridges damaged; Dnipro traffic curbed",
]

TIMELINE = [
    ("OVERNIGHT", "Russia's barrage hits Kyiv; missiles land in Poland"),
    ("MORNING", "Asia plunges: Nikkei -5.1%, Kospi -5.2%"),
    ("MIDDAY", "COP31 talks run into overtime in Antalya"),
    ("AFTERNOON", "Wall Street rout: S&P 500 -3.7% into correction"),
    ("EVENING", "M6.7 quake shakes Peru; felt in Lima"),
]

DATE_CHECK = (
    "LEFT OUT ON PURPOSE — broke before Friday: ICJ verdict delivered Thu 19 Nov · "
    "Shenzhen summit held Thu 19 Nov · Anthropic IPO debut Thu 19 Nov · PAHO measles "
    "ruling Tue 17 Nov · Dow first closed below 50,000 Thu 19 Nov · Kerch Bridge span "
    "severed earlier in the week.  NOT YET: BepiColombo enters Mercury orbit Sat 21 Nov."
)

FOOTER = (
    "Every story here happened or was first reported on Friday 20 November 2026. "
    "CLAIM = one side's account, not independently confirmed. "
    "Sources: AP, Reuters, AFP, CNN, USGS, CDC, ESA. All drawings original."
)

# ------------------------------------------------------------------ art
def draw_art(d, x0, y0, w, h, kind, bg):
    """Flat vector-style scene in the panel's art band."""
    d.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], fill=bg)
    cx, cy = x0 + w // 2, y0 + h // 2
    white = (255, 255, 255)
    dark = (26, 26, 26)
    if kind == "missile":
        d.polygon([(x0 + 30, cy + 6), (x0 + 150, cy - 8), (x0 + 175, cy),
                   (x0 + 150, cy + 8)], fill=white)
        d.line([(x0 + 30, cy + 4), (x0 + 8, cy + 12)], fill=white, width=3)
        d.line([(x0 + 30, cy - 2), (x0 + 12, cy - 10)], fill=white, width=2)
        for px, py in ((x0 + 200, cy - 10), (x0 + 212, cy + 6), (x0 + 196, cy + 12)):
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 210, 80))
    elif kind == "barrage":
        for bx in range(x0 + 12, x0 + w - 20, 26):
            d.rectangle([bx, y0 + h - 22, bx + 16, y0 + h - 6], fill=dark)
        for i in range(5):
            sx = x0 + 18 + i * 42
            d.line([(sx, y0 + 4), (sx + 12, y0 + 16)], fill=white, width=2)
            d.ellipse([sx + 9, y0 + 14, sx + 15, y0 + 20], fill=(255, 210, 80))
    elif kind == "summit":
        d.rectangle([x0 + 40, cy + 2, x0 + w - 40, cy + 8], fill=dark)
        for i, col in enumerate(((164, 18, 32), (31, 58, 95), (176, 106, 0))):
            fx = x0 + 62 + i * 52
            d.rectangle([fx, cy - 16, fx + 26, cy + 2], fill=col)
            d.ellipse([fx + 4, cy - 30, fx + 22, cy - 12], fill=white)
    elif kind == "court":
        d.polygon([(x0 + 60, y0 + 6), (x0 + w - 60, y0 + 6), (cx, y0 + 18)],
                  fill=white)
        for i in range(4):
            px = x0 + 68 + i * 30
            d.rectangle([px, y0 + 20, px + 10, y0 + h - 6], fill=white)
        d.rectangle([x0 + 56, y0 + h - 6, x0 + w - 56, y0 + h - 2], fill=white)
    elif kind == "market":
        pts = [(x0 + 10, y0 + 8), (x0 + 55, y0 + 12), (x0 + 95, y0 + 6),
               (x0 + 135, y0 + 18), (x0 + 175, y0 + 26), (x0 + 215, y0 + 30)]
        d.line(pts, fill=(255, 80, 80), width=3)
        d.polygon(pts + [(x0 + 215, y0 + h - 4), (x0 + 10, y0 + h - 4)],
                  fill=(255, 80, 80))
    elif kind == "tower":
        d.rectangle([cx - 12, y0 + 4, cx + 12, y0 + h - 4], fill=dark)
        for yy in range(y0 + 8, y0 + h - 8, 7):
            d.rectangle([cx - 8, yy, cx + 8, yy + 3], fill=(255, 210, 80))
        d.line([(x0 + 10, y0 + 6), (cx - 14, y0 + 16)], fill=white, width=2)
        d.ellipse([cx - 20, y0 + 13, cx - 12, y0 + 21], fill=(255, 210, 80))
    elif kind == "climate":
        d.ellipse([cx - 16, y0 + 3, cx + 16, y0 + h - 3], outline=white, width=3)
        d.arc([cx - 16, y0 + 3, cx + 16, y0 + h - 3], 20, 160, fill=white, width=2)
        d.line([(cx - 16, cy), (cx + 16, cy)], fill=white, width=2)
        for ang in (45, 135, 225, 315):
            import math
            rx = cx + int(24 * math.cos(math.radians(ang)))
            ry = cy + int(12 * math.sin(math.radians(ang)))
            d.line([(cx, cy), (rx, ry)], fill=(255, 210, 80), width=2)
    elif kind == "quake":
        d.polygon([(x0, y0 + h - 6), (x0 + w, y0 + h - 6),
                   (x0 + w, y0 + h - 2), (x0, y0 + h - 2)], fill=dark)
        d.line([(cx - 30, y0 + h - 6), (cx - 8, y0 + 10), (cx + 12, y0 + h - 6)],
               fill=white, width=2)
        d.rectangle([x0 + 16, y0 + 12, x0 + 44, y0 + h - 6], fill=white)
        d.polygon([(x0 + 190, y0 + 14), (x0 + 214, y0 + 14),
                   (x0 + 210, y0 + h - 6), (x0 + 194, y0 + h - 6)], fill=white)
    elif kind == "virus":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=white)
        for i in range(8):
            import math
            a = math.radians(i * 45)
            x1 = cx + int(11 * math.cos(a))
            y1 = cy + int(11 * math.sin(a))
            x2 = cx + int(19 * math.cos(a))
            y2 = cy + int(19 * math.sin(a))
            d.line([(x1, y1), (x2, y2)], fill=white, width=2)
            d.ellipse([x2 - 2, y2 - 2, x2 + 2, y2 + 2], fill=white)
    elif kind == "chip":
        d.rectangle([cx - 14, cy - 12, cx + 14, cy + 12], fill=white)
        d.rectangle([cx - 6, cy - 5, cx + 6, cy + 5], fill=bg)
        for i in range(4):
            px = cx - 10 + i * 7
            d.line([(px, cy - 12), (px, cy - 18)], fill=white, width=2)
            d.line([(px, cy + 12), (px, cy + 18)], fill=white, width=2)
    elif kind == "deals":
        d.rectangle([x0 + 46, y0 + 8, x0 + 96, y0 + h - 8], fill=white)
        d.rectangle([x0 + 136, y0 + 8, x0 + 186, y0 + h - 8], fill=white)
        d.line([(x0 + 96, cy), (x0 + 136, cy)], fill=white, width=3)
        d.polygon([(x0 + 104, cy - 5), (x0 + 112, cy), (x0 + 104, cy + 5)],
                  fill=white)
    elif kind == "fire":
        d.polygon([(cx, y0 + 4), (cx + 12, y0 + 16), (cx + 8, y0 + 24),
                   (cx + 16, y0 + 30), (cx, y0 + h - 4), (cx - 16, y0 + 30),
                   (cx - 8, y0 + 24), (cx - 12, y0 + 16)], fill=(255, 140, 40))
        d.polygon([(cx, y0 + 16), (cx + 6, y0 + 24), (cx, y0 + h - 6),
                   (cx - 6, y0 + 24)], fill=(255, 210, 80))
    elif kind == "protest":
        for i in range(5):
            px = x0 + 40 + i * 38
            d.ellipse([px - 6, y0 + 6, px + 6, y0 + 18], fill=white)
            d.rectangle([px - 7, y0 + 20, px + 7, y0 + h - 4], fill=white)
        d.rectangle([x0 + 8, y0 + 4, x0 + 26, y0 + 16], fill=(255, 210, 80))
    elif kind == "border":
        for i in range(9):
            px = x0 + 20 + i * 24
            d.rectangle([px, y0 + 6, px + 4, y0 + h - 6], fill=white)
        d.line([(x0 + 14, y0 + 12), (x0 + w - 14, y0 + 12)], fill=white, width=2)
        d.line([(x0 + 14, y0 + 22), (x0 + w - 14, y0 + 22)], fill=white, width=2)
    elif kind == "boat":
        d.polygon([(x0 + 60, cy + 2), (x0 + w - 60, cy + 2),
                   (x0 + w - 78, cy + 12), (x0 + 78, cy + 12)], fill=white)
        d.line([(cx, cy + 2), (cx, y0 + 6)], fill=white, width=2)
        d.polygon([(cx, y0 + 6), (cx + 16, cy), (cx, cy)], fill=(255, 210, 80))
        for wx in (x0 + 20, x0 + 90, x0 + 160):
            d.arc([wx, y0 + h - 12, wx + 30, y0 + h - 2], 0, 180,
                  fill=white, width=2)
    elif kind == "tennis":
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(200, 220, 60))
        d.arc([cx - 14, cy - 14, cx + 14, cy + 14], 300, 60, fill=white, width=2)
        d.arc([cx - 14, cy - 14, cx + 14, cy + 14], 120, 240, fill=white, width=2)
        d.ellipse([x0 + 26, y0 + 6, x0 + 44, y0 + 24], outline=white, width=2)
        d.line([(x0 + 36, y0 + 22), (x0 + 28, y0 + 30)], fill=white, width=2)


# ------------------------------------------------------------------ map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 62),
     (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-115, 28),
     (-125, 40), (-150, 60)],
    [(-80, 10), (-60, 5), (-35, -5), (-40, -20), (-55, -35), (-70, -50),
     (-75, -35), (-80, -15)],
    [(-10, 36), (0, 44), (10, 45), (20, 55), (30, 60), (25, 70), (10, 70),
     (0, 60), (-10, 50)],
    [(-17, 15), (-10, 30), (10, 37), (30, 32), (35, 28), (43, 12), (51, 10),
     (40, -5), (35, -20), (20, -35), (12, -18), (8, 4)],
    [(35, 36), (45, 40), (60, 45), (70, 55), (90, 70), (120, 72), (160, 70),
     (180, 65), (160, 55), (140, 40), (127, 35), (120, 22), (105, 10),
     (100, 8), (90, 15), (80, 8), (70, 22), (60, 25), (50, 28), (43, 12)],
    [(113, -22), (130, -12), (142, -11), (150, -22), (153, -32), (140, -38),
     (129, -32), (114, -30)],
]


def project(lon, lat, x0, y0, w, h):
    return (x0 + (lon + 180.0) / 360.0 * w,
            y0 + (90.0 - lat) / 180.0 * h)


# ------------------------------------------------------------------ build
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # top strip
    f_top = font(SANS_B, 11)
    d.text((mx, 12), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=f_top, fill=INK)
    right = "50 STORIES  ·  7 REGIONS"
    d.text((W - mx - f_top.getlength(right), 12), right, font=f_top, fill=RED)
    d.line([(mx, 32), (W - mx, 32)], fill=RULE, width=2)

    # masthead
    f_date = font(SERIF, 46)
    title = "Friday 20 November 2026"
    d.text(((W - f_date.getlength(title)) / 2, 40), title, font=f_date, fill=INK)
    f_sub = font(SERIF_IT, 15)
    sub = "Missiles in Poland  ·  A market rout  ·  A genocide verdict's fallout"
    d.text(((W - f_sub.getlength(sub)) / 2, 92), sub, font=f_sub, fill=MUTED)
    d.line([(mx, 116), (W - mx, 116)], fill=RULE, width=1)

    # timeline bar
    ty, th = 124, 40
    d.rectangle([mx, ty, W - mx, ty + th], fill=NAVY)
    f_tl_h = font(SANS_B, 9)
    f_tl = font(SANS, 10)
    slot_w = (W - 2 * mx) / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        sx = mx + i * slot_w
        d.text((sx + 8, ty + 5), when, font=f_tl_h, fill=(255, 210, 80))
        for j, ln in enumerate(fit_lines(what, f_tl, slot_w - 16, 2)):
            d.text((sx + 8, ty + 17 + j * 11), ln, font=f_tl, fill=(255, 255, 255))
        if i:
            d.line([(sx, ty + 5), (sx, ty + th - 5)], fill=(120, 140, 170), width=1)

    # panels: 4 x 4
    pw, ph, gap = 236, 112, 8
    px0, py0 = mx, 176
    f_tag = font(SANS_B, 9)
    f_head = font(SERIF, 13)
    f_det = font(SANS, 10)
    f_num = font(SANS_B, 11)
    f_chip = font(SANS_B, 8)
    for idx, (region, topic, chip, head, det, kind, _ll) in enumerate(PANELS):
        r, c = divmod(idx, 4)
        x = px0 + c * (pw + gap)
        y = py0 + r * (ph + gap)
        col = REGION_COLOR[region]
        d.rectangle([x, y, x + pw - 1, y + ph - 1], fill=PAPER,
                    outline=(200, 190, 160), width=1)
        # art band
        draw_art(d, x + 1, y + 1, pw - 2, 30, kind, col)
        # chip sits inside the art band, top right, on a white tab
        chip_w = f_chip.getlength(chip) + 8
        d.rectangle([x + pw - chip_w - 5, y + 4, x + pw - 5, y + 17],
                    fill=(255, 255, 255))
        d.text((x + pw - chip_w - 1, y + 6), chip, font=f_chip, fill=col)
        # number badge
        d.ellipse([x + 6, y + 36, x + 24, y + 54], fill=RED)
        num = str(idx + 1)
        d.text((x + 15 - f_num.getlength(num) / 2, y + 39), num,
               font=f_num, fill=(255, 255, 255))
        # tag
        d.text((x + 29, y + 36), "%s · %s" % (region, topic), font=f_tag, fill=col)
        # headline
        hy = y + 56
        for j, ln in enumerate(fit_lines(head, f_head, pw - 12, 2)):
            d.text((x + 6, hy + j * 15), ln, font=f_head, fill=INK)
        # detail
        dy = y + 56 + 2 * 15 + 1
        for j, ln in enumerate(fit_lines(det, f_det, pw - 12, 2)):
            d.text((x + 6, dy + j * 11), ln, font=f_det, fill=(60, 56, 48))

    my = py0 + 4 * ph + 3 * gap + 8  # map top
    # map
    f_sec = font(SANS_B, 12)
    d.text((mx, my), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.line([(mx + 168, my + 8), (W - mx, my + 8)], fill=RULE, width=1)
    map_y, map_h = my + 20, 96
    d.rectangle([mx, map_y, W - mx, map_y + map_h], fill=SEA,
                outline=(200, 190, 160), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx + 2, map_y + 2, W - 2 * mx - 4, map_h - 4)
               for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(150, 130, 90))
    f_pin = font(SANS_B, 8)
    for idx, (_rg, _tp, _ch, _hd, _dt, _k, (lon, lat)) in enumerate(PANELS):
        px, py = project(lon, lat, mx + 2, map_y + 2, W - 2 * mx - 4, map_h - 4)
        px, py = int(px), int(py)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        n = str(idx + 1)
        d.text((px - f_pin.getlength(n) / 2, py - 6), n, font=f_pin,
               fill=(255, 255, 255))

    # ALSO ON ...
    ay = map_y + map_h + 10
    d.text((mx, ay), "ALSO ON FRIDAY 20 NOVEMBER —", font=f_sec, fill=INK)
    d.line([(mx + 268, ay + 8), (W - mx, ay + 8)], fill=RULE, width=1)
    f_also = font(SANS, 9)
    cols, per_col = 3, 12
    col_w = (W - 2 * mx) / cols
    for i, item in enumerate(ALSO_ON):
        c, r = divmod(i, per_col)
        x = mx + c * col_w
        y = ay + 19 + r * 11
        line = fit_lines("· " + item, f_also, col_w - 8, 1)[0]
        d.text((x, y), line, font=f_also, fill=(60, 56, 48))

    # DATE CHECK
    dy = ay + 19 + per_col * 11 + 6
    d.rectangle([mx, dy, W - mx, dy + 50], fill=(238, 228, 200),
                outline=RED, width=1)
    f_dc_h = font(SANS_B, 10)
    f_dc = font(SANS, 10)
    d.text((mx + 8, dy + 5), "DATE CHECK", font=f_dc_h, fill=RED)
    for j, ln in enumerate(fit_lines(DATE_CHECK, f_dc, W - 2 * mx - 16, 3)):
        d.text((mx + 8, dy + 19 + j * 11), ln, font=f_dc, fill=INK)

    # footer
    f_ft = font(SANS, 9)
    fy = dy + 50 + 7
    for j, ln in enumerate(fit_lines(FOOTER, f_ft, W - 2 * mx, 2)):
        d.text((mx, fy + j * 11), ln, font=f_ft, fill=MUTED)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    print(build())
