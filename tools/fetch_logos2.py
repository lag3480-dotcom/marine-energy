"""위키미디어 공용에서 검색어로 로고 파일을 찾아 받는다."""
import json, pathlib, time, urllib.parse, urllib.request
root = pathlib.Path(__file__).resolve().parent.parent
out = root/"assets/logos/_candidates"; out.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "marine-energy-site/1.0 (https://github.com/lag3480-dotcom/marine-energy)"}
def get(url, tries=4):
    for t in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10*(t+1)); continue
            raise
Q = {"lotte": ["Lotte Department Store logo", "Lotte logo", "Lotte Outlets logo"],
     "bonjuk": ["Bonjuk logo", "본죽 로고", "Bon IF logo"],
     "shinhwa": ["Jeju Shinhwa World logo", "Shinhwa World"],
     "renault-samsung": ["Renault Samsung Motors logo"]}
rep = []
for slug, qs in Q.items():
    n = 0
    for q in qs:
        time.sleep(2)
        p = urllib.parse.urlencode({"action":"query","list":"search","srsearch":q,"srnamespace":"6","srlimit":"8","format":"json"})
        try:
            res = json.loads(get("https://commons.wikimedia.org/w/api.php?"+p))["query"]["search"]
        except Exception as e:
            rep.append(f"{slug}\t{q}\terror {e}"); continue
        titles = [r["title"].split(":",1)[1] for r in res]
        rep.append(f"{slug}\t{q}\t{titles}")
        for f in [t for t in titles if "logo" in t.lower() or "로고" in t][:3]:
            time.sleep(2)
            try:
                data = get("https://commons.wikimedia.org/wiki/Special:FilePath/"+urllib.parse.quote(f.replace(" ","_"))+"?width=480")
                ext = ".png" if data[:4]==b"\x89PNG" else ".jpg" if data[:2]==b"\xff\xd8" else ".bin"
                name = f"{slug}__s{n}{ext}"; n += 1
                (out/name).write_bytes(data); rep.append(f"{slug}\t\t{name}\t{f}")
            except Exception as e:
                rep.append(f"{slug}\t{f}\terror {e}")
(out/"report2.tsv").write_text("\n".join(rep)+"\n", encoding="utf-8"); print("\n".join(rep))
