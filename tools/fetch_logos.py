"""위키백과 문서에 쓰인 이미지 중 로고로 보이는 파일을 PNG로 받아 assets/logos/_candidates/ 에 저장."""
import json, pathlib, re, time, urllib.parse, urllib.request
root = pathlib.Path(__file__).resolve().parent.parent
out = root/"assets/logos/_candidates"; out.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "marine-energy-site/1.0 (https://github.com/lag3480-dotcom/marine-energy)"}
LOGO = re.compile(r"logo|로고|\bci\b|_ci|ci_|wordmark|emblem|symbol|심볼|bi\b", re.I)
def get(url, tries=4):
    for t in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10*(t+1)); continue
            raise
    raise RuntimeError("429 repeated")
report = []
for line in (root/"tools/logos.txt").read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"): continue
    slug, cands = line.split("|"); n = 0
    for c in cands.split(","):
        lang, title = c.split(":", 1)
        time.sleep(2)
        try:
            q = urllib.parse.urlencode({"action":"query","prop":"images","titles":title,"imlimit":"100","format":"json","redirects":"1"})
            pages = json.loads(get(f"https://{lang}.wikipedia.org/w/api.php?{q}"))["query"].get("pages", {})
            files = [im["title"].split(":",1)[1] for p in pages.values() for im in p.get("images", [])]
            hits = [f for f in files if LOGO.search(f)]
            report.append(f"{slug}\t{c}\tfiles={len(files)}\tlogo-like={hits}")
            for f in hits[:4]:
                time.sleep(2)
                url = f"https://{lang}.wikipedia.org/wiki/Special:FilePath/" + urllib.parse.quote(f.replace(" ","_")) + "?width=480"
                data = get(url)
                ext = ".png" if data[:4] == b"\x89PNG" else (".jpg" if data[:2] == b"\xff\xd8" else ".svg" if b"<svg" in data[:500] else ".bin")
                name = f"{slug}__{n}{ext}"; n += 1
                (out/name).write_bytes(data)
                report.append(f"{slug}\t\t{name}\t{f}")
        except Exception as e:
            report.append(f"{slug}\t{c}\terror {e}")
(out/"report.tsv").write_text("\n".join(report)+"\n", encoding="utf-8")
print("\n".join(report))
