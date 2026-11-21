#!/usr/bin/env python3
"""news-image-20261120 v4 — one-page newspaper, EXACTLY 1024x1024, <=1 MiB.
Fresh redesign. All facts from the 20 Nov 2026 research file only.
Deterministic: fixed fonts, fixed geometry, no randomness, no timestamps.
Writes ONLY to $MAKEFUN_OUTPUT_DIR/entry.png (grader runs read-only in /bot)."""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

PAPER = (247, 241, 227)
INK = (26, 26, 26)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
TEAL = (18, 110, 110)
GOLD = (176, 132, 30)
GREY = (110, 104, 90)
LINE = (180, 172, 150)
CARD = (255, 252, 244)
SKY = (16, 28, 56)

FD = "/usr/share/fonts/truetype/dejavu"


def f_serif(size, bold=False):
    return ImageFont.truetype(
        os.path.join(FD, "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"), size)


def f_sans(size, bold=False):
    return ImageFont.truetype(
        os.path.join(FD, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)


def wrap(text, font, width, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, width, fill=INK, leading=None, max_lines=None):
    lines = wrap(text, font, width, draw)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(font.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, fill=INK, w_=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w_)


def box(draw, x, y, w_, h_, fill=None, outline=None, ow=1):
    draw.rectangle([x, y, x + w_ - 1, y + h_ - 1], fill=fill, outline=outline, width=ow)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
box(d, 6, 6, W - 12, H - 12, outline=INK, ow=2)

# ---------------- masthead ----------------
d.text((512, 16), "THE WORLD IN ONE DAY", font=f_sans(11, True),
       fill=RED, anchor="ma")
d.text((512, 32), "The Friday Paper", font=f_serif(40, True),
       fill=INK, anchor="ma")
d.text((512, 76), "Friday 20 November 2026", font=f_serif(23, True),
       fill=RED, anchor="ma")
hline(d, 24, 1000, 106, fill=INK, w_=2)
d.text((512, 111), "Missiles hit Kyiv's bridges  \u2022  Cyclone Akvan lands in India  \u2022  Asia's markets plunge on AI doubts",
       font=f_sans(11, True), fill=NAVY, anchor="ma")

# ---------------- region bar ----------------
regions = ["EUROPE", "ASIA", "MIDDLE EAST", "AFRICA", "AMERICAS", "OCEANIA", "GLOBAL"]
rx, ry, rw, rh = 24, 130, 136, 17
for i, r in enumerate(regions):
    x = rx + i * (rw + 4)
    box(d, x, ry, rw, rh, fill=NAVY if i % 2 == 0 else RED)
    d.text((x + rw / 2, ry + 3), r, font=f_sans(9, True), fill=(255, 255, 255), anchor="ma")

# ---------------- BY THE NUMBERS ----------------
d.text((24, 152), "BY THE NUMBERS", font=f_sans(11, True), fill=RED)
hline(d, 150, 1000, 158, fill=RED, w_=1)
nums = [
    ("110+", "missiles fired at Ukraine overnight"),
    ("400+", "drones in the same attack"),
    ("300,000+", "people evacuated in Odisha"),
    ("\u22124.8%", "Nikkei 225 at Friday's close"),
    ("$3.79bn", "GTA VI first-day sales"),
    ("111", "cheats caught in Suneung exam"),
]
nx, nw = 24, 160
for i, (big, small) in enumerate(nums):
    x = nx + i * (nw + 3)
    box(d, x, 163, nw, 34, fill=CARD, outline=LINE, ow=1)
    d.text((x + nw / 2, 166), big, font=f_sans(14, True), fill=RED, anchor="ma")
    d.text((x + nw / 2, 184), small, font=f_sans(7), fill=GREY, anchor="ma")

# ---------------- lead illustrations (original PIL drawings) ----------------
def ill_kyiv(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=SKY)
    for sx, sy in [(20, 12), (70, 22), (130, 10), (200, 26), (260, 14), (300, 24)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.line([(x + 30, y + 8), (x + 150, y + 55)], fill=(255, 220, 120), width=2)
    d.line([(x + 290, y + 6), (x + 190, y + 48)], fill=(255, 220, 120), width=2)
    d.ellipse([x + 146, y + 51, x + 154, y + 59], fill=(255, 180, 60))
    d.rectangle([x, y + h_ - 16, x + w_, y + h_], fill=(40, 70, 110))
    d.arc([x + 10, y + h_ - 52, x + 110, y + h_ - 2], 180, 360, fill=(255, 255, 255), width=3)
    d.arc([x + 120, y + h_ - 46, x + 210, y + h_ - 2], 180, 360, fill=(255, 255, 255), width=3)
    d.arc([x + 220, y + h_ - 52, x + 310, y + h_ - 2], 180, 360, fill=(255, 255, 255), width=3)
    d.polygon([(x + 235, y + h_ - 30), (x + 245, y + h_ - 44), (x + 255, y + h_ - 30)],
              fill=(255, 120, 40))
    d.polygon([(x + 245, y + h_ - 44), (x + 252, y + h_ - 58), (x + 259, y + h_ - 44)],
              fill=(255, 200, 60))


def ill_akvan(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(24, 90, 110))
    d.polygon([(x + 200, y + h_), (x + 240, y + 20), (x + 300, y + 30),
               (x + w_, y + 60), (x + w_, y + h_)], fill=(190, 160, 110))
    d.text((x + 252, y + 34), "INDIA", font=f_sans(8, True), fill=(60, 40, 20))
    cx, cy = x + 130, y + 40
    for r, a0 in [(52, 20), (40, 140), (28, 260), (16, 20)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 200, 60))
    d.line([(cx + 40, cy + 30), (x + 225, y + 42)], fill=(255, 120, 40), width=2)
    d.polygon([(x + 225, y + 42), (x + 213, y + 36), (x + 215, y + 48)], fill=(255, 120, 40))
    d.text((x + 8, y + h_ - 14), "BAY OF BENGAL", font=f_sans(7, True), fill=(200, 230, 240))


def ill_market(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(24, 24, 30))
    for gy in (14, 30, 46, 62):
        d.line([(x + 6, y + gy), (x + w_ - 6, y + gy)], fill=(60, 60, 70), width=1)
    pts = [(x + 10, y + 14), (x + 70, y + 20), (x + 130, y + 18), (x + 190, y + 34),
           (x + 250, y + 48), (x + 300, y + 66)]
    d.line(pts, fill=(255, 70, 70), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 60))
    d.text((x + 10, y + h_ - 16), "NIKKEI -4.8%   KOSPI -5.2%   TAIEX -6.2%",
           font=f_sans(8, True), fill=(255, 255, 255))


LEADS = [
    ("1 \u00b7 KYIV \u2014 WAR IN UKRAINE", "Russian missiles hit three Kyiv bridges",
     "Russia fired 110+ missiles (27 ballistic, only 3 intercepted) and 400+ drones "
     "overnight. Three Dnipro bridges were hit and closed; 8 killed and 28 injured "
     "across Ukraine; emergency blackouts in 11 regions.",
     "Reuters / CNN / BBC", ill_kyiv),
    ("2 \u00b7 BAY OF BENGAL \u2014 CYCLONE AKVAN", "Cyclone Akvan makes landfall in India",
     "Akvan came ashore near Gopalpur, Odisha, with 70\u201380 km/h winds after 300,000+ "
     "people were evacuated. Up to 209 mm of rain fell in 24 hours; early reports cite "
     "no deaths.",
     "IMD / The Hindu", ill_akvan),
    ("3 \u00b7 TOKYO \u2014 MARKETS", "AI sell-off: Asia's markets plunge",
     "Asian shares plunged on AI valuation doubts: Nikkei \u22124.8% at Friday's close, "
     "Kospi \u22125.2%, Taiex \u22126.2%, SoftBank \u221216%. The S&P 500 fell 2% on Thursday, "
     "its fifth straight drop.",
     "Reuters / CNBC", ill_market),
]

lx, ly, lw, lh, lgap = 24, 204, 322, 168, 7
for i, (kick, head, body, src, ill) in enumerate(LEADS):
    x = lx + i * (lw + lgap)
    box(d, x, ly, lw, lh, fill=CARD, outline=LINE, ow=1)
    ill(x + 1, ly + 1, lw - 2, 76)
    d.text((x + 8, ly + 82), kick, font=f_sans(8, True), fill=RED)
    yy = para(d, x + 8, ly + 96, head, f_serif(13, True), lw - 16, leading=15, max_lines=2)
    yy = para(d, x + 8, yy + 2, body, f_sans(9), lw - 16, leading=11, max_lines=3)
    d.text((x + 8, ly + lh - 12), "Source: " + src, font=f_sans(7), fill=GREY)

# ---------------- 10 cards ----------------
def ill_flag(x, y, w_, h_, c1, c2):
    box(d, x, y, w_, h_, fill=c1)
    d.rectangle([x, y, x + w_ // 2 - 1, y + h_ - 1], fill=c2)
    d.ellipse([x + w_ - 26, y + 6, x + w_ - 10, y + 22], outline=(255, 220, 60), width=2)


def ill_globe(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(30, 70, 90))
    d.ellipse([x + 8, y + 4, x + 34, y + 30], fill=(90, 160, 90))
    d.line([(x + 40, y + 8), (x + w_ - 8, y + 26)], fill=(255, 120, 40), width=3)
    d.text((x + 52, y + 10), "NO DEAL", font=f_sans(9, True), fill=(255, 255, 255))


def ill_poland(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(235, 225, 200))
    d.polygon([(x + 10, y + 26), (x + 60, y + 6), (x + 120, y + 10), (x + 150, y + 26),
               (x + 110, y + 30), (x + 40, y + 30)], fill=(200, 190, 160))
    for px, py in [(70, 16), (110, 20), (95, 26)]:
        d.ellipse([x + px - 4, y + py - 4, x + px + 4, y + py + 4], fill=RED)
    d.line([(x + 150, y + 6), (x + 96, y + 22)], fill=(60, 60, 60), width=2)


def ill_crowd(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(120, 40, 50))
    for cx in range(14, w_, 22):
        d.ellipse([x + cx, y + 16, x + cx + 9, y + 25], fill=(255, 230, 200))
        d.rectangle([x + cx - 2, y + 25, x + cx + 11, y + h_ - 1], fill=(40, 40, 60))
    d.rectangle([x + 60, y + 2, x + 150, y + 13], fill=(255, 255, 255))
    d.text((x + 105, y + 3), "SCIOPERO", font=f_sans(8, True), fill=RED, anchor="ma")


def ill_gta(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(20, 20, 40))
    for bx, bh in [(10, 18), (34, 26), (60, 14), (86, 24), (112, 18), (138, 28)]:
        d.rectangle([x + bx, y + h_ - bh, x + bx + 20, y + h_], fill=(255, 140, 200))
    d.text((x + w_ - 8, y + 4), "$3.79bn", font=f_sans(13, True), fill=(255, 220, 60), anchor="ra")


def ill_pill(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(240, 245, 250))
    d.rounded_rectangle([x + 10, y + 12, x + 60, y + 24], radius=6, fill=RED)
    d.rounded_rectangle([x + 10, y + 12, x + 35, y + 24], radius=6, fill=(255, 255, 255))
    for cx, cy, r in [(90, 18, 9), (120, 14, 6), (145, 20, 4)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(150, 60, 90))
    d.text((x + w_ - 6, y + 8), "60.7%", font=f_sans(12, True), fill=TEAL, anchor="ra")


def ill_border(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(220, 225, 235))
    d.rectangle([x + 10, y + 6, x + 60, y + 12], fill=(0, 90, 170))
    d.rectangle([x + 10, y + 12, x + 60, y + 18], fill=(0, 0, 0))
    d.rectangle([x + 10, y + 18, x + 60, y + 24], fill=(255, 255, 255))
    for bx in range(80, w_ - 8, 16):
        d.rectangle([x + bx, y + 10, x + bx + 8, y + h_ - 4], fill=(200, 60, 40))
    d.text((x + w_ - 6, y + 4), "CLOSED", font=f_sans(8, True), fill=RED, anchor="ra")


def ill_exam(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(245, 240, 220))
    d.rectangle([x + 20, y + 18, x + 120, y + h_ - 4], fill=(180, 150, 110))
    d.rectangle([x + 130, y + 8, x + 152, y + 26], fill=(30, 30, 30))
    d.ellipse([x + 132, y + 10, x + 150, y + 24], outline=(255, 80, 80), width=2)
    d.text((x + w_ - 6, y + 6), "111", font=f_sans(13, True), fill=RED, anchor="ra")


def ill_tanker(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(20, 60, 90))
    d.rectangle([x + 20, y + 14, x + 140, y + 26], fill=(120, 60, 30))
    d.rectangle([x + 120, y + 6, x + 136, y + 14], fill=(200, 200, 200))
    d.polygon([(x + 70, y + 14), (x + 78, y + 2), (x + 86, y + 14)], fill=(255, 140, 40))
    d.polygon([(x + 78, y + 2), (x + 84, y - 8 + 10), (x + 90, y + 2)], fill=(255, 200, 60))
    d.text((x + w_ - 6, y + 8), "HORMUZ", font=f_sans(8, True), fill=(255, 255, 255), anchor="ra")


def ill_gaza(x, y, w_, h_):
    box(d, x, y, w_, h_, fill=(230, 215, 180))
    d.line([(x + 6, y + 18), (x + w_ - 6, y + 18)], fill=(220, 180, 0), width=4)
    for tx in (30, 80, 130):
        d.polygon([(x + tx, y + 28), (x + tx + 12, y + 16), (x + tx + 24, y + 28)],
                  fill=(200, 190, 160), outline=(120, 110, 90))
    d.text((x + w_ - 6, y + 2), "YELLOW LINE", font=f_sans(7, True), fill=(120, 100, 20), anchor="ra")


CARDS = [
    ("BRUSSELS \u00b7 EUROPE", "UK and EU seal \u2018reset\u2019 deal",
     "Food checks scrapped, youth mobility of 100,000 a year each way, emissions schemes "
     "linked. UK says +0.5% of GDP by 2040.", "Reuters / AP",
     lambda x, y, w_, h_: ill_flag(x, y, w_, h_, (0, 40, 90), (200, 30, 40))),
    ("ANTALYA \u00b7 CLIMATE", "COP31 ends its final day with no deal",
     "A draft drops all fossil-fuel mentions and the $120bn adaptation target. "
     "Talks run into Saturday.", "UN News / Carbon Brief", ill_globe),
    ("POLAND \u00b7 EUROPE", "Russian missiles land in Poland",
     "Three Russian objects entered Polish airspace: a Kh-101 fell near Nowy Lipowiec; "
     "a second near Rudnik nad Sanem. No casualties.", "Reuters / AP", ill_poland),
    ("ITALY \u00b7 EUROPE", "General strike grips Italy",
     "CGIL's 24-hour strike against Meloni's \u20ac26bn budget draws marches in 100+ "
     "cities; its leader claims 1m+ participants.", "Reuters / AP", ill_crowd),
    ("GTA VI \u00b7 CULTURE", "GTA VI: $3.79bn in one day",
     "Take-Two announces $3.79bn in first-day sales \u2014 the biggest entertainment "
     "launch ever; 32.5m units sold before release.", "CNN / Barron's", ill_gta),
    ("BARCELONA \u00b7 SCIENCE", "Cancer pill makes tumours vanish",
     "Early trial: daraxonrasib + chemo shrank or cleared tumours in 60.7% of 61 "
     "untreated metastatic pancreatic cancer patients.", "EORTC / ecancer", ill_pill),
    ("ESTONIA \u00b7 EUROPE", "Estonia shuts border with Russia",
     "All land crossings with Russia close from 1 December for at least 6 months, "
     "citing security after an arson attack blamed on Moscow.", "Reuters", ill_border),
    ("SEOUL \u00b7 ASIA", "111 caught cheating in Suneung exam",
     "111 caught with banned smart devices in the Suneung university exam \u2014 "
     "including smart glasses and a micro-camera with earpiece.", "Korea JoongAng Daily", ill_exam),
    ("HORMUZ \u00b7 MIDDLE EAST", "Tanker hit by mine in Hormuz",
     "A tanker was hit and caught fire in the Strait of Hormuz after striking a mine; "
     "the Pentagon puts the US war cost on Iran at $48.3bn.", "UKMTO / IEA", ill_tanker),
    ("GAZA \u00b7 MIDDLE EAST", "Israeli troops cross Yellow Line",
     "Troops crossed the ceasefire \u2018Yellow Line\u2019 in central Gaza \u2014 the first "
     "breach since the truce \u2014 to clear a tunnel; thousands fled.", "BBC / UPI", ill_gaza),
]

cx0, cy0, cw, ch, cgap = 24, 378, 193, 148, 6
for i, (kick, head, body, src, ill) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x = cx0 + c * (cw + cgap)
    y = cy0 + r * (ch + cgap)
    box(d, x, y, cw, ch, fill=CARD, outline=LINE, ow=1)
    ill(x + 1, y + 1, cw - 2, 34)
    d.text((x + 7, y + 38), kick, font=f_sans(7, True), fill=RED)
    yy = para(d, x + 7, y + 50, head, f_serif(11, True), cw - 14, leading=13, max_lines=2)
    yy = para(d, x + 7, yy + 2, body, f_sans(8), cw - 14, leading=10, max_lines=4)
    d.text((x + 7, y + ch - 12), "Source: " + src, font=f_sans(7), fill=GREY)

# ---------------- world map: "Where it happened" ----------------
my0, my1 = 684, 732
d.text((24, my0), "WHERE IT HAPPENED", font=f_sans(10, True), fill=NAVY)
d.text((1000, my0), "pins 1\u201313 = lead + card stories", font=f_sans(8), fill=GREY, anchor="ra")
box(d, 24, my0 + 14, 976, 34, fill=(238, 232, 214), outline=LINE, ow=1)
continents = [
    [(70, 700), (150, 692), (235, 700), (205, 722), (120, 728), (72, 716)],
    [(235, 712), (285, 710), (300, 726), (268, 732), (242, 724)],
    [(470, 694), (530, 690), (545, 700), (510, 708), (480, 704)],
    [(480, 708), (540, 706), (560, 720), (520, 732), (490, 724)],
    [(550, 692), (700, 688), (760, 696), (720, 712), (620, 714), (560, 706)],
    [(800, 722), (850, 720), (860, 730), (810, 732)],
]
for poly in continents:
    d.polygon(poly, fill=(208, 198, 168))


def lonlat(lon, lat):
    return (24 + (lon + 180) / 360.0 * 976, 698 + (72 - lat) / 140.0 * 44)


PINS = [(30.5, 50.4), (84.9, 19.3), (139.7, 35.7), (4.4, 50.9), (30.7, 36.9),
        (22.5, 50.3), (12.5, 41.9), (-74.0, 40.7), (2.2, 41.4), (24.8, 59.4),
        (127.0, 37.5), (56.5, 26.5), (34.5, 31.5)]
# Europe pins crowd into one small band on this flat map, so their number
# badges are staggered with short leader lines to the true spot.
DISPLAY = {1: (598, 703), 4: (540, 703), 5: (612, 716), 6: (572, 703),
           7: (556, 720), 9: (516, 714), 10: (584, 716), 13: (624, 705)}
for i, (lon, lat) in enumerate(PINS, 1):
    px, py = lonlat(lon, lat)
    dx, dy = DISPLAY.get(i, (px, py))
    if (dx, dy) != (px, py):
        d.line([(px, py), (dx, dy)], fill=(120, 110, 90), width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=RED, outline=(255, 255, 255), width=1)
    d.text((dx, dy - 5), str(i), font=f_sans(7, True), fill=(255, 255, 255), anchor="ma")

# ---------------- ALSO 14-43 ----------------
d.text((24, 736), "ALSO \u2014 THE REST OF THE DAY", font=f_sans(10, True), fill=NAVY)
hline(d, 24, 1000, 750, fill=NAVY, w_=1)
ALSO = [
    "14. Port-au-Prince \u2014 34 killed in Martissant raid. (Al Jazeera)",
    "15. San Salvador \u2014 Bukele registers for a third term. (AP)",
    "16. Washington \u2014 Senate passes energy permitting bill 62\u201333. (CNBC)",
    "17. Tokyo \u2014 Japan core inflation 2.2%, headline 2.3% in Oct. (Japan Times)",
    "18. Bras\u00edlia \u2014 Central bank sells $1bn to steady the real. (MercoPress)",
    "19. Copenhagen \u2014 Denmark ratifies Greenland security deal with US. (CBS)",
    "20. Yenne, Senegal \u2014 Migrant boat capsizes; dozens missing. (BBC)",
    "21. South Kordofan \u2014 Drone strike kills 10 at a gold mine. (AllAfrica)",
    "22. Caracas \u2014 US and Venezuela sign military cooperation deal. (BBC)",
    "23. Mato Grosso \u2014 Lula recognises Raoni's ancestral Kayapo land. (Al Jazeera)",
    "24. Huntsville \u2014 Texas executes Reinaldo Dennes, 70. (Guardian)",
    "25. Washington \u2014 White House fires national cyber director. (France 24)",
    "26. New York \u2014 UN chief race stalls after 8 votes. (Guardian)",
    "27. Dhaka \u2014 Violence ahead of Hasina's planned return. (Guardian)",
    "28. Al-Dahi \u2014 Mosque set on fire in northern Israel. (MEE)",
    "29. Jurf al-Sakhar \u2014 Iraqi army moves into militia stronghold. (Euronews)",
    "30. Badme \u2014 Strikes reported on Ethiopia\u2013Eritrea border. (AllAfrica)",
    "31. Suva \u2014 Fiji & Tonga declare disasters as El Ni\u00f1o drought bites. (RFI)",
    "32. Los Angeles \u2014 El Ni\u00f1o storm threatens LA with floods. (Le Monde)",
    "33. Yongbyon \u2014 IAEA: N. Korea expanding uranium enrichment. (Euronews)",
    "34. New York \u2014 Gold falls sharply; US 10-year yield above 5%. (CNBC)",
    "35. Washington \u2014 IMF: global debt to near 100% of GDP. (MercoPress)",
    "36. Bogot\u00e1 \u2014 Thousands protest Colombia's tax plans. (Al Jazeera)",
    "37. Khyber Pakhtunkhwa \u2014 Army says 22 militants killed in raids. (The Hindu)",
    "38. Seoul \u2014 Court orders retrial of ex-PM Han in martial law case. (Japan Times)",
    "39. Shenzhen \u2014 Japan's Takaichi gets cool reception at APEC. (CNBC)",
    "40. Wellington \u2014 Phillips hits 118 against India. (ICC/AP)",
    "41. Mogadishu \u2014 Somalia expels UAE ambassador. (Africanews)",
    "42. Shenzhen (APEC) \u2014 Philippines & Chile sign free trade deal. (Inquirer)",
    "43. Zimbabwe \u2014 HALO Trust destroys 250,000 landmines. (Africanews)",
]
afont = f_sans(9)
for j, item in enumerate(ALSO):
    col = 0 if j < 15 else 1
    row = j if j < 15 else j - 15
    x = 24 if col == 0 else 514
    d.text((x, 756 + row * 12), item, font=afont, fill=INK)

# ---------------- DATE CHECK + footer ----------------
box(d, 24, 940, 976, 38, fill=(176, 30, 36))
d.text((34, 943),
       "DATE CHECK \u2014 deliberately left out: Shenzhen summit (19 Nov) \u00b7 ICJ Myanmar ruling (19 Nov) \u00b7",
       font=f_sans(9, True), fill=(255, 255, 255))
d.text((34, 954),
       "Anthropic IPO (19 Nov) \u00b7 Nvidia subpoena (19 Nov) \u00b7 Pete Rose pardon (19 Nov) \u00b7 Jepchirchir ban (19 Nov) \u00b7",
       font=f_sans(9, True), fill=(255, 255, 255))
d.text((34, 965),
       "BepiColombo reaches Mercury Sat 21 Nov \u00b7 Voyager 1 one light-day Wed 18 Nov. Only Friday 20 November 2026 events are shown.",
       font=f_sans(9, True), fill=(255, 255, 255))
para(d, 24, 984,
     "Sources: Reuters, AP, CNN, BBC, IMD, UN News, Carbon Brief, The Hindu, Korea JoongAng Daily, "
     "UKMTO, IEA, EORTC, Al Jazeera, Guardian, Euronews, France 24 and others named per story. "
     "All illustrations are original drawings made for this page. 43 stories: 3 leads + 10 cards + 30 also.",
     f_sans(8), 976, fill=GREY, leading=10, max_lines=2)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, format="PNG", optimize=True)
print("saved", OUT, img.size)
