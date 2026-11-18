"""Dense edition v2: 44 stories, 11 illustrated cards, date as the headline."""

import os
import sys

from PIL import Image, ImageDraw

import dense as D
import render as R

W = H = 1024
M = 28

PAPER, INK, RED, SLATE, MUTED, GOLD = R.PAPER, R.INK, R.RED, R.SLATE, R.MUTED, R.GOLD
BG = D.BG


def rule(d, x0, y, x1, color=INK, w=2):
    d.rectangle([x0, y, x1, y + w - 1], fill=color)


def ill_kyiv(d, x, y, w, h):
    # two bridge decks over a river, one broken
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(206, 214, 218))
    for i, dy in enumerate((0.35, 0.62)):
        yy = y + h * dy
        d.rectangle([x + 6, yy, x + w * 0.42, yy + 5], fill=INK)
        d.rectangle([x + w * 0.52, yy, x + w - 6, yy + 5], fill=INK)
        d.polygon([(x + w * 0.42, yy + 5), (x + w * 0.40, yy - 7), (x + w * 0.455, yy + 5)], fill=INK)
        d.polygon([(x + w * 0.52, yy + 5), (x + w * 0.545, yy - 7), (x + w * 0.49, yy + 5)], fill=INK)
    d.ellipse([x + w * 0.43, y + h * 0.30, x + w * 0.51, y + h * 0.44], fill=(180, 178, 170))
    d.polygon([(x + w * 0.47, y + h * 0.28), (x + w * 0.44, y + h * 0.38),
               (x + w * 0.50, y + h * 0.38)], fill=RED)


def ill_gaza(d, x, y, w, h):
    # aid boxes and a crescent
    for i in range(3):
        bx = x + 14 + i * 30
        d.rectangle([bx, y + h - 34, bx + 24, y + h - 12], fill=(206, 190, 158), outline=INK)
        d.line([bx + 12, y + h - 34, bx + 12, y + h - 12], fill=RED, width=2)
    cx, cy, cr = x + w - 52, y + 26, 20
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=RED)
    d.ellipse([cx - cr + 9, cy - cr - 4, cx + cr + 9, cy + cr - 4], fill=BG["mideast"])


def ill_shooting(d, x, y, w, h):
    # three figures and a red cross marker
    for i, fx in enumerate((x + 26, x + 52, x + 78)):
        d.ellipse([fx - 6, y + 12, fx + 6, y + 24], fill=INK)
        d.line([fx, y + 24, fx, y + 44], fill=INK, width=4)
        d.line([fx, y + 30, fx - 8, y + 38], fill=INK, width=3)
        d.line([fx, y + 30, fx + 8, y + 38], fill=INK, width=3)
    d.rectangle([x + w - 52, y + 16, x + w - 16, y + 52], fill=RED)
    d.rectangle([x + w - 39, y + 22, x + w - 29, y + 46], fill=PAPER)
    d.rectangle([x + w - 46, y + 29, x + w - 22, y + 39], fill=PAPER)


def ill_parliament(d, x, y, w, h):
    cx = x + w / 2
    d.polygon([(cx - 58, y + h - 12), (cx, y + 10), (cx + 58, y + h - 12)],
              fill=(232, 228, 216), outline=INK)
    for i in range(6):
        bx = cx - 46 + i * 18
        d.rectangle([bx, y + h - 30, bx + 8, y + h - 12], fill=INK)
    d.rectangle([cx - 58, y + h - 10, cx + 58, y + h - 4], fill=INK)



def card_small2(img, d, x, y, w, h, kicker, head, sub, bg, draw_ill, flags=()):
    d.rectangle([x, y, x + w, y + h], fill=(252, 249, 242))
    d.rectangle([x, y, x + w, y + h], outline=(206, 198, 182), width=1)
    ill_h = 50
    d.rectangle([x + 1, y + 1, x + w - 1, y + ill_h], fill=bg)
    draw_ill(d, x + 1, y + 1, w - 2, ill_h)
    d.text((x + 8, y + ill_h + 13), kicker, font=R.mono(8), fill=RED)
    yy = y + ill_h + 27
    for line in R.fit_lines(d, head, R.sans(15), w - 16, 2):
        d.text((x + 8, yy), line, font=R.sans(15), fill=INK)
        yy += 16
    yy += 2
    for line in R.fit_lines(d, sub, R.sans_r(10), w - 16, 2):
        d.text((x + 8, yy), line, font=R.sans_r(10), fill=(52, 46, 38))
        yy += 11



def ill_virus(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2 + 2
    r = 16
    for i in range(12):
        import math as _m
        a = _m.pi * 2 * i / 12
        x1, y1 = cx + _m.cos(a) * r, cy + _m.sin(a) * r
        x2, y2 = cx + _m.cos(a) * (r + 8), cy + _m.sin(a) * (r + 8)
        d.line([x1, y1, x2, y2], fill=INK, width=2)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 226, 214), outline=INK, width=2)
    d.ellipse([cx - 6, cy - 4, cx + 2, cy + 4], fill=RED)


def ill_bars(d, x, y, w, h):
    base = y + h - 8
    for i, hh in enumerate((14, 22, 30, 40)):
        bx = x + 26 + i * 16
        d.rectangle([bx, base - hh, bx + 10, base], fill=INK)
    d.line([x + 18, base, x + 96, base], fill=INK, width=2)
    d.line([x + 20, base - 44, x + 20, base + 4], fill=INK, width=2)



def ill_garment(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    d.polygon([(cx - 22, cy - 14), (cx - 8, cy - 20), (cx, cy - 12), (cx + 8, cy - 20),
               (cx + 22, cy - 14), (cx + 30, cy - 2), (cx + 16, cy + 4), (cx + 16, cy + 20),
               (cx - 16, cy + 20), (cx - 16, cy + 4), (cx - 30, cy - 2)], fill=(238, 232, 220), outline=INK)
    d.line([cx - 8, cy - 18, cx, cy - 12, cx + 8, cy - 18], fill=RED, width=2)
    d.line([cx - 16, cy + 6, cx + 16, cy + 6], fill=RED, width=2)


def ill_cert(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - 26, cy - 18, cx + 26, cy + 18], fill=(250, 246, 236), outline=INK, width=2)
    for i in range(4):
        d.line([cx - 18, cy - 10 + i * 8, cx + 8, cy - 10 + i * 8], fill=(140, 134, 122), width=2)
    d.line([cx - 8, cy + 8, cx + 18, cy + 8], fill=(200, 60, 50), width=4)
    d.line([cx - 20, cy - 20, cx + 20, cy + 20], fill=RED, width=5)
    d.line([cx + 20, cy - 20, cx - 20, cy + 20], fill=RED, width=5)


def build(polys, out):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)

    kick = "THE WORLD'S NEWS IN ONE PICTURE"
    d.text((M, 18), kick, font=R.mono(12), fill=INK)
    right = "49 STORIES · 6 CONTINENTS · ALL FROM TUESDAY"
    d.text((W - M - R.tw(d, right, R.mono(12)), 18), right, font=R.mono(12), fill=INK)

    date = "Tuesday 17 November 2026"
    dw = R.tw(d, date, R.serif(50))
    d.text(((W - dw) / 2, 36), date, font=R.serif(50), fill=INK)
    rule(d, M, 92, W - M, INK, 3)

    # row 1: three big
    y1, h1 = 100, 212
    cw = (W - 2 * M - 2 * 14) / 3
    big = [
        ("EUROPE · UKRAINE", "Kerch Bridge span collapses",
         "Kyiv says a 227m road arch fell; Russia suspends traffic.",
         "war", D.ill_bridge),
        ("MIDDLE EAST · IRAN", "Iran strikes a US radar in Bahrain",
         "A third drone attack is intercepted; ships burn in Hormuz.",
         "mideast", D.ill_radar),
        ("ASIA · DIPLOMACY", "Quad leaders meet in Manila",
         "First summit since 2024; Trump then meets Xi and Putin.",
         "asia", D.ill_quad),
    ]
    for i, (k, hd, sb, bg, fn) in enumerate(big):
        D.card_big(img, d, M + i * (cw + 14), y1, cw, h1, k, hd, sb, BG[bg], fn)

    # rows 2 and 3: eight small
    cw2 = (W - 2 * M - 4 * 12) / 5
    rows = [
        [
            ("EUROPE · UKRAINE", "Russian missiles hit Kyiv's bridges", "North and South spans closed; two killed.", "war", ill_kyiv),
            ("ASIA · DEFENCE", "Japan scrambles its jets", "Two suspected Russian aircraft enter airspace.", "asia", D.ill_jet),
            ("AMERICAS · TECH", "US tightens AI-chip exports", "Five nations added to the diversion list.", "tech", D.ill_chip),
            ("BUSINESS · MARKETS", "Stocks, oil and gold slide", "Deutsche Bank falls 6% on a data leak.", "money", D.ill_chart),
            ("BUSINESS · TECH", "Nvidia posts $115.8bn quarter", "Revenue doubles; a first without Jensen Huang.", "tech", ill_bars),
        ],
        [
            ("MIDDLE EAST · WEST BANK", "Settlers kill an elderly woman", "Ten wounded in the central West Bank.", "mideast", D.ill_house),
            ("AMERICAS · HEALTH", "Measles-free status revoked", "The US, Mexico and Bolivia lose PAHO status.", "money", ill_cert),
            ("AFRICA · SAFETY", "17 killed in two shootings", "Separate attacks near Pietermaritzburg and Pretoria.", "war", ill_shooting),
            ("ASIA · LABOUR", "Bangladesh garment wage protests", "Tear gas in Dhaka as 500 factories shut.", "asia", ill_garment),
            ("AFRICA · HEALTH", "Ebola cases top 11,000", "5,400 deaths in DR Congo, WHO says.", "war", ill_virus),
        ],
    ]
    for r, row in enumerate(rows):
        y = 318 + r * 140
        for i, (k, hd, sb, bg, fn) in enumerate(row):
            card_small2(img, d, M + i * (cw2 + 12), y, cw2, 132, k, hd, sb, BG[bg], fn)

    # bottom: map + briefs
    my0, my1 = 600, 890
    R.draw_map(img, d, (M, my0, M + 316, my1), polys, [
        {"lon": 34.5, "lat": 45.2, "label": "Crimea", "tx": 8, "ty": -20},
        {"lon": 50.6, "lat": 26.0, "label": "Bahrain", "tx": 8, "ty": 16},
        {"lon": 121.0, "lat": 14.6, "label": "Manila", "tx": -8, "ty": 16, "align": "right"},
        {"lon": -77.0, "lat": 38.9, "label": "Washington", "tx": 6, "ty": -18},
        {"lon": 35.2, "lat": 31.9, "label": "West Bank", "tx": -8, "ty": 18, "align": "right"},
    ])

    lx = M + 332
    d.text((lx, my0 + 8), "ALSO ON TUESDAY 17 NOVEMBER", font=R.mono(10), fill=INK)
    rule(d, lx, my0 + 16, W - M, INK, 1)

    items = [
        ("EUR", "Russia says it downed 1,400 drones"),
        ("EUR", "US rebukes Ukraine's deep strikes"),
        ("EUR", "Germany, Norway fund Ukraine air defence"),
        ("EUR", "EU sees 1.4% growth, inflation above 3%"),
        ("EUR", "Moldova shuts its airspace over a drone"),
        ("EUR", "Pope Leo XIV struck by a rosary in Peru"),
        ("ASI", "Xi hosts Trump and Putin on 19 November"),
        ("ASI", "Trump 'may' meet Kim Jong Un in China"),
        ("ASI", "Trump lands in Manila for ASEAN, Quad"),
        ("ASI", "Hundreds arrested at Manila protests"),
        ("ASI", "Japan offers ASEAN its oil storage"),
        ("ASI", "Four held in North Macedonia attack plot"),
        ("ASI", "Kim Jong Un tours a ski resort with family"),
        ("ASI", "Cyclone Akvan nears India's east coast"),
        ("ASI", "Banda Sea 6.6 quake felt in Darwin"),
        ("M.E", "Qatar warns of a Gulf escalation"),
        ("M.E", "Iran says it captured a US drone intact"),
        ("M.E", "Jordan blocks Telegram after attack"),
        ("M.E", "UN: strike hit near its Rafah fuel convoy"),
        ("M.E", "Israeli opposition cries 'attempted coup'"),
        ("M.E", "Jericho attack wounds three Israelis"),
        ("M.E", "Kuwait says it repelled drone attacks"),
        ("AFR", "Five EU states agree Rwanda return hub"),
        ("AFR", "Mondlane's trial opens in Maputo"),
        ("AFR", "UN: 2,230 civilians killed in Sudan this year"),
        ("AME", "JPMorgan blames a software bug"),
        ("AME", "United cancels dozens, delays 800+"),
        ("AME", "Trump: no responsibility for FAA stop"),
        ("AME", "Trump 'would not mind' Huang at Nvidia"),
        ("AME", "Karim Khan ordered to pay $7.7m"),
        ("AME", "Brazil's Senate votes on a $9.7bn package"),
        ("OCE", "Australia eases backpacker visa curbs"),
        ("GLB", "COP31 enters its final week in Antalya"),
        ("GLB", "Turkey seizes opposition Sozcu TV"),
        ("GLB", "Three US carriers now in the Middle East"),
        ("GLB", "Kyiv used Neptune and Flamingo missiles"),
    ]
    f_reg = R.mono(7)
    col_w = (W - M - lx - 16) / 3
    per_col = 12
    for i, (region, text) in enumerate(items):
        col, row = divmod(i, per_col)
        x = lx + col * (col_w + 8)
        yy = my0 + 18 + row * 22
        d.text((x, yy), "%02d" % (i + 1), font=R.mono(8), fill=RED)
        d.text((x + 16, yy), region, font=f_reg, fill=MUTED)
        D.fit_one(d, text, 10, col_w - 20, INK, x + 16, yy + 8)

    # footer
    rule(d, M, 900, W - M, INK, 2)
    d.text((M, 910), "1,400 DOWNED · 800+ FLIGHTS · $7.7M · 49 STORIES", font=R.mono(13), fill=INK)
    d.text((W - M - R.tw(d, "TUESDAY 17 NOVEMBER 2026", R.mono(11)), 910),
           "TUESDAY 17 NOVEMBER 2026", font=R.mono(11), fill=RED)
    d.text((M, 936), "Every story happened or was first reported on Tuesday 17 November 2026. Contested claims are attributed.",
           font=R.sans_r(9), fill=MUTED)
    src = "Sources: Guardian · AP · Reuters · CNN · Al Jazeera · Anadolu · Euronews · DW · NPR · Democracy Now · Xinhua · The Hindu"
    d.text((M, 950), src, font=R.sans_r(9), fill=MUTED)

    img.convert("RGB").save(out, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "dense2.png"
    land = R.load_land(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/ne_110m_land.geojson"))
    build(land, out)
    print("wrote", out, os.path.getsize(out))
