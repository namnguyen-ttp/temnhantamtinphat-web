# Tải ảnh sản phẩm GoDEX từ namnguyeninfotech.com về src/img/godex (chạy trong GitHub Actions)
import os, urllib.request
from godex_list import ITEMS
out = os.path.join(os.path.dirname(__file__), "src", "img", "godex")
os.makedirs(out, exist_ok=True)
ok = 0
for n, u, p, im, g in ITEMS:
    dst = os.path.join(out, im.rsplit("/", 1)[-1])
    if os.path.exists(dst):
        ok += 1; continue
    try:
        req = urllib.request.Request(im, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r, open(dst, "wb") as f:
            f.write(r.read())
        ok += 1
    except Exception as ex:
        print("skip", im, ex)
print("downloaded", ok, "/", len(ITEMS))
