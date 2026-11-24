# -*- coding: utf-8 -*-
"""Bộ sinh website tĩnh temnhantamtinphat.com
Chạy: python3 build.py  -> xuất toàn bộ trang vào thư mục dist/
Nội dung danh mục và bài viết nằm ở content.py (sau này có thể đọc từ Google Sheet).
"""
import json, os, shutil, html
LOCAL_GODEX = os.environ.get('LOCAL_GODEX') == '1'
from urllib.parse import quote
from content import SITE, CATS, POSTS, FSC
import re
from godex_list import ITEMS as GITEMS, FILTERS as GFILTERS
from catalog import GROUPS, WHITE, WHITE_FILTERS, BESPOKE, MATERIALS, COLOR_TYPES, COLOR_OPTIONS, GODEX, GODEX_FILTERS, SUPPLIES, PHOTOS_WHITE
if FSC["status"] == "pending":
    CATS = [c for c in CATS if not c.get("fsc")]
    POSTS = [p for p in POSTS if not p.get("fsc")]
FSC_ON = FSC["status"] in ("active", "preview")
CERT_TXT = FSC["cert"] or "Hiển thị khi được cấp chứng chỉ"
for _c in CATS:
    _c["spec"] = [(k, v.replace("{cert}", CERT_TXT)) for k, v in _c["spec"]]

BASE = SITE["domain"]
OUT = os.path.join(os.path.dirname(__file__), "dist")
SRC = os.path.join(os.path.dirname(__file__), "src")
e = html.escape

# ---------- SVG helpers ----------
def lotus(size=42):
    return f'''<svg viewBox="0 0 48 48" width="{size}" height="{size}" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#a3121d"/><circle cx="24" cy="21" r="12" fill="#f5b70a" opacity=".9"/><path d="M24 10c5 5 6 12 0 22-6-10-5-17 0-22z" fill="#fff"/><path d="M24 32c-3-6-9-9-15-8 2 6 8 9 15 8z" fill="#ffd9d3"/><path d="M24 32c3-6 9-9 15-8-2 6-8 9-15 8z" fill="#ffd9d3"/><g fill="#a3121d"><rect x="21" y="17" width="1.4" height="9"/><rect x="23" y="17" width=".8" height="9"/><rect x="24.6" y="17" width="1.6" height="9"/></g><path d="M10 36h28" stroke="#f5b70a" stroke-width="2" stroke-linecap="round"/></svg>'''

def barcode(x, y, w, h, seed=7, color="#1d0f10"):
    s = seed; bars = []; cx = x
    while cx < x + w - 2:
        s = s * 16807 % 2147483647
        bw = 1 + s % 3
        bars.append(f'<rect x="{cx:.1f}" y="{y}" width="{bw}" height="{h}" fill="{color}"/>')
        cx += bw + 1 + (s >> 3) % 2
    return "".join(bars)

def label(kind, x, y, w=150, h=110, seed=3):
    """One die-cut label of a given job type, drawn at x,y."""
    r = 14
    if kind == "trang":
        return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" stroke="#e5d9d6"/>'
                f'<rect x="{x+14}" y="{y+14}" width="{w*.55}" height="8" rx="4" fill="#1d0f10"/>'
                f'<rect x="{x+14}" y="{y+28}" width="{w*.35}" height="6" rx="3" fill="#b8a9a6"/>'
                + barcode(x+14, y+44, w-28, h-72, seed) +
                f'<rect x="{x+14}" y="{y+h-22}" width="{w*.45}" height="6" rx="3" fill="#1d0f10"/></g>')
    if kind == "mau":
        cols = [("#f5b70a", "#a3121d"), ("#2bb673", "#0b5d3b"), ("#ff7a59", "#7d0b14"), ("#5b8def", "#16306b")][seed % 4]
        return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{cols[1]}"/>'
                f'<circle cx="{x+w*.72}" cy="{y+h*.42}" r="{h*.33}" fill="{cols[0]}"/>'
                f'<circle cx="{x+w*.72}" cy="{y+h*.42}" r="{h*.18}" fill="#fff" opacity=".85"/>'
                f'<rect x="{x+14}" y="{y+18}" width="{w*.4}" height="12" rx="6" fill="#fff"/>'
                f'<rect x="{x+14}" y="{y+38}" width="{w*.28}" height="7" rx="3.5" fill="#fff" opacity=".7"/>'
                f'<rect x="{x}" y="{y+h-26}" width="{w}" height="26" fill="#fff" opacity=".18"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="#fff" stroke-opacity=".4"/></g>')
    if kind == "vo":
        cracks = "".join(f'<path d="M{x+10+i*22} {y+12} l8 {h*.3} -6 {h*.25} 10 {h*.3}" stroke="#d9c9c5" fill="none"/>' for i in range(int(w/22)))
        return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if w==h else r}" fill="#fff" stroke="#e5d9d6"/>{cracks}'
                f'<rect x="{x+12}" y="{y+h/2-16}" width="{w-24}" height="32" rx="8" fill="#a3121d"/>'
                f'<text x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle" font-size="{min(16,w*0.105):.1f}" font-weight="800" fill="#fff" font-family="Be Vietnam Pro,Arial">BẢO HÀNH</text></g>')
    if kind == "nhua":
        return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#silver)" stroke="#fff"/>'
                f'<rect x="{x+16}" y="{y+18}" width="{w*.5}" height="12" rx="6" fill="#1d0f10" opacity=".75"/>'
                f'<path d="M{x+16} {y+h-30} q{w*.2} -24 {w*.4} 0 t{w*.35} 0" stroke="#a3121d" stroke-width="5" fill="none"/>'
                f'<rect x="{x+8}" y="{y+6}" width="{w*.35}" height="{h-12}" rx="10" fill="#fff" opacity=".35"/></g>')
    if kind == "nhiet":
        lines = "".join(f'<rect x="{x+14}" y="{y+16+i*14}" width="{(w-28)*(0.5+((seed+i)*37%50)/100)}" height="6" rx="3" fill="#9c8f8c"/>' for i in range(5))
        return (f'<g><path d="M{x} {y}h{w}v{h-10}l-12 10-12-10-12 10-12-10-12 10-12-10-12 10-12-10-12 10-12-10-12 10-12-10-12 10-{w-144}-10z" fill="#fff" stroke="#e5d9d6"/>{lines}'
                f'<rect x="{x+14}" y="{y+h-34}" width="{w-28}" height="12" rx="3" fill="#1d0f10"/></g>')
    if kind == "fsc":
        trees = "".join(f'<path d="M{x+18+i*26} {y+h-18} l11 -30 l11 30z" fill="#1f7a4d" opacity="{.6+i*.1:.1f}"/>' for i in range(int((w-30)/26)))
        return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" stroke="#cfe5d8"/>'
                f'<rect x="{x+14}" y="{y+14}" width="{w*.5}" height="10" rx="5" fill="#1d0f10"/>'
                f'<rect x="{x+14}" y="{y+30}" width="{w*.3}" height="6" rx="3" fill="#b8a9a6"/>{trees}'
                f'<rect x="{x+12}" y="{y+h-18}" width="{w-24}" height="4" rx="2" fill="#1f7a4d"/></g>')
    if kind == "nganh":
        c = ["#a3121d", "#2bb673", "#f5b70a", "#5b8def"][seed % 4]
        return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#fff" stroke="#e5d9d6"/>'
                f'<circle cx="{x+h/2}" cy="{y+h/2}" r="{h*.32}" fill="{c}"/>'
                f'<rect x="{x+h}" y="{y+h*.32}" width="{w-h-18}" height="10" rx="5" fill="#1d0f10"/>'
                f'<rect x="{x+h}" y="{y+h*.55}" width="{(w-h)*.5}" height="7" rx="3.5" fill="#b8a9a6"/></g>')
    return ""

DEFS = '<defs><linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef1f4"/><stop offset=".5" stop-color="#c7ced6"/><stop offset="1" stop-color="#f6f7f9"/></linearGradient><linearGradient id="core" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3e7dc"/><stop offset="1" stop-color="#cdb8a3"/></linearGradient></defs>'

KIND_PHOTO = {"trang": ("tem-35x22-ke-sat", "Tem nhãn trắng 35x22 bế sẵn, chụp tại kho"),
              "nhiet": ("nhiet-lien-tuc-76", "Cuộn decal nhiệt liên tục khổ 76 tại kho")}
KIND_TILE = {"mau": ("Tem in màu", "In 5–6 màu · cán màng · bế hình"),
             "vo": ("Decal vỡ", "Bóc là vỡ · tem bảo hành"),
             "nhua": ("Decal nhựa", "PP · PVC · trong · xi bạc"),
             "nganh": ("Theo ngành", "Mỹ phẩm · thực phẩm · dược · điện tử"),
             "fsc": ("FSC CoC", "Vật liệu có chứng nhận"),
             "trang": ("Tem bế trắng", "Decal nhiệt · decal giấy"),
             "nhiet": ("Giấy in nhiệt", "K57 · K80 · K110")}

def tile(title, sub, tone=""):
    return f'<div class="tile {tone}"><b>{e(title)}</b><span>{e(sub)}</span></div>'

def roll_svg(kind, bg=None):
    """Ảnh thật nếu có, nếu chưa có thì khối chữ thương hiệu (không dùng hình vẽ giả)."""
    if kind in KIND_PHOTO:
        n, a = KIND_PHOTO[kind]
        return img(n, a, 960, 1200, "cover")
    t, s = KIND_TILE.get(kind, ("Tâm Tín Phát", "Xưởng in tem nhãn"))
    return tile(t, s, "t-" + kind)

def hero_svg():
    items = [("a6-cuon-100x150x350", "Decal nhiệt 100x150 cuộn 350 tem"), ("tem-35x22-ke-sat", "Tem 35x22 bo góc"),
             ("thung-decal-tem-nhiet", "Thùng decal tem nhiệt"), ("a7-xap-75x105x500", "Decal nhiệt 75x105 xấp 500 tem"),
             ("cuon-35x22x25", "Decal nhiệt 35x22 cuộn 25 m"), ("tem-trang-suc", "Tem trang sức đuôi gập"),
             ("nhiet-lien-tuc-76", "Decal nhiệt liên tục khổ 76"), ("thung-cuon-100x150", "Thùng cuộn 100x150")]
    one = "".join(f'<figure>{img(n, a, 960, 1200, "", i < 3)}</figure>' for i, (n, a) in enumerate(items))
    return f'<div class="photo-belt" aria-label="Ảnh thật sản phẩm tại kho"><div class="pb-track">{one}{one.replace("<figure>", "<figure aria-hidden=true>")}</div></div>'

def printer_svg(kind="ban", bg=None, model="GoDEX"):
    sub = {"ban": "Máy in để bàn", "cn": "Máy in công nghiệp", "dd": "Máy in cầm tay"}.get(kind, "Máy in mã vạch")
    return tile(model, sub, "t-godex")

def poster_svg(cap=""):
    rollers = "".join(f'<circle cx="{120+i*150}" cy="150" r="46" fill="#3a2224"/><circle cx="{120+i*150}" cy="150" r="30" fill="#5a3a3c"/><circle cx="{120+i*150}" cy="150" r="8" fill="#f5b70a"/>' for i in range(5))
    return (f'<svg class="poster" viewBox="0 0 800 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<defs><radialGradient id="glow" cx=".5" cy=".2" r=".8"><stop offset="0" stop-color="#7d0b14"/><stop offset="1" stop-color="#1d0f10"/></radialGradient></defs>'
            f'<rect width="800" height="450" fill="url(#glow)"/>'
            f'<rect x="40" y="200" width="720" height="150" rx="18" fill="#2a1517"/>{rollers}'
            f'<path d="M0 104 C200 96 260 196 420 196 S640 110 800 104" stroke="#fff" stroke-width="16" fill="none" opacity=".92"/>'
            + "".join(f'<rect x="{30+i*86}" y="{96 + (0 if i<2 else 0)}" width="0" height="0"/>' for i in range(1)) +
            f'<rect x="0" y="380" width="800" height="70" fill="#000" opacity=".35"/></svg>')

def map_svg():
    return ('<svg viewBox="0 0 600 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<rect width="600" height="300" fill="#eef3e6"/>'
            '<path d="M-10 220 C120 190 200 260 330 230 S520 170 620 200 L620 320 L-10 320z" fill="#bfe0ee"/>'
            '<path d="M-10 120 L620 90" stroke="#fff" stroke-width="22"/><path d="M-10 120 L620 90" stroke="#f5b70a" stroke-width="3" stroke-dasharray="14 10"/>'
            '<path d="M260 -10 L300 320" stroke="#fff" stroke-width="16"/><path d="M80 -10 L120 210" stroke="#fff" stroke-width="10"/><path d="M430 -10 L460 200" stroke="#fff" stroke-width="10"/>'
            + "".join(f'<rect x="{x}" y="{y}" width="46" height="30" rx="6" fill="#dfe7d2"/>' for x, y in [(140,30),(330,20),(350,130),(150,140),(480,120),(30,40)]) +
            '<g transform="translate(318 112)"><ellipse cx="0" cy="44" rx="18" ry="6" fill="#000" opacity=".15"/><path d="M0 44 C-26 10 -30 -6 -30 -16 a30 30 0 0 1 60 0 c0 10 -4 26 -30 60z" fill="#a3121d"/><circle cy="-16" r="12" fill="#fff"/></g>'
            '<rect x="350" y="80" width="200" height="40" rx="12" fill="#fff"/><text x="364" y="106" font-size="16" font-weight="700" fill="#1d0f10" font-family="Be Vietnam Pro,Arial">Xưởng Tâm Tín Phát</text></svg>')

IC = {
 "phone": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg>',
 "zalo": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3C6.5 3 2 6.8 2 11.4c0 2.6 1.4 4.9 3.7 6.4L5 21l3.6-1.9c1.1.3 2.2.5 3.4.5 5.5 0 10-3.8 10-8.3S17.5 3 12 3z" fill="currentColor"/><path d="M8 9h4.6L8 14.2h4.8" stroke="#0068ff" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 9v5.2" stroke="#0068ff" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "play": '<svg viewBox="0 0 24 24" fill="#1d0f10" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>',
 "quote": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="3"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
}
STEP_IC = [
 '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="8" y="5" width="28" height="38" rx="6" fill="#a3121d"/><path d="M14 16h16M14 23h16M14 30h10" stroke="#fff" stroke-width="3" stroke-linecap="round"/><circle cx="37" cy="36" r="9" fill="#f5b70a"/><path d="M33 36l3 3 5-6" stroke="#1d0f10" stroke-width="2.5" fill="none"/></svg>',
 '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="5" y="9" width="38" height="28" rx="6" fill="#f5b70a"/><rect x="11" y="15" width="16" height="16" rx="4" fill="#fff"/><path d="M31 18h7M31 24h7M31 30h5" stroke="#1d0f10" stroke-width="2.5" stroke-linecap="round"/><path d="M18 41h12" stroke="#a3121d" stroke-width="4" stroke-linecap="round"/></svg>',
 '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="4" y="18" width="40" height="18" rx="5" fill="#a3121d"/><circle cx="14" cy="27" r="5" fill="#fff"/><circle cx="34" cy="27" r="5" fill="#fff"/><path d="M10 18V8h28v10" fill="#f5b70a"/><rect x="12" y="36" width="24" height="7" fill="#fff" stroke="#a3121d" stroke-width="2"/></svg>',
 '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="3" y="14" width="26" height="20" rx="3" fill="#a3121d"/><path d="M29 20h9l6 7v7H29z" fill="#f5b70a"/><circle cx="12" cy="37" r="5" fill="#1d0f10"/><circle cx="36" cy="37" r="5" fill="#1d0f10"/></svg>',
]

# ---------- page chrome ----------
NAV = [("index.html#danh-muc", "Sản phẩm", "sp"), ("bai-viet.html", "Bài viết", "bv"), ("gioi-thieu.html", "Giới thiệu", "gt"), ("lien-he.html", "Liên hệ", "lh")]

def nav_html():
    out = []
    for h, n, k in NAV:
        if k == "sp":
            sub = "".join(f'<li><a href="{g["slug"]}.html"><b>{e(g["name"])}</b><small>{e(GROUP_HINT[g["slug"]])}</small></a></li>' for g in GROUPS)
            out.append(f'<li class="has-sub"><a href="index.html#danh-muc" aria-haspopup="true">{n} <span class="caret">▾</span></a><ul class="sub">{sub}</ul></li>')
        else:
            out.append(f'<li><a href="{h}">{n}</a></li>')
    return "".join(out)

GROUP_HINT = {"san-pham-tem-be-trang": "Decal nhiệt, decal giấy, vận đơn, giấy bill",
              "san-pham-tem-mau": "Tem logo, mỹ phẩm, thực phẩm, decal vỡ, xi bạc",
              "thiet-bi-godex": "Máy in mã vạch, ruy băng, đầu in"}

def url(path):
    if path in ("index.html", ""):
        return BASE + "/"
    return BASE + "/" + path.replace(".html", "")

def org_schema():
    s = SITE
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE + "/#xuong",
        "name": s["legal"], "alternateName": s["brand"], "url": BASE + "/",
        "telephone": s["hotline_raw"], "email": s["email"],
        "address": {"@type": "PostalAddress", "streetAddress": s["street"], "addressLocality": s["locality"], "addressRegion": "TP. Hồ Chí Minh", "addressCountry": "VN"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "07:30", "closes": "17:00"}],
        "areaServed": "VN", "hasMap": s["map_link"],
        "description": "Xưởng in tem nhãn, decal, tem mã vạch, giấy in nhiệt tại Bình Chánh, TP.HCM. Đạt ISO 9001:2015.",
    }

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}

def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + '</script>'

def head(title, desc, path, schemas=()):
    gtm = ""
    if SITE.get("gtm"):
        g = SITE["gtm"]
        gtm = f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{g}');</script>"
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url(path)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:locale" content="vi_VN">
<meta property="og:site_name" content="{e(SITE['brand'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{BASE}/img/a6-cuon-100x150x350.webp">
<meta name="theme-color" content="#a3121d">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="style.css">
{gtm}
{"".join(ld(x) for x in schemas)}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="index.html">{lotus()}<span>Tâm Tín Phát<small>Xưởng in tem nhãn</small></span></a>
<button class="burger" aria-label="Mở menu" aria-expanded="false"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<ul class="menu">{nav_html()}</ul>
<a class="btn btn-red" href="lien-he.html#bao-gia">Nhận báo giá</a>
</div></header>
<main>
'''

def foot():
    s = SITE
    cats = "".join(f'<li><a href="{c["slug"]}.html">{e(c["name"])}</a></li>' for c in CATS)
    posts = "".join(f'<li><a href="{p["slug"]}.html">{e(p["short"])}</a></li>' for p in POSTS)
    return f'''</main>
<footer><div class="wrap">
<div class="cols">
<div><a class="brand" href="index.html" style="color:#fff">{lotus()}<span>{e(s["legal"])}<small style="color:#b89f9b">Xưởng in tem nhãn · ISO 9001:2015</small></span></a>
<p style="margin-top:14px">{e(s["address"])}</p>
<p>Hotline: <a href="tel:{s["hotline_raw"]}">{s["hotline"]}</a><br>Zalo: <a href="{s["zalo"]}">{s["zalo_num"]}</a><br>Email: <a href="mailto:{s["email"]}">{s["email"]}</a></p>
<p>{e(s["hours"])}</p></div>
<div><h4>Sản phẩm</h4><ul>{"".join(f'<li><a href="{g["slug"]}.html"><b>{e(g["name"])}</b></a></li>' for g in GROUPS)}{cats}</ul></div>
<div><h4>Bài viết</h4><ul>{posts}<li><a href="bai-viet.html">Tất cả bài viết</a></li></ul></div>
<div><h4>Công ty</h4><ul><li><a href="gioi-thieu.html">Giới thiệu xưởng</a></li><li><a href="lien-he.html">Liên hệ & bản đồ</a></li><li><a href="chinh-sach-bao-mat.html">Chính sách bảo mật</a></li><li><a href="so-do-trang.html">Sơ đồ trang</a></li><li><a href="sitemap.xml">Sitemap XML</a></li></ul></div>
</div>
<div class="legal"><span>© 2026 {e(s["legal"])}</span><span>temnhantamtinphat.com</span></div>
</div></footer>
<nav class="dock" aria-label="Liên hệ nhanh">
<a class="c" href="tel:{s["hotline_raw"]}" aria-label="Gọi {s["hotline"]}">{IC["phone"]}<span>Gọi</span></a>
<a class="z" href="{s["zalo"]}" aria-label="Nhắn Zalo {s["zalo_num"]}">{IC["zalo"]}<span>Zalo</span></a>
<a class="q" href="lien-he.html#bao-gia" aria-label="Nhận báo giá">{IC["quote"]}<span>Báo giá</span></a>
</nav>
<script src="app.js" defer></script>
</body>
</html>
'''

def video_block(v, title):
    yt = v.get("yt", "")
    return f'''<button class="video" type="button" data-yt="{e(yt)}" data-title="{e(title)}" aria-label="Phát video: {e(v["cap"])}">{poster_svg()}<span class="play">{IC["play"]}</span><span class="cap">{e(v["cap"])}</span></button>'''

def quote_form(pre=""):
    opts = "".join(f'<option{" selected" if c["slug"]==pre else ""}>{e(c["name"])}</option>' for c in CATS)
    return f'''<form class="quote" novalidate>
<div class="row2"><label for="f-ten">Họ tên<input id="f-ten" name="ho_ten" autocomplete="name" required></label>
<label for="f-sdt">Số điện thoại / Zalo<input id="f-sdt" name="sdt" type="tel" inputmode="tel" autocomplete="tel" required></label></div>
<label for="f-loai">Loại tem cần in<select id="f-loai" name="nhom">{opts}<option>Chưa rõ, cần tư vấn</option></select></label>
<div class="row2"><label for="f-kt">Kích thước (mm)<input id="f-kt" name="kich_thuoc" placeholder="VD: 50 × 30"></label>
<label for="f-sl">Số lượng<input id="f-sl" name="so_luong" placeholder="VD: 10 cuộn / 5.000 tem"></label></div>
<label for="f-gc">Ghi chú<textarea id="f-gc" name="ghi_chu" placeholder="Chất liệu, số màu, cán màng, máy in đang dùng…"></textarea></label>
<input type="text" name="web" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
<button class="btn btn-red" type="submit">Gửi yêu cầu báo giá {IC["arrow"]}</button>
<p class="ok" role="status"></p>
<p class="muted" style="font-size:14px;margin:0">Có sẵn file thiết kế? Gửi thẳng qua Zalo <a href="{SITE["zalo"]}">{SITE["zalo_num"]}</a> cho nhanh.</p>
</form>'''

def map_block():
    s = SITE
    return f'''<div class="map"><div class="art">{map_svg()}</div>
<div class="info"><h3>Ghé xưởng xem mẫu</h3>
<p>{e(s["address"])}</p><p class="muted">{e(s["hours"])}</p>
<div class="acts"><button class="btn btn-red" type="button" data-map="{e(s["map_embed"])}">Xem bản đồ</button>
<a class="btn btn-line" href="{e(s["map_link"])}" rel="noopener">Chỉ đường Google Maps</a></div></div></div>'''

def contact_band(pre=""):
    return f'''<section class="band" id="bao-gia"><div class="wrap">
<div class="head"><h2>Gửi kích thước, nhận báo giá</h2><p class="muted">Điền vài dòng hoặc gọi thẳng <a href="tel:{SITE["hotline_raw"]}"><b>{SITE["hotline"]}</b></a>. Nhân viên kinh doanh gọi lại tư vấn chất liệu và giá.</p></div>
<div class="contact"><div class="panel">{quote_form(pre)}</div>{map_block()}</div>
</div></section>'''

def cat_card(c, big=False):
    return f'''<a class="cat{' big' if big else ''}" href="{c["slug"]}.html"><div class="pic">{roll_svg(c["kind"])}</div>
<div class="txt"><h3>{e(c["name"])}</h3><p>{e(c["short"])}</p><span class="go">Xem chi tiết {IC["arrow"]}</span></div></a>'''

def group_card(g):
    pic = {"godex": printer_svg("ban", model="GoDEX"), "trang": img("a6-cuon-100x150x350", "Decal nhiệt 100x150 tại kho Tâm Tín Phát", 960, 1200, "cover"),
           "mau": img("banner-tem-nhan", "Các loại tem nhãn in màu Tâm Tín Phát", 1376, 768, "cover")}[g["kind"]]
    return f'''<a class="cat grp" href="{g["slug"]}.html"><div class="pic">{pic}</div>
<div class="txt"><h3>{e(g["name"])}</h3><p>{e(GROUP_HINT[g["slug"]])}</p><span class="go">Xem bảng mã {IC["arrow"]}</span></div></a>'''

def post_card(p):
    c = next(x for x in CATS if x["slug"] == p["cat"])
    pic = img("tem-35x22-thuoc", p["title"], 960, 1200, "cover") if p["slug"].startswith("kich-thuoc") else roll_svg(c["kind"])
    return f'''<a class="post" href="{p["slug"]}.html"><div class="pic">{pic}<span class="vtag">Có video</span></div>
<div class="txt"><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><time datetime="{p["date"]}">{p["date_vn"]}</time></div></a>'''

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

def fsc_band():
    if not FSC_ON:
        return ""
    note = '<p class="muted" style="font-size:14px">Bản xem trước: phần FSC chỉ bật trên web thật khi xưởng đã được cấp mã chứng chỉ.</p>' if FSC["status"] == "preview" else ""
    code = f'<p><b>Mã chứng chỉ:</b> {e(FSC["cert"])} · tra cứu tại info.fsc.org</p>' if FSC["cert"] else ""
    return f'''<section class="band fscb"><div class="wrap fgrid">
<div class="pic">{roll_svg("fsc", "#eaf5ee")}</div>
<div><h2>Tem nhãn có chứng nhận FSC cho hàng xuất khẩu</h2>
<p>Tâm Tín Phát có chứng nhận <b>FSC Chain of Custody</b>: vật liệu FSC được nhận, cất kho, sản xuất và khai báo riêng trên chứng từ. Đáp ứng yêu cầu nguồn gốc giấy bền vững của khách hàng châu Âu, Mỹ và nhà máy FDI.</p>{code}
<div class="hero-cta"><a class="btn btn-green" href="tem-nhan-giay-fsc.html">Xem tem nhãn FSC</a><a class="btn btn-line" href="chung-nhan-fsc-coc-la-gi.html">FSC CoC là gì?</a></div>{note}</div>
</div></section>'''

def img(name, alt, w=960, h=1200, cls="", eager=False):
    return f'<img class="{cls}" src="img/{name}.webp" alt="{e(alt)}" width="{w}" height="{h}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async">'

def gallery(items, gid):
    figs = "".join(f'<figure>{img(n, a)}<figcaption>{e(a)}</figcaption></figure>' for n, a in items)
    return f'''<div class="gal-wrap"><div class="gal" id="{gid}" tabindex="0" aria-label="Ảnh thật tại kho">{figs}</div>
<div class="gal-nav"><button type="button" class="gbtn" data-g="{gid}" data-d="-1" aria-label="Ảnh trước">‹</button><button type="button" class="gbtn" data-g="{gid}" data-d="1" aria-label="Ảnh sau">›</button></div></div>'''

def chips_filter(filters, target):
    btns = '<button type="button" class="fchip on" data-f="all">Tất cả</button>' + "".join(f'<button type="button" class="fchip" data-f="{k}">{e(n)}</button>' for k, n in filters)
    return f'<div class="filters" data-target="{target}" role="group" aria-label="Lọc sản phẩm">{btns}<input class="fsearch" type="search" placeholder="Tìm mã, kích thước…" aria-label="Tìm sản phẩm"></div>'

def group_page(g):
    s = SITE
    if g["slug"] == "san-pham-tem-be-trang":
        rows = "".join(f'<tr data-g="{grp}"><td data-l="Mã"><b>{e(m)}</b></td><td data-l="Sản phẩm">{e(n)}</td><td data-l="Kích thước (mm)" class="nw">{e(kt)}</td><td data-l="Cuộn" class="nw">{e(c)}</td><td data-l="Tem/hàng">{e(t)}</td><td data-l="Đóng gói" class="nw">{e(dg)}</td><td data-l="Dùng cho">{e(u)}</td><td data-l="Tình trạng"><span class="st">Có sẵn</span></td></tr>' for m, grp, n, kt, c, t, dg, st, u in WHITE)
        mats = "".join(f"<tr><td data-l='Chất liệu'><b>{e(a)}</b></td><td data-l='Đặc tính'>{e(b_)}</td><td data-l='Hợp với'>{e(c)}</td></tr>" for a, b_, c in MATERIALS)
        main = f'''<section class="band"><div class="wrap">
<div class="head"><h2>Ảnh thật tại kho</h2><p class="muted">Hàng chụp trực tiếp tại kho Tâm Tín Phát, không dùng ảnh mạng. Vuốt ngang để xem thêm.</p></div>
{gallery(PHOTOS_WHITE, "galw")}
<div class="poster-row"><div>{img("poster-giay-in-nhiet", "Các quy cách giấy in nhiệt A6, A7, 35x22, K80", 843, 1264)}</div>
<div><h2>Quy cách bán chạy</h2><ul class="ticks lt"><li>{IC["check"]}<span><b>A6 cuộn</b> 100×150, 350 tem/cuộn</span></li><li>{IC["check"]}<span><b>A6 xấp</b> 100×150, 500 tem/xấp</span></li><li>{IC["check"]}<span><b>A7 cuộn</b> 75×100, 300 tem/cuộn</span></li><li>{IC["check"]}<span><b>A7 xấp</b> 75×100 hoặc 75×105, 500 tem/xấp</span></li><li>{IC["check"]}<span><b>35×22</b> cuộn 25–30 m, 2 tem/hàng, <b class="price">20.000đ/cuộn</b> (bán lẻ)</span></li><li>{IC["check"]}<span><b>Giấy in bill K80</b> Ø45 đến Ø80</span></li><li>{IC["check"]}<span><b>Bảo hành nhiệt 6 tháng</b> cho decal nhiệt, bảo quản nơi khô ráo</span></li></ul>
<p class="muted">Lưu ý: số 350 trong "100×150×350" là số tem trên cuộn, không phải đường kính cuộn.</p>
<a class="btn btn-red" href="tel:{s["hotline_raw"]}">{IC["phone"]} Gọi lấy giá sỉ</a></div></div>
<div class="head" style="margin-top:clamp(40px,6vw,72px)"><h2>Bảng mã tem bế trắng có sẵn</h2><p class="muted">{len(WHITE)} mã hàng có sẵn tại kho. Lọc theo nhóm hoặc gõ kích thước, ví dụ "50 × 30".</p></div>
{chips_filter(WHITE_FILTERS, "tblw")}
<div class="scroll"><table class="cat-tbl stack" id="tblw"><thead><tr><th>Mã</th><th>Sản phẩm</th><th>Kích thước (mm)</th><th>Cuộn</th><th>Tem/hàng</th><th>Đóng gói</th><th>Dùng cho</th><th>Tình trạng</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted" style="font-size:14px;margin-top:10px">Decal nhiệt 35×22×30 m giá bán lẻ 20.000đ/cuộn. Decal nhiệt bảo hành nhiệt 6 tháng. Giá sỉ thay đổi theo số lượng thùng, gọi {s["hotline"]} để nhận giá.</p></div></section>
<section class="band" style="padding-top:0"><div class="wrap two">
<div><h2>Không thấy kích thước cần tìm?</h2><p class="muted">Xưởng bế theo mọi kích thước, khổ bế tối đa 330 mm, đơn từ 5–10 cuộn. Các khổ thị trường hay đặt:</p><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in BESPOKE)}</ul></div>
<div><h2>Chất liệu decal</h2><p class="muted">Phôi decal từ các hãng lớn như Avery Dennison, UPM Raflatac.</p><div class="scroll"><table class="spec stack"><thead><tr><th>Chất liệu</th><th>Đặc tính</th><th>Hợp với</th></tr></thead><tbody>{mats}</tbody></table></div></div>
</div></section>'''
    elif g["slug"] == "san-pham-tem-mau":
        rows = "".join(f'<tr><td data-l="Loại tem"><a href="{lk}.html"><b>{e(a)}</b></a></td><td data-l="Chất liệu">{e(b_)}</td><td data-l="Kích thước hay dùng">{e(c)}</td><td data-l="Hoàn thiện">{e(d)}</td></tr>' for a, b_, c, d, lk in COLOR_TYPES)
        opts = "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in COLOR_OPTIONS)
        swatch = "".join(f'<span class="sw" style="background:{c}" title="{n}"></span>' for c, n in [("#00a3e0","Cyan"),("#e6007e","Magenta"),("#ffe600","Yellow"),("#1d1d1b","Black"),("#a3121d","Pantone đỏ"),("#1f7a4d","Pantone xanh lá"),("#f5b70a","Pantone vàng"),("#c0c6cc","Xi bạc")])
        main = f'''<section class="band"><div class="wrap">
<div class="banner">{img("banner-tem-nhan", "Tem vận chuyển, tem trà sữa, tem mỹ phẩm, tem bảo hành – Tâm Tín Phát", 1376, 768)}</div>
<div class="head"><h2>Các loại tem màu đang dùng trên thị trường</h2><p class="muted">{len(COLOR_TYPES)} loại tem màu khách hay đặt. Bấm tên tem để xem chi tiết từng dòng.</p></div>
<div class="scroll"><table class="cat-tbl stack"><thead><tr><th>Loại tem</th><th>Chất liệu khuyên dùng</th><th>Kích thước hay dùng</th><th>Hoàn thiện</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
<section class="band" style="padding-top:0"><div class="wrap two">
<div><h2>Tùy chọn màu và hoàn thiện</h2><div class="sws">{swatch}</div><div class="scroll"><table class="spec"><tbody>{opts}</tbody></table></div></div>
<div><h2>Cách đặt tem màu</h2><ol class="prose"><li>Gửi logo, nội dung, kích thước qua Zalo {s["zalo_num"]}.</li><li>Xưởng tư vấn chất liệu, số màu, báo giá.</li><li>Duyệt layout, in mẫu thử nhanh trên máy Ricoh nếu cần xem màu.</li><li>In, cán màng, bế và giao tận nơi.</li></ol></div>
</div></section>'''
    else:
        specs = {m.replace("GoDEX ", ""): (dpi, ki, sp, kh, nt) for m, grp, dpi, ki, sp, kh, nt, u, ph in GODEX}
        def spec_for(name):
            for k in sorted(specs, key=len, reverse=True):
                if re.search(r"(?<![A-Za-z0-9])" + re.escape(k) + r"(?=$|[\s(])", name, re.I):
                    return specs[k]
            return None
        listed = " ".join(n for n, *_ in GITEMS)
        extra = [(m, None, "Liên hệ", None, grp) for m, grp, *_ in GODEX if m.replace("GoDEX ", "").lower() not in listed.lower()]
        def card(n, url_, price, im, grp):
            sp_ = spec_for(n) if grp != "pk" else None
            rows = f'<ul class="kv"><li><span>Độ phân giải</span><b>{e(sp_[0])}</b></li><li><span>Kiểu in</span><b>{e(sp_[1])}</b></li><li><span>Tốc độ in</span><b>{e(sp_[2])}</b></li><li><span>Khổ in tối đa</span><b>{e(sp_[3])}</b></li></ul>' if sp_ else ""
            mdl = (re.split(r"(?i)godex", n)[-1].strip() or n)[:22]
            pic = f'<div class="pic">{printer_svg(grp, model=mdl)}' + (f'<img src="{e(("img/godex/" + im.rsplit("/", 1)[-1]) if LOCAL_GODEX else im)}" alt="{e(n)}" loading="lazy" decoding="async" width="600" height="600" onerror="this.remove()">' if im else "") + "</div>"
            more = f'<a class="btn btn-line sm" href="{e(url_)}" rel="noopener">Thông số đầy đủ</a>' if url_ else ""
            return f'<article class="dev" data-g="{grp}">{pic}<div class="txt"><h3>{e(n)}</h3><p class="price">{e(price)}</p>{rows}<div class="dev-acts">{more}<a class="btn btn-red sm" href="tel:{s["hotline_raw"]}">Hỏi giá</a></div></div></article>'
        cards = "".join(card(*it) for it in GITEMS) + "".join(card(*it) for it in extra)
        total = len(GITEMS) + len(extra)
        sup = "".join(f"<tr><td data-l='Vật tư'><b>{e(a)}</b></td><td data-l='Đặc điểm'>{e(b_)}</td><td data-l='Dùng cho'>{e(c)}</td></tr>" for a, b_, c in SUPPLIES)
        main = f'''<section class="band"><div class="wrap">
<div class="head"><h2>Toàn bộ sản phẩm GoDEX</h2><p class="muted">{total} sản phẩm: máy in, máy RFID, giải pháp tự động, đầu in và phụ kiện. Máy 203 dpi cho tem thông thường, 300 dpi cho chữ nhỏ, 600 dpi cho tem linh kiện.</p></div>
{chips_filter(GFILTERS, "devs")}
<div class="devs" id="devs">{cards}</div></div></section>
<section class="band" style="padding-top:0"><div class="wrap two">
<div><h2>Ruy băng mực, đầu in, linh kiện</h2><div class="scroll"><table class="spec stack"><thead><tr><th>Vật tư</th><th>Đặc điểm</th><th>Dùng cho</th></tr></thead><tbody>{sup}</tbody></table></div></div>
<div><h2>Bảo hành và giao hàng</h2><ul class="ticks lt"><li>{IC["check"]}<span>Bảo hành máy 12 tháng; đầu in 6 tháng (không bảo hành đầu in trầy xước do in hoặc hư do cháy nổ).</span></li><li>{IC["check"]}<span>Adapter và linh phụ kiện bảo hành theo tiêu chuẩn của hãng.</span></li><li>{IC["check"]}<span>Miễn phí giao hàng trong bán kính 5 km hoặc hóa đơn trên 3.000.000đ.</span></li><li>{IC["check"]}<span>Hướng dẫn cài đặt, thiết kế tem bằng phần mềm GoLabel miễn phí.</span></li></ul>
<p class="muted">Thiết bị GoDEX do Công ty TNHH TMDV Nam Nguyễn phân phối. Xem thêm tại <a href="https://namnguyeninfotech.com" rel="noopener">namnguyeninfotech.com</a>.</p></div>
</div></section>'''
    sub_cats = [c for c in CATS if c["slug"] in g["cats"]]
    more = f'<section class="band" style="padding-top:0"><div class="wrap"><div class="head"><h2>Xem chi tiết từng dòng</h2></div><div class="cats">{"".join(cat_card(c) for c in sub_cats)}</div></div></section>' if sub_cats else ""
    pic = {"godex": printer_svg("ban", model="GoDEX"), "trang": img("thung-cuon-decal", "Decal nhiệt cuộn tại kho Tâm Tín Phát", 960, 1200, "cover", True),
           "mau": img("banner-tem-nhan", "Các loại tem nhãn in màu Tâm Tín Phát", 1376, 768, "cover", True)}[g["kind"]]
    body = f'''<section class="phero"><div class="wrap pgrid"><div>
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Trang chủ</a><span>/</span><a href="index.html#danh-muc">Sản phẩm</a><span>/</span><span>{e(g["name"])}</span></nav>
<h1>{e(g["h1"])}</h1><p class="lead">{e(g["lead"])}</p>
<div class="hero-cta"><a class="btn btn-gold" href="tel:{s["hotline_raw"]}">{IC["phone"]} {s["hotline"]}</a><a class="btn btn-line" style="color:#fff" href="{s["zalo"]}">Zalo {s["zalo_num"]}</a></div></div>
<div class="pic">{pic}</div></div></section>
<nav class="gtabs"><div class="wrap">{"".join(f'<a href="{x["slug"]}.html"{" aria-current=page" if x is g else ""}>{e(x["name"])}</a>' for x in GROUPS)}</div></nav>
{main}{more}{contact_band()}'''
    sch = [org_schema(), crumbs_schema([("Trang chủ", "index.html"), (g["name"], g["slug"] + ".html")])]
    if g["slug"] == "thiet-bi-godex":
        def offer(p):
            d = re.sub(r"[^0-9]", "", p)
            return {"offers": {"@type": "Offer", "price": d, "priceCurrency": "VND", "availability": "https://schema.org/InStock"}} if d else {}
        sch.append({"@context": "https://schema.org", "@type": "ItemList", "name": "Sản phẩm GoDEX",
                    "itemListElement": [{"@type": "ListItem", "position": i+1, "item": dict({"@type": "Product", "name": n, "brand": {"@type": "Brand", "name": "GoDEX"}, "image": im, "url": u_}, **offer(p))} for i, (n, u_, p, im, g) in enumerate(GITEMS)]})
    write(g["slug"] + ".html", head(g["title"], g["desc"], g["slug"] + ".html", sch) + body + foot())

# ---------- pages ----------
def home():
    s = SITE
    order = ["tem-nhan-trang", "decal-vo-tem-bao-hanh", "decal-nhua-decal-trong", "tem-nhan-mau", "tem-nhan-theo-nganh", "giay-in-nhiet-giay-in-bill"]
    bigs = {"tem-nhan-trang", "tem-nhan-mau", "tem-nhan-theo-nganh"}
    cats = "".join(cat_card(next(c for c in CATS if c["slug"] == k), k in bigs) for k in order)
    fsc_strip = f'<span>{IC["check"]} Có chứng nhận FSC CoC</span>' if FSC_ON else ""
    steps = [("Gửi kích thước hoặc file", "Qua Zalo, form hoặc gọi điện. Chưa có file cũng được."),
             ("Duyệt layout", "Xưởng dựng bản layout để anh/chị duyệt nội dung, màu, kích thước trước khi in."),
             ("In, cán màng, bế", "In 5–6 màu trên dây chuyền xưởng, cán màng và bế đúng hình."),
             ("Giao tận nơi", "Giao nội thành TP.HCM, gửi xe đi tỉnh theo yêu cầu.")]
    body = f'''<section class="hero"><div class="wrap">
<div class="hero-grid"><div>
<h1>In tem nhãn đẹp, <b>chuẩn xưởng</b>, nhận cả đơn nhỏ</h1>
<p class="lead">Tâm Tín Phát là xưởng in tem nhãn tại Bình Chánh, TP.HCM: tem bế trắng, tem in màu, decal vỡ, decal nhựa, giấy in nhiệt. Anh/chị gửi kích thước, xưởng lo phần còn lại.</p>
<div class="hero-cta"><a class="btn btn-gold" href="tel:{s["hotline_raw"]}">{IC["phone"]} Gọi {s["hotline"]}</a><a class="btn btn-line" href="{s["zalo"]}">Gửi file qua Zalo</a></div>
</div>
<ul class="facts"><li><b>ISO 9001:2015</b><span>Quy trình sản xuất được chứng nhận</span></li><li><b>5–6 màu</b><span>In cuộn và in tờ</span></li><li><b>Từ 5 cuộn</b><span>Nhận đơn số lượng nhỏ</span></li><li><b>~100 người</b><span>Đội ngũ xưởng và kỹ thuật</span></li></ul>
</div></div>
<div class="roll">{hero_svg()}</div></section>
<div class="strip"><div class="wrap"><span>{IC["check"]} Duyệt layout trước khi in</span><span>{IC["check"]} Cán màng bóng / mờ</span><span>{IC["check"]} Bế theo mọi hình</span><span>{IC["check"]} Tem cuộn hợp mọi máy in mã vạch</span>{fsc_strip}</div></div>
<section class="band" id="danh-muc"><div class="wrap">
<div class="head"><h2>3 nhóm sản phẩm chính</h2><p class="muted">Tem bế trắng có sẵn hàng trăm cuộn mỗi mã, tem màu in theo yêu cầu, và máy in GoDEX để in tem ngay tại cửa hàng, nhà máy.</p></div>
<div class="cats" style="margin-bottom:clamp(40px,6vw,72px)">{"".join(group_card(g) for g in GROUPS)}</div>
<div class="head"><h2>Chọn loại tem anh/chị cần</h2><p class="muted">Sáu nhóm sản phẩm xưởng làm hằng ngày. Bấm vào từng nhóm để xem chất liệu, quy cách và câu hỏi hay gặp.</p></div>
<div class="cats">{cats}</div></div></section>
<section class="band" style="padding-top:0"><div class="wrap">
<div class="head"><h2>Đặt in trong 4 bước</h2><p class="muted">Không cần rành kỹ thuật in. Anh/chị chỉ cần biết tem dán vào đâu và cần bao nhiêu.</p></div>
<ol class="route">{"".join(f"<li>{STEP_IC[i]}<h3>{e(t)}</h3><p>{e(d)}</p></li>" for i, (t, d) in enumerate(steps))}</ol></div></section>
<section class="band dark"><div class="wrap vgrid">
{video_block({"cap": "Một ngày ở xưởng in Tâm Tín Phát", "yt": s.get("home_video", "")}, "Xưởng in Tâm Tín Phát")}
<div><h2>Xem tem được in ra như thế nào</h2><p class="muted">Clip quay thật tại xưởng, cập nhật mỗi tuần: từ cuộn decal trắng tới con tem hoàn chỉnh.</p>
<ul class="ticks"><li>{IC["check"]}<span>Dây chuyền in letterpress nhiều màu</span></li><li>{IC["check"]}<span>Máy in nhanh Ricoh cho mẫu thử</span></li><li>{IC["check"]}<span>Bế, xả cuộn và kiểm từng cuộn trước khi giao</span></li></ul>
<a class="btn btn-gold" href="gioi-thieu.html">Tìm hiểu xưởng</a></div></div></section>
<section class="band"><div class="wrap">
<div class="head"><h2>Cẩm nang tem nhãn</h2><a class="go" href="bai-viet.html">Tất cả bài viết {IC["arrow"]}</a></div>
<div class="posts">{"".join(post_card(p) for p in POSTS)}</div></div></section>
{fsc_band()}
{contact_band()}'''
    write("index.html", head("In tem nhãn, decal, tem mã vạch giá xưởng tại TP.HCM | Tâm Tín Phát",
                             "Xưởng in tem nhãn Tâm Tín Phát (Bình Chánh, TP.HCM): tem bế trắng, tem in màu 5–6 màu, decal vỡ, decal nhựa, giấy in nhiệt. ISO 9001:2015, nhận đơn từ 5 cuộn.",
                             "index.html", [org_schema(), {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["brand"], "url": BASE + "/", "inLanguage": "vi"}]) + body + foot())

CAT_PHOTO = {
    "tem-nhan-trang": img("tem-2-hang-thuoc-do", "Tem nhãn trắng 35x22, 2 tem mỗi hàng", 960, 1200, "cover", True),
    "giay-in-nhiet-giay-in-bill": img("nhiet-lien-tuc-76", "Cuộn giấy decal nhiệt liên tục khổ 76", 960, 1200, "cover", True),
}
CAT_BANNER = {
    "giay-in-nhiet-giay-in-bill": f'<section class="band" style="padding-bottom:0"><div class="wrap banner">{img("banner-giay-k80", "Giấy in nhiệt K80 cuộn nhỏ và cuộn lớn", 1376, 768)}</div></section>',
}

def group_crumb(c):
    g = next((g for g in GROUPS if c["slug"] in g["cats"]), None)
    return f'<a href="{g["slug"]}.html">{e(g["name"])}</a><span>/</span>' if g else '<a href="index.html#danh-muc">Sản phẩm</a><span>/</span>'

def cat_page(c):
    rel = [p for p in POSTS if p["cat"] == c["slug"]] or POSTS[:2]
    others = [x for x in CATS if x["slug"] != c["slug"]][:3]
    spec = "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in c["spec"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in c["faq"])
    body = f'''<section class="phero"><div class="wrap pgrid"><div>
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Trang chủ</a><span>/</span>{group_crumb(c)}<span>{e(c["name"])}</span></nav>
<h1>{e(c["h1"])}</h1><p class="lead">{e(c["lead"])}</p>
<div class="hero-cta"><a class="btn btn-gold" href="tel:{SITE["hotline_raw"]}">{IC["phone"]} {SITE["hotline"]}</a><a class="btn btn-line" style="color:#fff" href="#bao-gia">Nhận báo giá</a></div></div>
<div class="pic">{CAT_PHOTO[c["slug"]] if c["slug"] in CAT_PHOTO else roll_svg(c["kind"], "#fff")}</div></div></section>
{CAT_BANNER.get(c["slug"], "")}
<section class="band"><div class="wrap two">
<div><h2>Quy cách xưởng làm</h2><div class="scroll"><table class="spec"><tbody>{spec}</tbody></table></div></div>
<div><h2>Hay dùng cho</h2><ul class="chips">{"".join(f"<li>{e(u)}</li>" for u in c["uses"])}</ul>
<div class="prose" style="margin-top:22px">{c["body"]}</div></div>
</div></section>
<section class="band dark"><div class="wrap vgrid">{video_block(c["video"], c["name"])}
<div><h2>{e(c["video"]["h"])}</h2><p class="muted">{e(c["video"]["p"])}</p><a class="btn btn-gold" href="#bao-gia">Báo giá {e(c["name"].lower())}</a></div></div></section>
<section class="band"><div class="wrap two">
<div class="faq"><h2>Câu hỏi hay gặp</h2>{faq}</div>
<div><h2>Đọc thêm</h2><div class="posts" style="grid-template-columns:minmax(0,1fr)">{"".join(post_card(p) for p in rel[:2])}</div></div>
</div></section>
<section class="band" style="padding-top:0"><div class="wrap"><div class="head"><h2>Sản phẩm khác</h2></div><div class="cats">{"".join(cat_card(o) for o in others)}</div></div></section>
{contact_band(c["slug"])}'''
    sch = [org_schema(), crumbs_schema([("Trang chủ", "index.html"), (c["name"], c["slug"] + ".html")]), faq_schema(c["faq"]),
           {"@context": "https://schema.org", "@type": "Service", "name": c["name"], "serviceType": c["name"], "provider": {"@id": BASE + "/#xuong"}, "areaServed": "VN", "description": c["lead"], "url": url(c["slug"] + ".html")}]
    write(c["slug"] + ".html", head(c["title"], c["desc"], c["slug"] + ".html", sch) + body + foot())

def post_page(p):
    c = next(x for x in CATS if x["slug"] == p["cat"])
    toc = "".join(f'<li><a href="#{h["id"]}">{e(h["h"])}</a></li>' for h in p["sections"])
    secs = "".join(f'<h2 id="{h["id"]}">{e(h["h"])}</h2>{h["html"]}' for h in p["sections"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    others = [x for x in POSTS if x["slug"] != p["slug"]]
    body = f'''<section class="phero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Trang chủ</a><span>/</span><a href="bai-viet.html">Bài viết</a><span>/</span><a href="{c["slug"]}.html">{e(c["name"])}</a></nav>
<h1 style="max-width:22ch">{e(p["title"])}</h1><p class="meta">Xưởng in Tâm Tín Phát · <time datetime="{p["date"]}">{p["date_vn"]}</time> · {p["mins"]} phút đọc</p></div></section>
<section class="band"><div class="wrap art-wrap">
<article class="prose">{video_block(p["video"], p["title"])}<p style="margin-top:22px"><b>{e(p["intro"])}</b></p>{secs}
<h2 id="hoi-dap">Hỏi nhanh – đáp gọn</h2><div class="faq">{faq}</div>
<div class="cta-box"><h3>{e(p["cta"])}</h3><p>Gửi kích thước và số lượng, xưởng báo giá và gửi layout duyệt trước khi in.</p><div><a class="btn btn-gold" href="tel:{SITE["hotline_raw"]}">{IC["phone"]} {SITE["hotline"]}</a><a class="btn btn-line" href="{SITE["zalo"]}">Zalo {SITE["zalo_num"]}</a></div></div>
</article>
<aside class="toc"><b>Trong bài</b><ol>{toc}<li><a href="#hoi-dap">Hỏi đáp</a></li></ol>
<p style="margin:16px 0 8px"><b>Sản phẩm liên quan</b></p><a class="go" href="{c["slug"]}.html">{e(c["name"])} {IC["arrow"]}</a></aside>
</div></section>
<section class="band" style="padding-top:0"><div class="wrap"><div class="head"><h2>Bài viết khác</h2></div><div class="posts">{"".join(post_card(o) for o in others)}</div></div></section>'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"],
           "inLanguage": "vi", "author": {"@type": "Organization", "name": SITE["legal"]}, "publisher": {"@id": BASE + "/#xuong"}, "mainEntityOfPage": url(p["slug"] + ".html")}
    sch = [org_schema(), art, crumbs_schema([("Trang chủ", "index.html"), ("Bài viết", "bai-viet.html"), (p["short"], p["slug"] + ".html")]), faq_schema(p["faq"])]
    v = p["video"]
    if v.get("yt"):
        sch.append({"@context": "https://schema.org", "@type": "VideoObject", "name": v["cap"], "description": p["desc"], "uploadDate": p["date"],
                    "thumbnailUrl": f"https://i.ytimg.com/vi/{v['yt']}/hqdefault.jpg", "embedUrl": f"https://www.youtube.com/embed/{v['yt']}"})
    write(p["slug"] + ".html", head(p["seo_title"], p["desc"], p["slug"] + ".html", sch) + body + foot())

def simple(path, title, desc, h1, lead, inner, crumbs_name):
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Trang chủ</a><span>/</span><span>{e(crumbs_name)}</span></nav>
<h1>{e(h1)}</h1><p class="lead">{e(lead)}</p></div></section>{inner}'''
    write(path, head(title, desc, path, [org_schema(), crumbs_schema([("Trang chủ", "index.html"), (crumbs_name, path)])]) + body + foot())

def misc():
    s = SITE
    simple("bai-viet.html", "Cẩm nang tem nhãn, decal, mã vạch | Tâm Tín Phát", "Bài viết hướng dẫn chọn kích thước, chất liệu và cách đặt in tem nhãn, decal, tem mã vạch, có video quay tại xưởng.",
           "Cẩm nang tem nhãn", "Kinh nghiệm chọn tem, chọn chất liệu và đặt in cho đúng, viết từ chính xưởng in. Bài nào cũng có video.",
           f'<section class="band"><div class="wrap"><div class="posts">{"".join(post_card(p) for p in POSTS)}</div></div></section>', "Bài viết")
    simple("lien-he.html", "Liên hệ & bản đồ xưởng in tem nhãn Tâm Tín Phát", f"Liên hệ xưởng in tem nhãn Tâm Tín Phát: {s['address']}. Hotline {s['hotline']}, Zalo {s['zalo_num']}.",
           "Liên hệ xưởng Tâm Tín Phát", f"Gọi {s['hotline']}, nhắn Zalo {s['zalo_num']} hoặc ghé xưởng tại Bình Chánh để xem mẫu thật.", contact_band(), "Liên hệ")
    simple("gioi-thieu.html", "Giới thiệu xưởng in tem nhãn Tâm Tín Phát – ISO 9001:2015", "Tâm Tín Phát là xưởng in tem nhãn tại Bình Chánh, TP.HCM với khoảng 100 nhân sự, đạt ISO 9001:2015, in 5–6 màu dạng cuộn và tờ.",
           "Xưởng in tem nhãn ở Bình Chánh", "Khoảng 100 con người, một việc: làm ra những con tem dán đẹp, bám chắc và đúng hẹn.",
           f'''<section class="band"><div class="wrap two"><div class="prose"><h2>Chúng tôi làm gì</h2><p>{e(s["legal"])} sản xuất tem nhãn, decal, tem mã vạch, giấy in nhiệt và giấy in bill cho mọi ngành hàng. Xưởng in trên hệ thống letterpress nhiều màu, có máy in nhanh Ricoh để in mẫu thử, cán màng và bế hình ngay tại chỗ.</p>
<h2>Vì sao khách chọn xưởng</h2><ul><li>Quy trình đạt chứng nhận ISO 9001:2015.</li><li>In 5–6 màu, dạng cuộn và dạng tờ.</li><li>Nhận đơn từ 5–10 cuộn, phù hợp shop và thương hiệu mới.</li><li>Mỗi đơn đều có layout để khách duyệt trước khi in.</li>{"<li>Có chứng nhận FSC Chain of Custody cho đơn hàng cần vật liệu FSC.</li>" if FSC_ON else ""}</ul></div>
<div>{video_block({"cap": "Bên trong xưởng Tâm Tín Phát", "yt": s.get("home_video", "")}, "Xưởng Tâm Tín Phát")}</div></div></section>{contact_band()}''', "Giới thiệu")
    simple("chinh-sach-bao-mat.html", "Chính sách bảo mật | Tâm Tín Phát", "Chính sách bảo mật thông tin khách hàng của website temnhantamtinphat.com.",
           "Chính sách bảo mật", "Cách chúng tôi thu thập và dùng thông tin anh/chị gửi qua website.",
           f'''<section class="band"><div class="wrap prose"><h2>Thông tin thu thập</h2><p>Khi gửi form báo giá, anh/chị cung cấp họ tên, số điện thoại và nội dung yêu cầu. Website cũng ghi nhận số liệu truy cập ẩn danh (Google Analytics, công cụ quảng cáo) để cải thiện trang.</p>
<h2>Mục đích sử dụng</h2><p>Thông tin chỉ dùng để liên hệ tư vấn, báo giá và chăm sóc đơn hàng. Chúng tôi không bán hay chia sẻ thông tin cho bên thứ ba ngoài mục đích này.</p>
<h2>Lưu trữ và yêu cầu xoá</h2><p>Thông tin được lưu trên hệ thống nội bộ của công ty. Anh/chị có thể yêu cầu xem, sửa hoặc xoá thông tin bằng cách gọi {s["hotline"]} hoặc email {s["email"]}.</p>
<h2>Đơn vị chịu trách nhiệm</h2><p>{e(s["legal"])} – {e(s["address"])}.</p></div></section>''', "Chính sách bảo mật")
    pages = [("index.html", "Trang chủ")] + [(g["slug"] + ".html", g["name"]) for g in GROUPS] + [(c["slug"] + ".html", c["name"]) for c in CATS] + [("bai-viet.html", "Bài viết")] + [(p["slug"] + ".html", p["short"]) for p in POSTS] + [("gioi-thieu.html", "Giới thiệu"), ("lien-he.html", "Liên hệ"), ("chinh-sach-bao-mat.html", "Chính sách bảo mật")]
    simple("so-do-trang.html", "Sơ đồ trang | Tâm Tín Phát", "Danh sách toàn bộ trang trên website temnhantamtinphat.com.", "Sơ đồ trang", "Toàn bộ trang trên website, để anh/chị tìm nhanh.",
           f'<section class="band"><div class="wrap"><ul class="sm-list">{"".join(f"<li><a href=\"{h}\">{e(n)}</a></li>" for h, n in pages)}</ul></div></section>', "Sơ đồ trang")
    return pages

def seo_files(pages):
    pri = {"index.html": "1.0"}
    rows = []
    for h, _ in pages + [("so-do-trang.html", "")]:
        p = pri.get(h, "0.9" if any(h == c["slug"] + ".html" for c in CATS) or any(h == g["slug"] + ".html" for g in GROUPS) else "0.7")
        d = next((x["date"] for x in POSTS if x["slug"] + ".html" == h), SITE["updated"])
        rows.append(f"  <url><loc>{url(h)}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    write("_headers", "/*.css\n  Cache-Control: public, max-age=31536000, immutable\n/*.js\n  Cache-Control: public, max-age=31536000, immutable\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    write("404.html", head("Không tìm thấy trang | Tâm Tín Phát", "Trang không tồn tại.", "404.html") +
          '<section class="phero"><div class="wrap"><h1>Trang này đã bị bế mất</h1><p class="lead">Đường dẫn không còn. Quay lại trang chủ hoặc gọi xưởng nhé.</p><a class="btn btn-gold" href="index.html">Về trang chủ</a></div></section>' + foot())

if __name__ == "__main__":
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ("style.css", "app.js"):
        shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "img"))
    home()
    for c in CATS: cat_page(c)
    for g in GROUPS: group_page(g)
    for p in POSTS: post_page(p)
    pages = misc()
    seo_files(pages)
    print("OK", len(os.listdir(OUT)), "files")
