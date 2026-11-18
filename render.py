"""Render entry.png: a one-page front page summing up Tuesday 17 November 2026.

Build-time tool (Pillow). The submitted program, main.py, only copies the
rendered PNG; stdlib-only applies to that program, not to this renderer.
"""

import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 40

PAPER = (244, 239, 227)
INK = (22, 19, 15)
RED = (192, 57, 43)
SLATE = (46, 64, 87)
GOLD = (201, 162, 39)
MUTED = (108, 100, 88)

LIB = "/usr/share/fonts/truetype/liberation/"
DJV = "/usr/share/fonts/truetype/dejavu/"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def sans(size):
    return font(LIB + "LiberationSans-Bold.ttf", size)


def sans_r(size):
    return font(LIB + "LiberationSans-Regular.ttf", size)


def serif(size):
    return font(LIB + "LiberationSerif-Bold.ttf", size)


def serif_r(size):
    return font(LIB + "LiberationSerif-Regular.ttf", size)


def mono(size):
    return font(DJV + "DejaVuSansMono-Bold.ttf", size)


def mono_r(size):
    return font(DJV + "DejaVuSansMono.ttf", size)


def tw(d, text, f, tracking=0):
    if not text:
        return 0
    b = d.textbbox((0, 0), text, font=f)
    return b[2] - b[0] + tracking * max(0, len(text) - 1)


def tracked(d, xy, text, f, fill, tracking=0, anchor="left"):
    total = tw(d, text, f, tracking)
    x, y = xy
    if anchor == "center":
        x -= total / 2
    elif anchor == "right":
        x -= total
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += d.textlength(ch, font=f) + tracking


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if tw(d, test, f) <= maxw or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, f, maxw, maxlines):
    lines = wrap(d, text, f, maxw)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        last = lines[-1]
        while tw(d, last + "…", f) > maxw and len(last) > 3:
            last = last[:-1]
        lines[-1] = last.rstrip(" ,.;") + "…"
    return lines


def block(d, x, y, lines, f, fill, lh, tracking=0):
    for ln in lines:
        tracked(d, (x, y), ln, f, fill, tracking)
        y += lh
    return y


def rule(d, x0, y, x1, color=INK, w=2):
    d.rectangle([x0, y, x1, y + w - 1], fill=color)


# ---------------------------------------------------------------- world map

def load_land(path):
    with open(path) as fh:
        geo = json.load(fh)
    polys = []
    for feat in geo["features"]:
        g = feat["geometry"]
        if not g:
            continue
        if g["type"] == "Polygon":
            polys.append(g["coordinates"])
        elif g["type"] == "MultiPolygon":
            polys.extend(g["coordinates"])
    return polys


def draw_map(img, d, box, polys, markers):
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0, y1 - y0
    lon0, lon1 = -180.0, 180.0
    lat0, lat1 = -62.0, 68.0

    def px(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * mw,
                y0 + (lat1 - lat) / (lat1 - lat0) * mh)

    d.rectangle([x0, y0, x1, y1], fill=(238, 233, 221))
    for lon in range(-150, 181, 30):
        gx = px(lon, 0)[0]
        d.line([gx, y0 + 1, gx, y1 - 1], fill=(226, 220, 207), width=1)
    for lat in range(-60, 61, 30):
        gy = px(0, lat)[1]
        d.line([x0 + 1, gy, x1 - 1, gy], fill=(226, 220, 207), width=1)

    land = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    ld = ImageDraw.Draw(land)
    for poly in polys:
        for ring in poly:
            pts, last = [], None
            for lon, lat in ring:
                p = px(lon, lat)
                q = (round(p[0] - x0, 2), round(p[1] - y0, 2))
                if q != last:
                    pts.append(q)
                    last = q
            if len(pts) >= 3:
                ld.polygon(pts, fill=SLATE + (58,))
    img.alpha_composite(land, (x0, y0))
    d.rectangle([x0, y0, x1, y1], outline=(84, 94, 108), width=1)

    f = sans(13)
    for m in markers:
        mx, my = px(m["lon"], m["lat"])
        fw = tw(d, m["label"], f)
        lx = mx + m.get("tx", 0)
        if m.get("align") == "right":
            lx -= fw
        ly = max(y0 + 4, min(y1 - 22, my + m.get("ty", 0)))
        d.line([mx, my, mx + m.get("tx", 0) * 0.45, ly + 9], fill=INK, width=1)
        d.rectangle([lx - 4, ly, lx + fw + 4, ly + 19], fill=PAPER, outline=(202, 194, 180))
        d.text((lx, ly + 15), m["label"], font=f, fill=INK)
        d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=RED, outline=PAPER, width=2)

    f = mono(12)
    label = "17 NOV 2026"
    lw = tw(d, label, f)
    d.rectangle([x1 - lw - 20, y1 - 26, x1 - 8, y1 - 7], fill=RED)
    d.text((x1 - lw - 14, y1 - 23), label, font=f, fill=PAPER)


# ---------------------------------------------------------------- icons

def drone(d, cx, cy, s=1.0):
    """Top-view quadcopter: body, four arms, four rotors."""
    d.rounded_rectangle([cx - 2.2 * s, cy - 3.0 * s, cx + 2.2 * s, cy + 3.0 * s],
                        radius=1.6 * s, fill=INK)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ex, ey = cx + dx * 9 * s, cy + dy * 5.2 * s
        d.line([cx, cy, ex, ey], fill=INK, width=max(1, int(1.6 * s)))
        d.line([ex - 3.2 * s, ey, ex + 3.2 * s, ey], fill=INK, width=max(1, int(2.2 * s)))
    d.ellipse([cx - 1.2 * s, cy - 1.2 * s, cx + 1.2 * s, cy + 1.2 * s], fill=RED)


def icon_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 233, 221))
    sea_y = y + h - int(h * 0.24)
    d.rectangle([x, sea_y, x + w, y + h], fill=(212, 217, 214))
    for i in range(5):
        wy = sea_y + 9 + i * 8
        d.line([x + 20 + (i * 37) % 110, wy, x + 58 + (i * 37) % 110, wy], fill=(172, 183, 187), width=2)

    deck = y + int(h * 0.58)
    gap0, gap1 = x + int(w * 0.42), x + int(w * 0.60)
    cx = (gap0 + gap1) / 2

    # smoke first, so the broken deck cuts in front of it
    for ox, rw, rh in ((-20, 34, 44), (-4, 48, 70), (22, 28, 34)):
        d.ellipse([cx + ox - rw / 2, deck - rh, cx + ox + rw / 2, deck + 6], fill=(186, 184, 175))
        d.ellipse([cx + ox - rw / 2 + 7, deck - rh + 8, cx + ox + rw / 2 - 2, deck], fill=(213, 210, 200))

    # deck, split at the gap
    d.rectangle([x + 4, deck, gap0, deck + 8], fill=INK)
    d.rectangle([gap1, deck, x + w - 4, deck + 8], fill=INK)
    # torn ends
    d.polygon([(gap0, deck + 8), (gap0 - 12, deck - 13), (gap0 - 4, deck + 8)], fill=INK)
    d.polygon([(gap1, deck + 8), (gap1 + 12, deck - 13), (gap1 + 4, deck + 8)], fill=INK)
    # hanging rebar
    for rx, sgn in ((gap0, -1), (gap1, 1)):
        for k in (0, 7):
            d.line([rx + sgn * 3, deck + 8, rx + sgn * 8 + k, deck + 26], fill=(74, 84, 98), width=2)

    for pxc in (x + int(w * 0.16), x + int(w * 0.84)):
        top = deck - int(h * 0.42)
        d.rectangle([pxc - 5, top, pxc + 5, deck + 8], fill=INK)
        d.rectangle([pxc - 18, top + 9, pxc + 18, top + 13], fill=INK)
        for side in (-1, 1):
            for k in (1, 2, 3):
                tx = pxc + side * k * 22
                if x + 6 < tx < x + w - 6:
                    d.line([pxc, top + 13, tx, deck + 4], fill=INK, width=1)

    for pxc in (x + int(w * 0.16), x + int(w * 0.84), gap0, gap1):
        d.line([pxc, deck + 8, pxc, sea_y + 22], fill=(74, 84, 98), width=3)

    # impact star on the gap
    pts = []
    for i in range(16):
        ang = math.pi * 2 * i / 16
        r = 25 if i % 2 == 0 else 9
        pts.append((cx + r * math.cos(ang), deck - 6 + r * math.sin(ang)))
    d.polygon(pts, fill=RED)
    d.ellipse([cx - 6, deck - 12, cx + 6, deck], fill=(255, 226, 190))

    # three drones above
    for dx, dy, s in ((x + 46, y + 38, 1.0), (x + 92, y + 20, 1.15), (x + 128, y + 48, 0.9)):
        drone(d, dx, dy, s)


def icon_trefoil(d, cx, cy, r):
    for i in range(3):
        a0 = -90 + i * 120
        d.pieslice([cx - r, cy - r, cx + r, cy + r], a0 + 7, a0 + 113, fill=INK)
    d.ellipse([cx - r * 0.30, cy - r * 0.30, cx + r * 0.30, cy + r * 0.30], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)


def icon_chart(d, x, y, w, h):
    d.line([x, y - 2, x, y + h], fill=INK, width=2)
    d.line([x, y + h, x + w, y + h], fill=INK, width=2)
    pts = [(x + 5, y + 8), (x + w * 0.28, y + 16), (x + w * 0.45, y + 10),
           (x + w * 0.62, y + h * 0.52), (x + w * 0.80, y + h * 0.58), (x + w - 6, y + h - 6)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex + 4, ey + 4), (ex - 12, ey + 2), (ex - 2, ey - 12)], fill=RED)


def icon_megaphone(d, x, y, w, h):
    cx, cy = x + w * 0.46, y + h * 0.46
    s = min(w, h) * 0.40
    d.polygon([(cx - s * 0.55, cy - s * 0.45), (cx + s * 0.55, cy - s), (cx + s * 0.55, cy + s),
               (cx - s * 0.55, cy + s * 0.45)], outline=INK, width=3, fill=PAPER)
    d.rectangle([cx - s * 1.05, cy - s * 0.40, cx - s * 0.55, cy + s * 0.40], fill=INK)
    d.line([cx - s * 0.85, cy + s * 0.42, cx - s * 1.05, cy + s * 1.0], fill=INK, width=4)
    for i, r in enumerate((s * 0.55, s * 0.85, s * 1.15)):
        d.arc([cx + s * 0.55 - r, cy - r, cx + s * 0.55 + r, cy + r], 300, 60,
              fill=RED if i == 0 else INK, width=3)


def icon_house(d, x, y, w, h):
    bw = w * 0.62
    bx = x + (w - bw) / 2
    by = y + h * 0.42
    d.rectangle([bx, by, bx + bw, y + h - 2], outline=INK, width=3, fill=PAPER)
    d.polygon([(bx - 7, by), (bx + bw / 2, y + 4), (bx + bw + 7, by)], outline=INK, width=3, fill=PAPER)
    fx, fy = bx + bw / 2, y + h - 3
    d.polygon([(fx - 8, fy), (fx - 4, fy - 13), (fx + 1, fy - 22), (fx + 7, fy - 12), (fx + 8, fy)], fill=RED)
    d.polygon([(fx - 3, fy), (fx + 1, fy - 10), (fx + 4, fy)], fill=GOLD)


def icon_chip(d, x, y, w, h):
    s = min(w, h) * 0.60
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], outline=INK, width=3, fill=PAPER)
    d.rectangle([cx - s * 0.20, cy - s * 0.20, cx + s * 0.20, cy + s * 0.20], fill=RED)
    for i in range(3):
        off = -s * 0.26 + i * s * 0.26
        d.line([cx - s / 2 - 7, cy + off, cx - s / 2, cy + off], fill=INK, width=3)
        d.line([cx + s / 2, cy + off, cx + s / 2 + 7, cy + off], fill=INK, width=3)
        d.line([cx + off, cy - s / 2 - 7, cx + off, cy - s / 2], fill=INK, width=3)
        d.line([cx + off, cy + s / 2, cx + off, cy + s / 2 + 7], fill=INK, width=3)


def icon_jet(d, x, y, w, h):
    cx, cy = x + w * 0.58, y + h * 0.50
    s = min(w, h) * 0.40
    d.polygon([(cx + s * 1.30, cy), (cx - s * 0.55, cy - s * 0.18),
               (cx - s * 1.05, cy), (cx - s * 0.55, cy + s * 0.18)], fill=INK)
    d.polygon([(cx + s * 0.12, cy - s * 0.05), (cx - s * 0.42, cy - s * 1.05),
               (cx - s * 0.02, cy - s * 1.05), (cx + s * 0.48, cy - s * 0.05)], fill=INK)
    d.polygon([(cx + s * 0.16, cy + s * 0.05), (cx - s * 0.06, cy + s * 0.92),
               (cx + s * 0.32, cy + s * 0.92), (cx + s * 0.52, cy + s * 0.05)], fill=INK)
    d.polygon([(cx - s * 0.80, cy - s * 0.02), (cx - s * 1.02, cy - s * 0.55),
               (cx - s * 0.78, cy - s * 0.55), (cx - s * 0.56, cy - s * 0.02)], fill=INK)
    for i in range(2):
        yy = cy - 6 + i * 12
        d.line([x + 2, yy, x + w * 0.16, yy], fill=RED if i == 0 else (150, 144, 132), width=2)


# ---------------------------------------------------------------- page

def build(polys, out):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)

    # ---------------- masthead
    tracked(d, (W / 2, 72), "THE WORLD TODAY", serif(58), INK, tracking=4, anchor="center")
    rule(d, M, 84, W - M, INK, 3)

    f_edit = mono(15)
    d.text((M, 91), "WORLD EDITION · 9 STORIES · 3 CONTINENTS", font=f_edit, fill=MUTED)
    right = "FINAL EDITION"
    d.text((W - M - tw(d, right, f_edit), 91), right, font=f_edit, fill=MUTED)

    d.rectangle([M, 116, W - M, 160], fill=RED)
    tracked(d, (W / 2, 149), "TUESDAY · 17 NOVEMBER 2026", mono(31), PAPER, tracking=1, anchor="center")

    # ---------------- lead
    lx = M
    tracked(d, (lx, 184), "BREAKING · CRIMEA", mono(20), RED, tracking=2)
    tracked(d, (lx, 228), "KERCH BRIDGE", serif(54), INK)
    tracked(d, (lx, 278), "CRIPPLED", serif(54), INK)

    f_deck = serif_r(20)
    deck = fit_lines(d, "Ukraine strikes Russia's only land link to Crimea; Moscow says it downed 1,400 drones.", f_deck, 560, 2)
    y = block(d, lx, 304, deck, f_deck, (56, 50, 42), 23)

    f_bul = sans_r(19)
    y += 12
    for b in ("Road-and-rail span closed, 'critically damaged'", "Second night of mass drone attacks"):
        d.rectangle([lx, y - 11, lx + 7, y - 4], fill=RED)
        d.text((lx + 14, y), b, font=f_bul, fill=INK, anchor="ls")
        y += 21

    ill = Image.new("RGBA", (352, 244), PAPER + (255,))
    icon_bridge(ImageDraw.Draw(ill), 0, 0, 352, 244)
    img.alpha_composite(ill, (632, 168))

    # ---------------- map + numbers
    map_box = (M, 416, 716, 660)
    markers = [
        {"lon": -77.0, "lat": 38.9, "label": "Washington — Iran claim", "tx": 10, "ty": -30},
        {"lon": 34.5, "lat": 45.2, "label": "Crimea — bridge hit", "tx": 12, "ty": -38},
        {"lon": 35.2, "lat": 31.9, "label": "West Bank — settler attack", "tx": -14, "ty": 30, "align": "right"},
        {"lon": 121.0, "lat": 14.6, "label": "Manila — protests", "tx": -18, "ty": 26, "align": "right"},
        {"lon": 139.7, "lat": 35.7, "label": "Tokyo — jets scrambled", "tx": -14, "ty": 16, "align": "right"},
    ]
    draw_map(img, d, map_box, polys, markers)

    px0 = 728
    d.rectangle([px0, 416, W - M, 660], fill=(236, 231, 220))
    d.rectangle([px0, 416, W - M, 660], outline=(84, 94, 108), width=1)
    tracked(d, (px0 + 14, 436), "THE DAY IN NUMBERS", mono(12), INK, tracking=1)
    rule(d, px0 + 14, 444, W - M - 14, INK, 1)

    figures = [("1,400", ("drones Russia says it", "downed over two nights")),
               ("800+", ("US flights cut or", "delayed in the outage")),
               ("$7.7m", ("ex-ICC prosecutor", "ordered to pay"))]
    fy = 452
    for num, lab in figures:
        d.text((px0 + 14, fy + 22), num, font=mono(24), fill=INK, anchor="ls")
        yy = fy + 36
        for ln in lab:
            d.text((px0 + 14, yy), ln, font=sans_r(12), fill=(58, 52, 44))
            yy += 13
        fy += 64

    # ---------------- two cards
    cy0, cy1 = 668, 754
    cards = [("IRAN 'DIRTY BOMB' CLAIM", "Reported plot on Washington; Tehran denies", "trefoil"),
             ("MARKETS SLIDE", "Oil, gold and stocks fall sharply", "chart")]
    for i, (head, sub, kind) in enumerate(cards):
        x0 = M + i * 482
        x1 = x0 + 462
        d.rectangle([x0, cy0, x1, cy1], fill=(250, 247, 239))
        d.rectangle([x0, cy0, x1, cy1], outline=(198, 190, 175), width=1)
        if kind == "trefoil":
            icon_trefoil(d, x0 + 44, cy0 + 43, 23)
        else:
            icon_chart(d, x0 + 18, cy0 + 24, 50, 40)
        tracked(d, (x0 + 84, cy0 + 32), head, sans(22), INK)
        f_cs = sans_r(17)
        lines = fit_lines(d, sub, f_cs, 360, 2)
        block(d, x0 + 84, cy0 + 54, lines, f_cs, (58, 52, 44), 20)

    # ---------------- 2x2 grid
    f_th, f_ts = sans(22), sans_r(17)
    items = [
        ("MANILA PROTESTS", "Hundreds arrested at anti-Trump rally", icon_megaphone),
        ("SETTLER ATTACK", "Elderly Palestinian woman killed, 10 hurt", icon_house),
        ("AI-CHIP CURBS", "US tightens exports to five nations", icon_chip),
        ("JAPAN SCRAMBLES JETS", "Suspected Russian jets enter airspace", icon_jet),
    ]
    for i, (head, sub, ic) in enumerate(items):
        row, col = divmod(i, 2)
        x0 = M + col * 482
        y0 = 762 + row * 96
        x1 = x0 + 462
        d.rectangle([x0, y0, x1, y0 + 86], fill=(250, 247, 239))
        d.line([x0, y0, x1, y0], fill=(210, 202, 186), width=1)
        d.line([x0, y0 + 86, x1, y0 + 86], fill=(210, 202, 186), width=1)
        ic(d, x0 + 8, y0 + 22, 44, 44)
        tracked(d, (x0 + 66, y0 + 34), head, f_th, INK)
        d.text((x0 + 66, y0 + 56), sub, font=f_ts, fill=(58, 52, 44))

    # ---------------- footer
    rule(d, M, 952, W - M, INK, 2)
    f_num = mono(15)
    tracked(d, (M, 972), "1,400 DOWNED · 800+ FLIGHTS · 9 STORIES · 3 CONTINENTS", f_num, INK)
    tracked(d, (W - M, 972), "17 NOV 2026", f_num, RED, tracking=1, anchor="right")
    d.text((M, 990), "ALSO REPORTED · NSA classified network offline in maintenance · Jordan blocks Telegram",
           font=sans(14), fill=INK)
    d.text((M, 1008), "Sources: Guardian · AP · Reuters · CNN · Al Jazeera · Euronews · NPR · Anadolu · DW · Times of Israel · Democracy Now",
           font=sans_r(10), fill=MUTED)

    img.convert("RGB").save(out, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    land = load_land(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/ne_110m_land.geojson"))
    build(land, out)
    print("wrote", out, os.path.getsize(out), "bytes")
