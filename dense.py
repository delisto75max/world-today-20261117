"""Dense edition: 38 verified stories from Tuesday 17 November 2026 on one page.

Build-time renderer (Pillow). Reuses the map and icon helpers of render.py.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

import render as R

W = H = 1024
M = 28

PAPER = R.PAPER
INK = R.INK
RED = R.RED
SLATE = R.SLATE
GOLD = R.GOLD
MUTED = R.MUTED

# card colours, flat blocks behind each illustration
BG = {
    "war": (222, 226, 216),
    "mideast": (233, 220, 205),
    "asia": (216, 224, 228),
    "tech": (223, 226, 216),
    "money": (233, 226, 208),
    "europe": (228, 220, 224),
}


def rule(d, x0, y, x1, color=INK, w=2):
    d.rectangle([x0, y, x1, y + w - 1], fill=color)


def flag(d, x, y, w, h, code):
    """A 3-stripe or simple geometric flag, drawn flat."""
    if code == "us":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        for i in range(7):
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                        fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        d.rectangle([x, y, x + w * 0.42, y + h * 0.54], fill=(30, 50, 100))
    elif code == "ir":
        for i, c in enumerate([(35, 120, 70), (255, 255, 255), (200, 40, 45)]):
            d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    elif code == "ph":
        d.rectangle([x, y, x + w, y + h / 2], fill=(30, 60, 140))
        d.rectangle([x, y + h / 2, x + w, y + h], fill=(180, 40, 50))
        d.polygon([(x, y), (x + w * 0.38, y + h / 2), (x, y + h)], fill=(255, 255, 255))
    elif code == "rs":
        for i, c in enumerate([(180, 40, 50), (30, 50, 120), (255, 255, 255)]):
            d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    elif code == "de":
        for i, c in enumerate([(20, 20, 20), (200, 40, 45), (230, 190, 60)]):
            d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    elif code == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(200, 40, 45))
        d.ellipse([x + 4, y + 3, x + 12, y + 11], fill=(240, 200, 60))
    elif code == "jp":
        d.rectangle([x, y, x + w, y + h], fill=(250, 250, 246))
        d.ellipse([x + w / 2 - h * 0.3, y + h * 0.2, x + w / 2 + h * 0.3, y + h * 0.8],
                  fill=(190, 45, 55))
    else:
        d.rectangle([x, y, x + w, y + h], fill=(200, 200, 195))


def card_big(img, d, x, y, w, h, kicker, head, sub, bg, draw_ill, flags=()):
    d.rectangle([x, y, x + w, y + h], fill=(252, 249, 242))
    d.rectangle([x, y, x + w, y + h], outline=(206, 198, 182), width=1)
    ill_h = 92
    d.rectangle([x + 1, y + 1, x + w - 1, y + ill_h], fill=bg)
    draw_ill(d, x + 1, y + 1, w - 2, ill_h)
    if flags:
        fx = x + w - 8 - len(flags) * 30
        for i, code in enumerate(flags):
            flag(d, fx + i * 30, y + 8, 26, 17, code)
    d.text((x + 10, y + ill_h + 16), kicker, font=R.mono(10), fill=RED)
    yy = y + ill_h + 38
    for line in R.fit_lines(d, head, R.serif(23), w - 20, 2):
        d.text((x + 10, yy), line, font=R.serif(23), fill=INK)
        yy += 25
    for line in R.fit_lines(d, sub, R.sans_r(13), w - 20, 2):
        d.text((x + 10, yy + 2), line, font=R.sans_r(13), fill=(52, 46, 38))
        yy += 16


def card_small(img, d, x, y, w, h, kicker, head, sub, bg, draw_ill, flags=()):
    d.rectangle([x, y, x + w, y + h], fill=(252, 249, 242))
    d.rectangle([x, y, x + w, y + h], outline=(206, 198, 182), width=1)
    ill_h = 58
    d.rectangle([x + 1, y + 1, x + w - 1, y + ill_h], fill=bg)
    draw_ill(d, x + 1, y + 1, w - 2, ill_h)
    if flags:
        fx = x + w - 6 - len(flags) * 24
        for i, code in enumerate(flags):
            flag(d, fx + i * 24, y + 6, 21, 14, code)
    d.text((x + 8, y + ill_h + 14), kicker, font=R.mono(9), fill=RED)
    yy = y + ill_h + 32
    for line in R.fit_lines(d, head, R.sans(16), w - 16, 2):
        d.text((x + 8, yy), line, font=R.sans(16), fill=INK)
        yy += 18
    for line in R.fit_lines(d, sub, R.sans_r(11), w - 16, 2):
        d.text((x + 8, yy + 2), line, font=R.sans_r(11), fill=(52, 46, 38))
        yy += 13


# ---------------------------------------------------------------- illustrations

def ill_bridge(d, x, y, w, h):
    R.icon_bridge(d, x, y, w, h)


def ill_radar(d, x, y, w, h):
    cx, cy = x + w * 0.30, y + h * 0.62
    d.arc([cx - 70, cy - 70, cx + 70, cy + 70], 200, 340, fill=INK, width=2)
    d.arc([cx - 48, cy - 48, cx + 48, cy + 48], 200, 340, fill=INK, width=2)
    d.arc([cx - 26, cy - 26, cx + 26, cy + 26], 200, 340, fill=RED, width=2)
    d.line([cx, cy, cx + 10, cy - 46], fill=INK, width=3)
    d.rectangle([cx - 22, cy, cx + 22, cy + 10], fill=INK)
    # incoming drone triangles
    for i, (dx, dy) in enumerate(((150, 18), (185, 34), (215, 12))):
        s = 7
        d.polygon([(x + dx, y + dy), (x + dx - s, y + dy - s * 1.6),
                   (x + dx + s, y + dy - s * 1.6)], fill=RED)
        d.line([x + dx, y + dy - s * 1.6, x + dx + 26, y + dy - 2], fill=(150, 60, 50), width=1)
    # ship with smoke
    sx, sy = x + w - 70, y + h - 26
    d.polygon([(sx, sy + 10), (sx + 52, sy + 10), (sx + 44, sy + 20), (sx + 8, sy + 20)], fill=INK)
    d.ellipse([sx + 18, sy - 14, sx + 36, sy + 6], fill=(150, 150, 145))


def ill_quad(d, x, y, w, h):
    # table, four chairs, four flags on the wall behind
    ty = y + 34
    d.rectangle([x + 40, ty + 22, x + w - 40, ty + 30], fill=INK)
    for fx in (x + 58, x + w - 58):
        d.line([fx, ty + 30, fx, ty + 54], fill=INK, width=3)
        d.line([fx - 12, ty + 54, fx + 12, ty + 54], fill=INK, width=3)
    for i, code in enumerate(["US", "AUS", "IND", "JPN"]):
        px = x + w / 2 - 104 + i * 54
        d.rectangle([px, y + 12, px + 44, y + 34], fill=PAPER, outline=INK, width=1)
        d.text((px + 22, y + 28), code, font=R.mono(10), fill=INK, anchor="ms")


def ill_chip(d, x, y, w, h):
    R.icon_chip(d, x + w / 2 - 24, y + 8, 48, h - 16)


def ill_chart(d, x, y, w, h):
    R.icon_chart(d, x + 26, y + 14, w - 60, h - 26)


def ill_house(d, x, y, w, h):
    R.icon_house(d, x + w / 2 - 26, y + 8, 52, h - 16)


def ill_jet(d, x, y, w, h):
    R.icon_jet(d, x + 20, y + 4, w - 40, h - 8)


def ill_parliament(d, x, y, w, h):
    cx = x + w / 2
    d.polygon([(cx - 70, y + h - 14), (cx, y + 10), (cx + 70, y + h - 14)], fill=(230, 226, 214), outline=INK)
    for i in range(7):
        bx = cx - 60 + i * 20
        d.rectangle([bx, y + h - 34, bx + 9, y + h - 14], fill=INK)
    d.rectangle([cx - 70, y + h - 12, cx + 70, y + h - 6], fill=INK)



def fit_one(d, text, path_size, maxw, fill, x, y):
    """Draw one line, shrinking the face until it fits, then eliding."""
    size = path_size
    while size > 7:
        f = R.font(R.DJV + "DejaVuSansMono.ttf", size) if False else R.sans(size)
        if R.tw(d, text, f) <= maxw:
            d.text((x, y), text, font=f, fill=fill)
            return
        size -= 1
    f = R.sans(size)
    t = text
    while R.tw(d, t + "…", f) > maxw and len(t) > 3:
        t = t[:-1]
    d.text((x, y), t.rstrip(" ,.;") + "…", font=f, fill=fill)


# ---------------------------------------------------------------- page

def build(polys, out):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)

    kick = "THE WORLD'S NEWS IN ONE PICTURE"
    d.text((M, 20), kick, font=R.mono(12), fill=INK)
    right = "40 STORIES · ALL FROM TUESDAY"
    d.text((W - M - R.tw(d, right, R.mono(12)), 20), right, font=R.mono(12), fill=INK)

    date = "Tuesday 17 November 2026"
    tracked_w = R.tw(d, date, R.serif(58))
    d.text(((W - tracked_w) / 2, 34), date, font=R.serif(50), fill=INK)
    rule(d, M, 92, W - M, INK, 3)

    # row 1: three big stories
    y1, h1 = 100, 222
    cw = (W - 2 * M - 2 * 14) / 3
    big = [
        ("EUROPE · UKRAINE", "Kerch Bridge span collapses",
         "Kyiv says a 227m road arch fell; Russia suspends traffic and admits damage.",
         "war", ill_bridge),
        ("MIDDLE EAST · IRAN", "Iran strikes US radar in Bahrain",
         "A third drone attack is intercepted; three ships burn in the Strait of Hormuz.",
         "mideast", ill_radar),
        ("ASIA · DIPLOMACY", "Quad leaders meet in Manila",
         "First Quad summit since 2024; Trump then meets Xi and Putin.",
         "asia", ill_quad),
    ]
    for i, (k, hd, sb, bg, fn) in enumerate(big):
        card_big(img, d, M + i * (cw + 14), y1, cw, h1, k, hd, sb, BG[bg], fn)

    # row 2: four medium stories
    y2, h2 = 330, 184
    cw2 = (W - 2 * M - 3 * 12) / 4
    small = [
        ("AMERICAS · TECH", "US tightens AI-chip exports", "Five nations added to the diversion watchlist.", "tech", ill_chip),
        ("BUSINESS · MARKETS", "Stocks, oil and gold slide", "Deutsche Bank falls 6% on a data leak.", "money", ill_chart),
        ("MIDDLE EAST · WEST BANK", "Settlers kill an elderly woman", "Ten more wounded in the central West Bank.", "mideast", ill_house),
        ("ASIA · DEFENCE", "Japan scrambles its jets", "Two suspected Russian aircraft breach airspace.", "asia", ill_jet),
    ]
    for i, (k, hd, sb, bg, fn) in enumerate(small):
        card_small(img, d, M + i * (cw2 + 12), y2, cw2, h2, k, hd, sb, BG[bg], fn)

    # bottom: map, one-line briefs, figures strip
    my0, my1 = 524, 812
    R.draw_map(img, d, (M, my0, M + 340, my1), polys, [
        {"lon": 34.5, "lat": 45.2, "label": "Crimea", "tx": 8, "ty": -22},
        {"lon": 50.6, "lat": 26.0, "label": "Bahrain", "tx": 8, "ty": 16},
        {"lon": 121.0, "lat": 14.6, "label": "Manila", "tx": -8, "ty": 16, "align": "right"},
        {"lon": -77.0, "lat": 38.9, "label": "Washington", "tx": 6, "ty": -20},
        {"lon": 35.2, "lat": 31.9, "label": "West Bank", "tx": -8, "ty": 18, "align": "right"},
    ])

    lx = M + 356
    d.text((lx, my0 + 10), "ALSO ON TUESDAY 17 NOVEMBER", font=R.mono(11), fill=INK)
    rule(d, lx, my0 + 18, W - M, INK, 1)

    items = [
        ("EUR", "Russian missiles hit Kyiv's two bridges"),
        ("EUR", "Russia says it downed 1,400 drones"),
        ("EUR", "US rebukes Ukraine's deep strikes"),
        ("EUR", "Germany, Norway fund Ukraine air defence"),
        ("EUR", "Serbia's parliament sits for first time"),
        ("EUR", "EU sees 1.4% growth, inflation above 3%"),
        ("ASI", "Xi hosts Trump and Putin on 19 November"),
        ("ASI", "Trump 'may' meet Kim Jong Un in China"),
        ("ASI", "Trump lands in Manila for ASEAN, Quad"),
        ("ASI", "Hundreds arrested at Manila protests"),
        ("ASI", "Japan offers ASEAN its oil storage"),
        ("ASI", "Four held in North Macedonia attack plot"),
        ("ASI", "Kim Jong Un tours a ski resort with family"),
        ("M.E", "Qatar warns of a Gulf escalation"),
        ("M.E", "Iran says it captured a US drone intact"),
        ("M.E", "Jordan blocks Telegram after attack"),
        ("M.E", "Germany urges more Gaza aid before winter"),
        ("M.E", "UN: strike hit near its Rafah fuel convoy"),
        ("M.E", "Israeli opposition cries 'attempted coup'"),
        ("M.E", "Jericho attack wounds three Israelis"),
        ("AFR", "Five EU states agree Rwanda return hub"),
        ("AFR", "South Africa: 17 killed in shootings"),
        ("AFR", "Mondlane's trial opens in Maputo"),
        ("AME", "JPMorgan blames a software bug"),
        ("AME", "United cancels dozens, delays 800+"),
        ("AME", "Trump: no responsibility for FAA stop"),
        ("AME", "Trump 'would not mind' Huang at Nvidia"),
        ("AME", "Karim Khan ordered to pay $7.7m"),
        ("AME", "Pope Leo XIV struck by a rosary in Peru"),
        ("GLB", "COP31 enters its final week in Antalya"),
        ("GLB", "Turkey seizes opposition Sozcu TV"),
        ("GLB", "Three US carriers now in the Middle East"),
        ("GLB", "Kyiv used Neptune and Flamingo missiles"),
    ]
    f_item = R.sans(10)
    f_reg = R.mono(7)
    col_w = (W - M - lx - 16) / 3
    per_col = 11
    for i, (region, text) in enumerate(items):
        col, row = divmod(i, per_col)
        x = lx + col * (col_w + 8)
        yy = my0 + 30 + row * 25
        d.text((x, yy), "%02d" % (i + 1), font=R.mono(8), fill=RED)
        d.text((x + 16, yy), region, font=f_reg, fill=MUTED)
        fit_one(d, text, 10, col_w - 20, INK, x + 16, yy + 8)

    # figures strip
    rule(d, M, 826, W - M, (170, 162, 146), 1)
    figs = [("1,400", "drones Russia says it downed"),
            ("800+", "US flights cut or delayed"),
            ("$7.7m", "ordered from Karim Khan"),
            ("40", "stories from Tuesday 17 Nov")]
    fw = (W - 2 * M) / 4
    for i, (num, lab) in enumerate(figs):
        x = M + i * fw
        d.text((x, 838), num, font=R.mono(24), fill=RED if i == 2 else INK)
        d.text((x, 868), lab, font=R.sans_r(11), fill=(52, 46, 38))

    # footer
    rule(d, M, 940, W - M, INK, 2)
    d.text((M, 950), "Every story happened or was first reported on Tuesday 17 November 2026. Contested claims are attributed.",
           font=R.sans_r(9), fill=MUTED)
    src = "Sources: Guardian · AP · Reuters · CNN · Al Jazeera · Anadolu · Euronews · DW · NPR · Democracy Now · Xinhua · The Hindu"
    d.text((M, 964), src, font=R.sans_r(9), fill=MUTED)
    d.text((W - M - R.tw(d, "TUESDAY 17 NOVEMBER 2026", R.mono(9)), 1004),
           "TUESDAY 17 NOVEMBER 2026", font=R.mono(9), fill=RED)

    img.convert("RGB").save(out, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "dense.png"
    land = R.load_land(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/ne_110m_land.geojson"))
    build(land, out)
    print("wrote", out, os.path.getsize(out))
