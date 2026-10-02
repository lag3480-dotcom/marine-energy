"""위키백과 요약 API에서 각 브랜드 대표 이미지(대개 로고)를 받아 assets/logos/_candidates/ 에 저장."""
import json, os, pathlib, urllib.parse, urllib.request
root = pathlib.Path(__file__).resolve().parent.parent
out = root/"assets/logos/_candidates"; out.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "marine-energy-site/1.0 (github.com/lag3480-dotcom/marine-energy)"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
report = []
for line in (root/"tools/logos.txt").read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"): continue
    slug, cands = line.split("|")
    for i, c in enumerate(cands.split(",")):
        lang, title = c.split(":", 1)
        try:
            j = json.loads(get(f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title.replace(" ", "_"))))
            img = (j.get("originalimage") or j.get("thumbnail") or {}).get("source")
            if not img: report.append(f"{slug}\t{c}\tno image"); continue
            ext = os.path.splitext(urllib.parse.urlparse(img).path)[1].lower() or ".img"
            name = f"{slug}__{i}{ext}"
            (out/name).write_bytes(get(img))
            report.append(f"{slug}\t{c}\t{name}\t{img}")
        except Exception as e:
            report.append(f"{slug}\t{c}\terror {e}")
(out/"report.tsv").write_text("\n".join(report)+"\n", encoding="utf-8")
print("\n".join(report))
