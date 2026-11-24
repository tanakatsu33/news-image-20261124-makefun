"""Dense one-page front for Tuesday 24 November 2026: 35 sourced, badged stories.

Flat shapes + type only. Every text block is measured with textlength and
wrapped programmatically; anything that would leave its box is reported as a
warning instead of silently spilling.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 240, 226)
PANEL = (238, 230, 212)
INK = (28, 26, 24)
SOFT = (92, 86, 78)
RULE = (150, 140, 126)
ACCENT = (160, 28, 28)
GREY = (118, 112, 104)
LAND = (196, 184, 162)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/noto/"
BOLD = FD + "NotoSans-Bold.ttf"
SC = FD + "NotoSans-SemiCondensed.ttf"
SCB = FD + "NotoSans-SemiCondensedBold.ttf"
SCSB = FD + "NotoSans-SemiCondensedSemiBold.ttf"
CB = FD + "NotoSansDisplay-CondensedBold.ttf"
SERIF_BLACK = FD + "NotoSerif-Black.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 24
warnings = []
_fc = {}

# Glyph guard: warn whenever a string uses a character its font lacks (no tofu boxes).
try:
    from fontTools.ttLib import TTFont
    _cmaps = {}

    def _missing(s, f):
        path = f.path
        if path not in _cmaps:
            _cmaps[path] = TTFont(path).getBestCmap()
        return {ch for ch in s if not ch.isspace() and ord(ch) not in _cmaps[path]}
except ImportError:  # pragma: no cover
    def _missing(s, f):
        return set()

_raw_text = d.text


def _checked_text(xy, s, *a, **kw):
    miss = _missing(s, kw["font"])
    if miss:
        warnings.append(f"missing glyphs {sorted(miss)} in {kw['font'].path.split('/')[-1]}: {s!r}")
    return _raw_text(xy, s, *a, **kw)


d.text = _checked_text


def font(path, size):
    key = (path, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(path, size)
    return _fc[key]


def tw(s, f):
    return d.textlength(s, font=f)


def wrap(s, f, width):
    lines, cur = [], ""
    for w in s.split():
        trial = (cur + " " + w).strip()
        if tw(trial, f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(x, y, s, f, width, lh, fill, max_lines=None, tag=""):
    lines = wrap(s, f, width)
    if max_lines and len(lines) > max_lines:
        warnings.append(f"{tag}: {len(lines)} lines > {max_lines}: {s!r}")
    for ln in lines:
        if tw(ln, f) > width:
            warnings.append(f"{tag}: line too wide: {ln!r}")
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def check_bottom(y, limit, tag):
    if y > limit:
        warnings.append(f"{tag}: content bottom {y:.0f} > box bottom {limit:.0f}")


def centered(y, s, f, fill):
    d.text(((W - tw(s, f)) / 2, y), s, font=f, fill=fill)


def chip(x, y, label, size=10):
    """Verification badge. One system, three fills."""
    f = font(SCB, size)
    pad = 4
    w = tw(label, f) + 2 * pad
    h = size + 5
    if label == "CONFIRMED":
        d.rectangle([x, y, x + w, y + h], fill=ACCENT)
        col = WHITE
    elif label == "OFFICIAL":
        d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=ACCENT, width=1)
        col = ACCENT
    else:  # REPORTED
        d.rectangle([x, y, x + w, y + h], fill=GREY)
        col = WHITE
    d.text((x + pad, y + h / 2), label, font=f, fill=col, anchor="lm")
    return w


def source_line(x, y, source, badge, width, size=12, tag=""):
    f = font(SCSB, size)
    d.text((x, y), source, font=f, fill=SOFT)
    sx = x + tw(source, f) + 6
    cw = chip(sx, y + 2, badge, size=size - 2)
    if sx + cw - x > width:
        warnings.append(f"{tag}: source+badge too wide")


# ======================= 1. MASTHEAD =======================
y = 12
centered(y, "THE WORLD IN ONE PICTURE", font(BOLD, 15), ACCENT)
y += 18
f_date = font(SERIF_BLACK, 62)
date = "TUESDAY 24 NOVEMBER 2026"
if tw(date, f_date) > W - 2 * M:
    warnings.append("date too wide")
centered(y - 6, date, f_date, INK)
y += 78
centered(y, "35 STORIES · EVERY STORY SOURCED AND BADGED", font(SCB, 14), SOFT)
y += 22
d.line([M, y, W - M, y], fill=INK, width=3)
d.line([M, y + 5, W - M, y + 5], fill=INK, width=1)
y += 12

# ======================= 2. LEAD BAND =======================
lead_top = y
d.text((M, y), "LEAD · CLIMATE — ANTALYA", font=font(SCB, 13), fill=ACCENT)
y += 17
f_lead = font(BOLD, 40)
d.text((M, y - 4), "COP31 ENDS WITH NO DEAL", font=f_lead, fill=INK)
hl_w = tw("COP31 ENDS WITH NO DEAL", f_lead)
# badge + source to the right of the headline
bx = M + hl_w + 18
cw = chip(bx, y + 10, "CONFIRMED", size=13)
d.text((bx + cw + 8, y + 9), "Reuters", font=font(SCSB, 15), fill=SOFT)
y += 50
y = block(M, y, "Climate talks collapse as Saudi-led oil states force every mention of fossil "
          "fuels out of the text — the first failure to reach a political agreement since 2009.",
          font(SC, 16), W - 2 * M, 20, INK, max_lines=2, tag="lead summary")
y += 6
d.line([M, y, W - M, y], fill=RULE, width=1)
y += 6

# ======================= 3. NUMBERS STRIP =======================
nums = [
    ("≈500,000", "Russian war dead in leaked data"),
    ("$44bn", "CrowdStrike–Zscaler deal"),
    ("810,592", "Hondas recalled in the US"),
    ("222,000", "EU early deaths tied to dirty air"),
    ("7.3m", "people's food aid at risk from wars"),
    ("24", "dead in the Banten factory fire"),
]
strip_top = y
d.rectangle([M, y, W - M, y + 44], fill=INK)
f_lab = font(SCB, 12)
f_num = font(CB, 16)
f_approx = font(FD + "NotoSansMono-CondensedBold.ttf", 16)  # Noto Sans lacks the ≈ glyph
f_txt = font(SC, 13)
d.text((M + 8, y + 6), "THE DAY", font=f_lab, fill=(240, 196, 120))
d.text((M + 8, y + 22), "IN NUMBERS", font=f_lab, fill=(240, 196, 120))
nx0 = M + 90
row_w = W - M - 8 - nx0
sep = " · "
rows = [nums[:3], nums[3:]]
for ri, row in enumerate(rows):
    x = nx0
    ry = y + 4 + ri * 19
    for i, (n, t) in enumerate(row):
        if i:
            d.text((x, ry + 1), sep, font=f_txt, fill=(200, 190, 170))
            x += tw(sep, f_txt)
        if n.startswith("≈"):
            d.text((x, ry - 1), "≈", font=f_approx, fill=WHITE)
            x += tw("≈", f_approx)
            n = n[1:]
        d.text((x, ry - 1), n, font=f_num, fill=WHITE)
        x += tw(n, f_num) + 4
        d.text((x, ry + 1), t, font=f_txt, fill=(225, 218, 205))
        x += tw(t, f_txt)
    if x > W - M - 4:
        warnings.append(f"numbers row {ri}: overflows by {x - (W - M - 4):.0f}px")
y += 44 + 8

# ======================= 4. FEATURED GRID =======================
featured = [
    ("SPACE SECURITY", "Allies: Russia may orbit a nuclear weapon",
     "Reports say Moscow's nuclear-armed 'Sputnik-S' satellite could launch next month; NATO vows to defend space",
     "Japan Times", "REPORTED"),
    ("TECH", "Nvidia brings back Huang as CEO",
     "Reinstated under pressure from Trump; shares leapt about a third as Wall Street rallied",
     "Reuters", "CONFIRMED"),
    ("UKRAINE WAR", "Hacked data puts Russian toll near 500,000",
     "New leaked figures put Russia's military deaths in Ukraine close to half a million",
     "Japan Times", "REPORTED"),
    ("INDONESIA", "Factory fire kills 24; 30 still missing",
     "Rescuers search the ruins of a Banten candy factory near Jakarta",
     "Qatar Tribune", "CONFIRMED"),
    ("KOREA", "Seoul scrambles jets at Russian warplanes",
     "Russian aircraft entered South Korea's air defence zone, its military says",
     "Japan Times", "OFFICIAL"),
    ("BANGLADESH", "Hasina to return home on Dec 16",
     "The ousted PM, facing a death sentence, plans to fly back on the state carrier",
     "Reuters", "OFFICIAL"),
    ("BRITAIN", "No EU return without a referendum",
     "PM Burnham calls rejoining the EU without a public vote 'unthinkable'",
     "Reuters", "CONFIRMED"),
    ("MARKETS", "Gold rebounds from a 14-month low",
     "Spot gold at $3,645 an ounce as traders await US inflation data",
     "Reuters", "CONFIRMED"),
]
GAP = 10
PW = (W - 2 * M - 3 * GAP) / 4
PH = 136
f_k = font(SCB, 12)
f_h = font(SCB, 18)
f_s = font(SC, 13)
for i, (reg, head, summ, src, badge) in enumerate(featured):
    c, r = i % 4, i // 4
    x0 = M + c * (PW + GAP)
    y0 = y + r * (PH + GAP)
    d.rectangle([x0, y0, x0 + PW, y0 + PH], fill=PANEL)
    d.rectangle([x0, y0, x0 + PW, y0 + 3], fill=ACCENT)
    ix, iw = x0 + 8, PW - 16
    yy = y0 + 8
    d.text((ix, yy), f"{i + 1} · {reg}", font=f_k, fill=ACCENT)
    yy += 16
    yy = block(ix, yy, head, f_h, iw, 21, INK, max_lines=2, tag=f"panel {i + 1} head")
    yy += 3
    yy = block(ix, yy, summ, f_s, iw, 15, SOFT, max_lines=3, tag=f"panel {i + 1} summary")
    foot_y = y0 + PH - 20
    check_bottom(yy, foot_y + 2, f"panel {i + 1}")
    source_line(ix, foot_y, src, badge, iw, size=12, tag=f"panel {i + 1}")
y += 2 * PH + GAP + 10

# ======================= 5. MAP + TIMELINE + DATE CHECK =======================
band_top = y
BH = 172
MAPW = 372
TLW = 300
DCW = W - 2 * M - MAPW - TLW - 2 * 14
mx0, tx0 = M, M + MAPW + 14
dx0 = tx0 + TLW + 14

# --- world map: coarse dot grid from rough continent polygons (lon, lat) ---
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-95, 72), (-80, 64), (-60, 55), (-66, 45), (-81, 31), (-80, 25),
     (-97, 26), (-97, 18), (-87, 21), (-83, 9), (-78, 8), (-105, 22), (-117, 32), (-125, 42),
     (-124, 49), (-140, 60), (-165, 60)],
    # Greenland
    [(-55, 60), (-42, 60), (-20, 70), (-22, 81), (-60, 82), (-70, 76)],
    # South America
    [(-78, 8), (-60, 10), (-50, 0), (-35, -6), (-40, -22), (-58, -38), (-68, -55), (-75, -50),
     (-72, -30), (-80, -6)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (2, 51), (8, 54), (5, 58), (12, 66), (25, 71),
     (40, 68), (45, 55), (40, 45), (28, 41), (20, 40), (12, 44), (10, 38), (0, 39)],
    # Britain
    [(-6, 50), (2, 51), (0, 55), (-3, 59), (-6, 57)],
    # Africa
    [(-17, 21), (-10, 32), (10, 37), (32, 31), (34, 28), (43, 12), (51, 12), (40, -4), (40, -16),
     (32, -28), (20, -35), (13, -18), (9, 0), (-8, 4), (-17, 14)],
    # Asia (incl. Middle East, India, SE Asia mainland)
    [(28, 41), (36, 36), (34, 28), (43, 12), (57, 22), (60, 25), (68, 24), (73, 16), (78, 8),
     (82, 16), (90, 22), (95, 16), (99, 7), (104, 1), (109, 12), (108, 21), (121, 30), (122, 40),
     (128, 35), (130, 43), (142, 47), (142, 60), (162, 62), (180, 66), (180, 70), (140, 73),
     (110, 77), (70, 73), (60, 68), (45, 68), (40, 45)],
    # Japan
    [(130, 31), (136, 34), (141, 36), (142, 43), (145, 44), (140, 41), (135, 36), (130, 34)],
    # Indonesia / Borneo (coarse)
    [(95, 5), (106, -6), (115, -8), (120, -9), (118, 0), (117, 7), (109, 2), (104, 0)],
    # Australia
    [(114, -22), (122, -18), (131, -12), (137, -12), (142, -11), (146, -19), (153, -26),
     (150, -37), (140, -38), (131, -31), (115, -34)],
]
LAT_TOP, LAT_BOT = 78, -50
map_title_h = 18
map_cap_h = 16
my0 = band_top + map_title_h
mh = BH - map_title_h - map_cap_h
d.text((mx0, band_top), "WHERE THE DAY HAPPENED", font=font(SCB, 13), fill=ACCENT)


def proj(lon, lat):
    px = mx0 + (lon + 170) / 360 * MAPW
    py = my0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh
    return px, py


def inside(pt, poly):
    x, yv = pt
    res = False
    n = len(poly)
    for k in range(n):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % n]
        if (y1 > yv) != (y2 > yv):
            xi = x1 + (yv - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                res = not res
    return res


STEP = 5
for lat in range(LAT_TOP - 2, LAT_BOT, -STEP):
    for lon in range(-170, 190, STEP):
        ln = lon if lon <= 180 else lon - 360
        if any(inside((ln, lat), p) for p in CONTINENTS):
            px, py = proj(lon, lat)
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=LAND)

PINS = [
    ("L", 30.7, 36.9), (1, 37.6, 55.7), (2, -122, 37.4), (3, 31, 49), (4, 106.1, -6.2),
    (5, 127, 37.5), (6, 90.4, 23.8), (7, -1.5, 52.5), (8, -74, 40.7), (11, 39.5, 13.5),
    (12, 44.9, 13.0), (13, 56.3, 26.5), (17, 23.5, -4), (20, -93, 42), (26, 96, 20),
    (29, 139.7, 35.7), (31, 121.5, 24), (34, 98.5, 41), (24, 10.5, 56.5), (32, -100, 32),
]
f_pin = font(SCB, 9)
for lab, lon, lat in PINS:
    px, py = proj(lon, lat)
    r = 6
    fill = INK if lab == "L" else ACCENT
    d.ellipse([px - r, py - r, px + r, py + r], fill=fill, outline=PAPER, width=1)
    d.text((px, py), str(lab), font=f_pin, fill=WHITE, anchor="mm")
cap = "34 stories · 20+ countries  ·  L = lead, numbers = stories"
d.text((mx0, band_top + BH - map_cap_h + 2), cap, font=font(SC, 12), fill=SOFT)
if tw(cap, font(SC, 12)) > MAPW:
    warnings.append("map caption too wide")

# --- timeline ---
d.rectangle([tx0, band_top, tx0 + TLW, band_top + BH], fill=PANEL)
d.text((tx0 + 10, band_top + 8), "THE DAY IN UTC — AS REPORTED", font=font(SCB, 13), fill=ACCENT)
TL = [
    ("00:23", "Gold steadies at $3,645"),
    ("00:35", "Tokyo factory PMI 53.7"),
    ("03:11", "Moscow claims Sumy strikes"),
    ("07:55", "Falcon 9 window opens (PT)"),
    ("All day", "COP31 fallout in Antalya"),
]
f_tt = font(CB, 17)
f_tl = font(SC, 15)
ty = band_top + 34
line_x = tx0 + 82
d.line([line_x, ty + 6, line_x, ty + 4 * 26 + 8], fill=RULE, width=2)
for t, s in TL:
    d.text((line_x - 10 - tw(t, f_tt), ty - 1), t, font=f_tt, fill=INK)
    d.ellipse([line_x - 4, ty + 7, line_x + 4, ty + 15], fill=ACCENT)
    d.text((line_x + 12, ty), s, font=f_tl, fill=INK)
    if line_x + 12 + tw(s, f_tl) > tx0 + TLW - 6:
        warnings.append(f"timeline row too wide: {s!r}")
    ty += 26
check_bottom(ty, band_top + BH, "timeline")

# --- date check ---
d.rectangle([dx0, band_top, dx0 + DCW, band_top + BH], outline=ACCENT, width=2)
d.text((dx0 + 10, band_top + 8), "DATE CHECK", font=font(SCB, 13), fill=ACCENT)
dc = ("Every story here happened or was first reported on Tuesday 24 Nov 2026 in some time "
      "zone. Left out as earlier days' news: the sinking of the Russian corvette Merkury off "
      "Benghazi (night of 22 Nov), drone strikes on Khartoum (23 Nov), Gaza strikes of 21–23 Nov.")
yy = block(dx0 + 10, band_top + 28, dc, font(SC, 12), DCW - 20, 15, INK, tag="date check")
check_bottom(yy, band_top + BH - 4, "date check")
y = band_top + BH + 10

# ======================= 6. MORE OF THE DAY =======================
d.line([M, y, W - M, y], fill=INK, width=2)
d.text((M, y + 4), "MORE OF THE DAY", font=font(SCB, 14), fill=ACCENT)
y += 24
more = [
    (9, "UKRAINE", "20 Ukrainian drones downed over Moscow"),
    (10, "TÜRKİYE", "Assets of 108 frozen in fund scandal"),
    (11, "ETHIOPIA", "Amnesty alleges war crimes in Tigray"),
    (12, "YEMEN", "Saudi strikes kill or injure 25+ in Lahj"),
    (13, "HORMUZ", "Iran: three tankers hit by sea mines"),
    (14, "ESTONIA", "Moscow accuses Estonia of near-war acts"),
    (15, "NORTH KOREA", "Pyongyang threatens Swiss office closure"),
    (16, "FOOD AID", "Wars put food aid for 7.3m at risk — UN"),
    (17, "CONGO", "Congo halts cobalt exports again"),
    (18, "CYBER", "CrowdStrike buys Zscaler for $44bn"),
    (19, "FBI", "Deputy FBI director Raia to retire"),
    (20, "IOWA", "Trump halts Iowa plant detonation"),
    (21, "US CONGRESS", "Ethics panel: evidence against Gomez"),
    (22, "HONDA", "Honda recalls 810,592 vehicles in US"),
    (23, "GERMANY", "Bomb threats hit hundreds of schools"),
    (24, "DENMARK", "Denmark to ban phones in schools"),
    (25, "EU AIR", "Dirty air linked to 222,000 early deaths"),
    (26, "MYANMAR", "Myanmar pressed after ICJ genocide ruling"),
    (27, "GAZA", "Injured Gaza children reach UK care"),
    (28, "WEST BANK", "Settlers set cars alight in West Bank"),
    (29, "JAPAN", "Japan factory output grows: PMI 53.7"),
    (30, "JAPAN", "Chubu Electric faked quake risk data"),
    (31, "TAIWAN", "Taiwan votes Saturday; Beijing watches"),
    (32, "FOOTBALL", "US to host 2031 Women's World Cup"),
    (33, "SPACE", "SpaceX set to fly classified USSF-266"),
    (34, "SPACE", "Shenzhou 24 launch day at Jiuquan"),
]
COLS = 3
CGAP = 10
CW = (W - 2 * M - (COLS - 1) * CGAP) / COLS
per_col = (len(more) + COLS - 1) // COLS
LH = 18
f_mr = font(FD + "NotoSans-CondensedBold.ttf", 11)
# headline font: semi-condensed 14 first, condensed fallbacks for the longest lines
# all in the same (medium) weight so the list reads as one system
HEAD_FONTS = [font(FD + "NotoSans-SemiCondensedMedium.ttf", 14),
              font(FD + "NotoSans-CondensedMedium.ttf", 14),
              font(FD + "NotoSans-CondensedMedium.ttf", 13)]
for i, (n, reg, head) in enumerate(more):
    c, r = i // per_col, i % per_col
    x = M + c * (CW + CGAP)
    yy = y + r * LH
    pre = f"{n} · {reg} — "
    d.text((x, yy + 3), pre, font=f_mr, fill=ACCENT)
    hx = x + tw(pre, f_mr)
    for k, f_mh in enumerate(HEAD_FONTS):
        if hx + tw(head, f_mh) - x <= CW:
            break
    else:
        warnings.append(f"more {n}: overflows column by {hx + tw(head, f_mh) - x - CW:.0f}px")
    if k:
        print(f"note: more {n} uses fallback font #{k}")
    d.text((hx, yy), head, font=f_mh, fill=INK)
for c in range(1, COLS):
    lx = M + c * (CW + CGAP) - CGAP / 2
    d.line([lx, y, lx, y + per_col * LH - 2], fill=RULE, width=1)
y += per_col * LH + 6

# ======================= 7. FOOTER =======================
d.line([M, y, W - M, y], fill=INK, width=1)
foot = ("Sources: Reuters · The Japan Times · Qatar Tribune · Times of India · Izvestia · "
        "Space Calendar — Badges: CONFIRMED = several sources · OFFICIAL = primary source · "
        "REPORTED = single source, as attributed.")
yy = block(M, y + 4, foot, font(SC, 12), W - 2 * M, 15, SOFT, max_lines=2, tag="footer")
check_bottom(yy, H - 6, "page")

img.save("entry.png", optimize=True)
for w in warnings:
    print("WARNING:", w)
print(f"saved entry.png, bottom y={yy:.0f}, warnings={len(warnings)}")
