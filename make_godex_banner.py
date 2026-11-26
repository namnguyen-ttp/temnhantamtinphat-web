# Ghép banner "Máy in mã vạch để bàn GoDEX" từ ảnh sản phẩm thật (chạy sau fetch_godex_images.py)
# Kết quả: src/img/banner-godex.webp (1600x1100) và src/img/banner-godex-vuong.webp (1080x1080, dùng chạy quảng cáo)
import os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from godex_list import ITEMS

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "src", "img")
GDIR = os.path.join(IMG, "godex")
FB = os.path.join(ROOT, "fonts", "Inter-ExtraBold.otf")
FM = os.path.join(ROOT, "fonts", "Inter-SemiBold.otf")
PICK = ["GM630 Pro", "RT863i Pro", "RT730i Pro", "RT700i Pro", "EZ530+", "DT4L", "G500", "GE300 (USB)"]
RED, DARK, GOLD, WHITE = (168, 20, 27), (24, 12, 14), (245, 183, 10), (255, 255, 255)


def model(n):
    return re.split(r"(?i)godex", n)[-1].strip()


def pick_items():
    ban = [it for it in ITEMS if it[4] == "ban" and it[3]]
    out = []
    for p in PICK:
        for it in ban:
            if model(it[0]).lower() == p.lower() and os.path.exists(os.path.join(GDIR, it[3].rsplit("/", 1)[-1])):
                out.append(it); break
    for it in ban:  # bù nếu thiếu ảnh
        if len(out) >= 8: break
        if it not in out and os.path.exists(os.path.join(GDIR, it[3].rsplit("/", 1)[-1])):
            out.append(it)
    return out[:8]


def price_min(items):
    v = [int(re.sub(r"\D", "", p)) for _, _, p, _, g in ITEMS if g == "ban" and re.search(r"\d", p)]
    return min(v) if v else None


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, (0, 0), m)
    return out


def bg(w, h):
    g = Image.new("RGB", (w, h), DARK)
    d = ImageDraw.Draw(g)
    for y in range(h):
        k = y / h
        d.line([(0, y), (w, y)], fill=(int(120 - 70 * k), int(14 - 4 * k), int(20 - 6 * k)))
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse((w * 0.55, -h * 0.4, w * 1.3, h * 0.5), fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    g = Image.composite(Image.new("RGB", (w, h), GOLD), g, glow.point(lambda v: v // 3))
    return g


def tile(it, tw, ph, fb):
    """Thẻ sản phẩm phủ kín khung: nền là chính ảnh phóng to làm mờ, máy in đặt trọn ở giữa (không bị cắt)."""
    src = Image.open(os.path.join(GDIR, it[3].rsplit("/", 1)[-1])).convert("RGB")
    back = ImageOps.fit(src, (tw, ph), Image.LANCZOS).filter(ImageFilter.GaussianBlur(18))
    back = Image.blend(back, Image.new("RGB", back.size, WHITE), 0.25)
    fg = ImageOps.contain(src, (tw, ph), Image.LANCZOS)
    back.paste(fg, ((tw - fg.size[0]) // 2, (ph - fg.size[1]) // 2))
    lab = getattr(fb, "_lab", 56)
    card = Image.new("RGB", (tw, ph + lab), WHITE)
    card.paste(back, (0, 0))
    d = ImageDraw.Draw(card)
    name = model(it[0]).replace(" (USB)", "")
    f = fb
    while d.textlength(name, font=f) > tw - 24 and f.size > 14:
        f = ImageFont.truetype(FB, f.size - 2)
    d.text((tw // 2, ph + lab // 2), name, font=f, fill=DARK, anchor="mm")
    return rounded(card, 22)


def shadow(canvas, box, r=22):
    sh = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((box[0] + 6, box[1] + 12, box[2] + 6, box[3] + 12), r, fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    canvas.paste(Image.new("RGB", canvas.size, (0, 0, 0)), (0, 0), sh)


def make(w, h, cols, out):
    items = pick_items()
    if len(items) < 4:
        print("banner: thiếu ảnh, bỏ qua"); return False
    c = bg(w, h); d = ImageDraw.Draw(c)
    pad = int(w * 0.05)
    big = ImageFont.truetype(FB, int(w * 0.052)); mid = ImageFont.truetype(FM, int(w * 0.024))
    small = ImageFont.truetype(FB, int(w * 0.022)); tagf = ImageFont.truetype(FB, int(w * 0.02))
    # nhãn GoDEX chính hãng
    tag = "GoDEX CHÍNH HÃNG"
    tw = d.textlength(tag, font=tagf)
    d.rounded_rectangle((pad, pad, pad + tw + 36, pad + int(w * 0.042)), 99, fill=GOLD)
    d.text((pad + 18, pad + int(w * 0.021)), tag, font=tagf, fill=DARK, anchor="lm")
    y = pad + int(w * 0.06)
    d.text((pad, y), "Máy in mã vạch để bàn", font=big, fill=WHITE)
    y += int(big.size * 1.25)
    pm = price_min(items)
    sub = ("Giá chỉ từ " + f"{pm:,}".replace(",", ".") + "đ · đã gồm VAT") if pm else "Giá đã gồm VAT"
    d.text((pad, y), sub, font=mid, fill=GOLD)
    y += int(mid.size * 1.9)
    # lưới sản phẩm: trải kín toàn bộ chiều ngang và chiều cao còn lại
    rows = max(1, min(len(items), 8) // cols)  # chỉ lấy hàng đầy, không để ô trống
    foot_h = int(h * 0.11) if h <= w * 1.2 else int(h * 0.075)
    gap = int(w * 0.022)
    avail_h = h - y - foot_h - int(pad * 0.6)
    tw = int((w - 2 * pad - gap * (cols - 1)) / cols)
    th = int((avail_h - gap * (rows - 1)) / rows)
    lab = max(44, int(th * 0.16))
    ph = th - lab
    fb = ImageFont.truetype(FB, max(18, min(int(lab * 0.5), int(tw * 0.09))))
    fb._lab = lab
    for i, it in enumerate(items[: cols * rows]):
        r, k = divmod(i, cols)
        tx, ty = pad + k * (tw + gap), int(y + r * (th + gap))
        t = tile(it, tw, ph, fb)
        shadow(c, (tx, ty, tx + t.size[0], ty + t.size[1]))
        c.paste(t, (tx, ty), t)
    # chân banner
    fy = h - foot_h
    d = ImageDraw.Draw(c)
    d.rectangle((0, fy, w, h), fill=RED)
    d.rectangle((0, fy, w, fy + 6), fill=GOLD)
    left = "Bảo hành thân máy 24 tháng · Freeship đơn từ 3 triệu"
    fl = small
    while d.textlength(left, font=fl) > w * 0.6 and fl.size > 12:
        fl = ImageFont.truetype(FB, fl.size - 1)
    d.text((pad, fy + foot_h // 2 + 3), left, font=fl, fill=WHITE, anchor="lm")
    fh = ImageFont.truetype(FB, int(w * 0.03))
    hot = "0989 139 333"
    hw = d.textlength(hot, font=fh)
    d.rounded_rectangle((w - pad - hw - 40, fy + foot_h * 0.18, w - pad, fy + foot_h * 0.86), 99, fill=GOLD)
    d.text((w - pad - 20, fy + foot_h // 2 + 3), hot, font=fh, fill=DARK, anchor="rm")
    c.save(os.path.join(IMG, out), quality=86, method=6)
    print("banner", out, len(items), "máy")
    return True


if __name__ == "__main__":
    make(1600, 1100, 4, "banner-godex.webp")
    make(1080, 1080, 3, "banner-godex-vuong.webp")
    make(1080, 1920, 2, "banner-godex-dung.webp")  # dọc 9:16, đầy màn hình điện thoại (story/reels)
