"""Draw a one-page newspaper front for Tuesday 24 November 2026 (flat shapes + type)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 240, 226)
INK = (28, 26, 24)
SOFT = (88, 82, 74)
ACCENT = (178, 34, 34)
FONT_DIR = "/usr/share/fonts/truetype/noto/"
BOLD = FONT_DIR + "NotoSans-Bold.ttf"
REG = FONT_DIR + "NotoSans-Regular.ttf"
SERIF_BLACK = FONT_DIR + "NotoSerif-Black.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 28  # outer margin
warnings = []


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(s, f):
    return d.textlength(s, font=f)


def wrap(s, f, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, f) <= width:
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
        if text_w(ln, f) > width:
            warnings.append(f"{tag}: line too wide: {ln!r}")
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


# ---------- Masthead ----------
y = 22
f_small = font(BOLD, 22)
label = "THE WORLD IN ONE PICTURE"
d.text(((W - text_w(label, f_small)) / 2, y), label, font=f_small, fill=ACCENT)
y += 34
date = "TUESDAY 24 NOVEMBER 2026"
size = 84
while text_w(date, font(SERIF_BLACK, size)) > W - 2 * 16:  # date may use a slimmer margin
    size -= 1
f_date = font(SERIF_BLACK, size)
d.text(((W - text_w(date, f_date)) / 2, y), date, font=f_date, fill=INK)
y += int(size * 1.25)
d.rectangle([M, y, W - M, y + 5], fill=INK)
d.rectangle([M, y + 9, W - M, y + 10], fill=INK)
y += 24

# ---------- Lead story ----------
lead_top = y
f_kick = font(BOLD, 24)
d.text((M, y), "LEAD · NATO / RUSSIA / SPACE", font=f_kick, fill=ACCENT)
y += 34
f_lead = font(BOLD, 58)
y = block(M, y, "NATO VOWS SPACE DEFENCE", f_lead, W - 2 * M, 68, INK, 1, "lead")
motif_w = 210
f_label = font(REG, 25)
y = block(M, y + 6, "Reports say Russia's nuclear-armed 'Sputnik-S' satellite could launch "
          "within weeks — Rutte vows to defend every inch, including space",
          f_label, W - 2 * M - motif_w, 33, SOFT, 3, "lead label")

# satellite + globe motif (right of the label)
cx, cy = W - M - 95, lead_top + 138  # keep orbit clear of the headline
d.ellipse([cx - 62, cy - 30, cx + 62, cy + 94], fill=(222, 214, 196), outline=INK, width=3)
d.arc([cx - 62, cy - 2, cx + 62, cy + 66], 0, 180, fill=INK, width=2)
d.line([cx, cy - 30, cx, cy + 94], fill=INK, width=2)
d.arc([cx - 30, cy - 30, cx + 30, cy + 94], 90, 270, fill=INK, width=2)
d.arc([cx - 30, cy - 30, cx + 30, cy + 94], 270, 90, fill=INK, width=2)
# dashed orbit ring around the globe, satellite riding on it
for a in range(200, 340, 12):
    d.arc([cx - 92, cy - 52, cx + 92, cy + 40], a, a + 6, fill=ACCENT, width=3)
sx, sy = cx + 40, cy - 48
d.rectangle([sx - 12, sy - 12, sx + 12, sy + 12], fill=INK)
d.rectangle([sx - 52, sy - 8, sx - 16, sy + 8], fill=ACCENT)
d.rectangle([sx + 16, sy - 8, sx + 52, sy + 8], fill=ACCENT)

y = max(y, cy + 94) + 14
d.rectangle([M, y, W - M, y + 3], fill=INK)
y += 16

# ---------- Six-panel grid ----------
panels = [
    ("UKRAINE", "Drone strike leaves several missing near Kyiv",
     "Russian strike damages homes in the Kyiv region; rescuers search for the missing"),
    ("INDONESIA", "Rescuers search factory ruins for 30 missing",
     "24 confirmed dead in the Banten candy factory fire near Jakarta"),
    ("TURKIYE", "Assets of 108 frozen in fund scandal",
     "Prosecutors freeze assets of 108 people in the investment fund crisis"),
    ("ETHIOPIA", "Amnesty alleges war crimes in Tigray",
     "Report says army shelling killed 14 civilians; Amnesty urges a U.N. probe"),
    ("BRITAIN", "No EU return without a referendum",
     "PM Burnham calls rejoining the EU without a vote 'unthinkable'"),
    ("CHESS", "Youngest world title match opens in Geneva",
     "Game 1 today: Gukesh, 20, defends his crown against Sindarov, 20"),
]
cols, rows = 2, 3
gap = 24
grid_top, grid_bot = y, H - M
cw = (W - 2 * M - gap * (cols - 1)) / cols
ch = (grid_bot - grid_top) / rows
f_pk = font(BOLD, 24)
f_ph = font(BOLD, 36)
f_pl = font(REG, 24)
for i, (kick, head, lab) in enumerate(panels):
    c, r = i % cols, i // cols
    x0 = M + c * (cw + gap)
    y0 = grid_top + r * ch
    if r > 0:
        d.line([x0, y0 - 6, x0 + cw, y0 - 6], fill=SOFT, width=1)
    d.rectangle([x0, y0 + 4, x0 + 8, y0 + 26], fill=ACCENT)
    d.text((x0 + 16, y0), kick, font=f_pk, fill=ACCENT)
    yy = block(x0, y0 + 32, head, f_ph, cw, 42, INK, 2, kick + " head")
    yy = block(x0, yy + 4, lab, f_pl, cw, 30, SOFT, 2, kick + " label")
    if yy > y0 + ch - 8:
        warnings.append(f"{kick}: panel overflow by {yy - (y0 + ch - 8):.0f}px")
if cols == 2:
    xm = M + cw + gap / 2
    d.line([xm, grid_top, xm, grid_bot], fill=SOFT, width=1)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, "date size", size)
for w in warnings:
    print("WARN", w)
