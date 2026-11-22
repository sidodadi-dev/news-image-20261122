#!/usr/bin/env python3
"""Build the front-page poster for 22 November 2026 world news.

Draws entry.png (1024x1024) with Pillow. All art is drawn in code;
all text is wrapped to fit its box.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
NAVY = (18, 38, 66)
NAVY2 = (30, 58, 96)
RED = (178, 34, 34)
RED2 = (200, 52, 44)
INK = (28, 32, 40)
GREY = (96, 96, 92)
LIGHT = (233, 226, 210)
CARD = (255, 252, 244)
WHITE = (255, 255, 255)
SEA = (46, 92, 128)
SAND = (214, 196, 152)
GOLD = (212, 160, 60)

F = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    try:
        return ImageFont.truetype(F + name, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real pixel widths."""
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def letterspaced(draw, text, fnt, x, y, fill, tracking=4):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + tracking
    return cx


# ---------------------------------------------------------------- icons
def icon_explosion(d, x, y, s, col):
    pts = []
    import math
    for i in range(16):
        r = s if i % 2 == 0 else s * 0.45
        a = math.pi * i / 8 - math.pi / 2
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    d.polygon(pts, fill=col)
    d.ellipse([x - s * 0.28, y - s * 0.28, x + s * 0.28, y + s * 0.28],
              fill=GOLD)


def icon_quake(d, x, y, s, col):
    d.line([(x - s, y - s * 0.55), (x - s * 0.55, y + s * 0.2),
            (x - s * 0.15, y - s * 0.4), (x + s * 0.25, y + s * 0.45),
            (x + s * 0.6, y - s * 0.15), (x + s, y + s * 0.3)],
           fill=col, width=4)
    d.line([(x - s, y + s * 0.8), (x + s, y + s * 0.8)], fill=col, width=3)


def icon_trade(d, x, y, s, col):
    d.arc([x - s, y - s * 0.7, x, y + s * 0.7], 90, 270, fill=col, width=4)
    d.arc([x, y - s * 0.7, x + s, y + s * 0.7], 270, 90, fill=col, width=4)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=GOLD)
    # arrowheads: left arc ends pointing down, right arc ends pointing up
    d.polygon([(x - s, y + s * 0.7), (x - s - 9, y + s * 0.45),
               (x - s + 2, y + s * 0.45)], fill=col)
    d.polygon([(x + s, y - s * 0.7), (x + s + 9, y - s * 0.45),
               (x + s - 2, y - s * 0.45)], fill=col)


def icon_globe(d, x, y, s, col):
    d.ellipse([x - s, y - s, x + s, y + s], outline=col, width=4)
    d.ellipse([x - s * 0.45, y - s, x + s * 0.45, y + s], outline=col, width=3)
    d.line([(x - s, y), (x + s, y)], fill=col, width=3)
    d.arc([x - s, y - s * 0.45, x + s, y + s * 0.45], 180, 360,
          fill=col, width=3)


def icon_aid(d, x, y, s, col):
    d.rectangle([x - s * 0.8, y - s * 0.35, x + s * 0.8, y + s * 0.8],
                outline=col, width=4)
    d.line([(x - s * 0.8, y - s * 0.35), (x, y - s * 0.95),
            (x + s * 0.8, y - s * 0.35)], fill=col, width=4)
    d.rectangle([x - s * 0.12, y - s * 0.15, x + s * 0.12, y + s * 0.6],
                fill=RED2)
    d.rectangle([x - s * 0.45, y + s * 0.12, x + s * 0.45, y + s * 0.36],
                fill=RED2)


def icon_parliament(d, x, y, s, col):
    d.polygon([(x - s, y - s * 0.35), (x, y - s * 0.95),
               (x + s, y - s * 0.35)], fill=col)
    for i, cx in enumerate((x - s * 0.62, x - s * 0.21, x + s * 0.21,
                            x + s * 0.62)):
        d.rectangle([cx - 4, y - s * 0.3, cx + 4, y + s * 0.55], fill=col)
    d.rectangle([x - s * 0.95, y + s * 0.55, x + s * 0.95, y + s * 0.75],
                fill=col)


ICONS = [icon_explosion, icon_quake, icon_trade,
         icon_globe, icon_aid, icon_parliament]

PANELS = [
    ("LVIV, UKRAINE",
     "Massive overnight barrage hits Lviv",
     "At least 2 killed and 10 hurt as ~400 drones and 110 missiles rain down; debris also falls in Poland."),
    ("PERU",
     "Magnitude 6.9 quake shakes the Andes",
     "Strong tremor rattles Peru's highlands; no damage or casualties reported so far."),
    ("EU – INDONESIA",
     "Trade deal signed after a decade",
     "The pact scraps 98.5% of tariffs, opening markets on both sides after ten years of talks."),
    ("COP31",
     "Climate talks stall and overrun",
     "Negotiations in Turkiye drag past schedule, split over fossil fuels and finance."),
    ("GAZA",
     "Four nations press Israel on aid",
     "Australia, Canada, Italy and the UK jointly urge Israel to open access as floods hit Gaza."),
    ("ISRAEL",
     "Herzog taps Eisenkot to form government",
     "The president picks ex-military chief Gadi Eisenkot, passing over Netanyahu."),
]

TICKER = ("Cartel boss 'El Chapo Isidro' arrested in Mexico; 11 killed in "
          "Sinaloa  \u00b7  Hong Kong election voting begins  \u00b7  "
          "Magnitude 4.1 quake in Myanmar  \u00b7  Drone hits Russian cargo "
          "ship in the Baltic; Finland on alert")


def lead_art(d, x, y, w, h):
    """Gulf coastline scene: sky, sea, shore, radar, missile arcs."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 196))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    d.line([(x, y + h * 0.62), (x + w, y + h * 0.62)], fill=NAVY2, width=3)
    for i, yy in enumerate((0.70, 0.79, 0.88)):
        d.line([(x + 14, y + h * yy), (x + 70 + i * 30, y + h * yy)],
               fill=(120, 165, 200), width=3)
        d.line([(x + w - 90 - i * 20, y + h * yy),
                (x + w - 20, y + h * yy)], fill=(120, 165, 200), width=3)
    # coastline
    d.polygon([(x, y + h * 0.62), (x + w * 0.45, y + h * 0.42),
               (x + w * 0.62, y + h * 0.52), (x + w, y + h * 0.30),
               (x + w, y), (x, y)], fill=SAND)
    d.line([(x, y + h * 0.62), (x + w * 0.45, y + h * 0.42),
            (x + w * 0.62, y + h * 0.52), (x + w, y + h * 0.30)],
           fill=NAVY, width=3)
    # sun (drawn after the land so it stays visible)
    d.ellipse([x + w - 95, y + 18, x + w - 25, y + 88], fill=GOLD)
    # radar dish on the shore: half-disc bowl + mast + base
    bx, by = x + w * 0.30, y + h * 0.50
    d.pieslice([bx - 24, by - 36, bx + 24, by + 4], 180, 360, fill=NAVY)
    d.line([(bx, by - 2), (bx, by + 28)], fill=NAVY, width=5)
    d.line([(bx - 16, by + 28), (bx + 16, by + 28)], fill=NAVY, width=5)
    # missile arcs (red, dashed by segments)
    import math
    for (sx, sy, ex, ey, peak) in (
            (0.08, 0.16, 0.55, 0.55, 0.02),
            (0.30, 0.10, 0.78, 0.42, -0.06),
            (0.55, 0.06, 0.95, 0.50, -0.10)):
        pts = []
        for t in range(21):
            tt = t / 20
            px = x + w * (sx + (ex - sx) * tt)
            py = y + h * (sy + (ey - sy) * tt - peak * 4 * tt * (1 - tt))
            pts.append((px, py))
        d.line(pts, fill=RED2, width=4)
        d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5,
                   pts[-1][0] + 5, pts[-1][1] + 5], fill=RED2)
    # small ships near the strait
    for sx in (0.62, 0.80):
        hx, hy = x + w * sx, y + h * 0.80
        d.polygon([(hx - 26, hy), (hx + 26, hy), (hx + 18, hy + 10),
                   (hx - 18, hy + 10)], fill=NAVY)
        d.rectangle([hx - 8, hy - 12, hx + 6, hy], fill=NAVY)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 36
    # ---- masthead
    y = 30
    letterspaced(d, "THE WORLD IN ONE DAY", SANS_B(26), mx + 4, y, RED, 5)
    y += 40
    d.text((mx, y), "SUNDAY 22 NOVEMBER 2026", font=SERIF_B(52), fill=NAVY)
    y += 66
    d.line([(mx, y), (W - mx, y)], fill=NAVY, width=3)
    y += 10
    d.text((mx, y), "The day's biggest stories, in a single picture",
           font=SERIF_I(20), fill=GREY)
    y += 34
    d.line([(mx, y), (W - mx, y)], fill=NAVY, width=1)
    # ---- lead block
    lead_y = y + 14
    lead_h = 268
    art_w = 400
    lead_art(d, mx, lead_y, art_w, lead_h)
    d.rectangle([mx, lead_y, mx + art_w, lead_y + lead_h],
                outline=NAVY, width=2)
    tx = mx + art_w + 24
    tw = W - mx - tx
    ty = lead_y + 4
    d.text((tx, ty), "TOP STORY  \u00b7  THE GULF", font=SANS_B(17), fill=RED)
    ty += 30
    title = "IRAN STRIKES AT US BASES ACROSS THE GULF"
    lines = wrap(d, title, SANS_B(33), tw)
    ty = draw_lines(d, lines, tx, ty, SANS_B(33), NAVY, 40)
    ty += 8
    stand = ("Iran says its missiles and drones hit US positions in Bahrain "
             "in retaliation for a drone incursion; Bahrain says its defences "
             "intercepted the attack and blames Iran for a fire at a civilian "
             "industrial site. No US casualties confirmed.")
    slines = wrap(d, stand, SANS(18), tw)
    draw_lines(d, slines, tx, ty, SANS(18), INK, 24)
    # ---- panels grid
    grid_y = lead_y + lead_h + 18
    gap = 14
    cw = (W - 2 * mx - 2 * gap) // 3
    ch = 196
    for i, (loc, title, body) in enumerate(PANELS):
        r, c = divmod(i, 3)
        x = mx + c * (cw + gap)
        yy = grid_y + r * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CARD, outline=NAVY,
                    width=1)
        d.rectangle([x, yy, x + cw, yy + 5], fill=RED)
        ix, iy = x + 34, yy + 42
        ICONS[i](d, ix, iy, 24, NAVY2)
        lx = x + 70
        d.text((lx, yy + 18), loc, font=SANS_B(15), fill=RED)
        tlines = wrap(d, title, SANS_B(19), cw - 24)
        draw_lines(d, tlines[:2], x + 14, yy + 62, SANS_B(19), NAVY, 24)
        blines = wrap(d, body, SANS(15), cw - 28)
        draw_lines(d, blines[:3], x + 14, yy + 62 + 24 * len(tlines[:2]) + 6,
                   SANS(15), INK, 20)
    # ---- footer ticker
    fy = grid_y + 2 * ch + gap + 16
    fh = H - fy - 26
    d.rectangle([mx, fy, W - mx, fy + fh], fill=NAVY)
    d.text((mx + 16, fy + (fh - 20) // 2 - 2), "ALSO TODAY",
           font=SANS_B(18), fill=GOLD)
    tlines = wrap(d, TICKER, SANS(15), W - mx - (mx + 16 + 150))
    n = min(len(tlines), 3)
    draw_lines(d, tlines[:n], mx + 16 + 150, fy + (fh - n * 19) // 2,
               SANS(15), WHITE, 19)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
