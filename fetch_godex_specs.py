# Lấy thông số kỹ thuật từng sản phẩm GoDEX trên namnguyeninfotech.com (chạy trong GitHub Actions)
# Kết quả: godex_specs.json  {slug: "dòng 1\ndòng 2..."}
import json, os, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from godex_list import ITEMS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "godex_specs.json")
BLOCK = ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "br", "ul", "ol", "table")


def text_of(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", "ignore")
    soup = BeautifulSoup(html, "html.parser")
    el = soup.select_one(".entry-detail .contents-text") or soup.select_one(".entry-detail")
    if not el:
        return ""
    for x in el.select("script,style,nav,.ftwp-list,img,iframe"):
        x.decompose()
    for x in el.find_all(BLOCK):
        if x.name == "br":
            x.replace_with("\n")
        else:
            x.insert_before("\n")
            x.insert_after("\n")
    for td in el.find_all(["td", "th"]):
        td.insert_after(" | ")
    lines = []
    for ln in el.get_text().split("\n"):
        ln = re.sub(r"\s+", " ", ln).strip(" |")
        if ln:
            lines.append(ln)
    return "\n".join(lines)


def job(it):
    slug = it[1].rsplit("/", 1)[-1]
    try:
        return slug, text_of(it[1])
    except Exception as ex:
        print("skip", slug, ex)
        return slug, ""


with ThreadPoolExecutor(8) as ex:
    res = dict(ex.map(job, ITEMS))
old = {}
if os.path.exists(OUT):
    old = json.load(open(OUT, encoding="utf-8"))
for k, v in res.items():
    if not v and old.get(k):
        res[k] = old[k]
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("specs", sum(1 for v in res.values() if v), "/", len(res))
