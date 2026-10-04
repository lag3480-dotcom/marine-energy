"""blog/_src/*.json -> blog/<slug>/index.html, blog/index.html 목록, sitemap.xml, robots.txt.
글 하나 = JSON 하나: slug, title, description, date(YYYY-MM-DD), region, body(HTML)."""
import json, pathlib, html, re
root = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((root/"src/config.json").read_text(encoding="utf-8"))
SITE = cfg["SITE_URL"].rstrip("/") + "/"
posts = sorted((json.loads(p.read_text(encoding="utf-8")) for p in (root/"blog/_src").glob("*.json")),
               key=lambda p: p["date"], reverse=True)

STYLE = (root/"blog/index.html").read_text(encoding="utf-8").split("<style>",1)[1].split("</style>",1)[0]
POST_STYLE = """
article h2{font:400 1.45rem/1.4 "Black Han Sans",sans-serif;margin:36px 0 8px}
article h3{font-size:1.1rem;margin:28px 0 6px}
article .meta{color:var(--steel);font-size:.9rem}
article ul,article ol{padding-left:1.3em}
.cta{background:var(--ink);color:#fff;padding:22px;border-left:8px solid var(--pipe);margin:40px 0}
.cta a{display:inline-block;margin:10px 10px 0 0;padding:12px 18px;background:var(--pipe);color:var(--ink);font-weight:700;text-decoration:none}
.cta a.alt{background:#fff}
.more{margin:0 0 60px}
"""

def head(title, desc, url, extra=""):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=IBM+Plex+Sans+KR:wght@400;700&display=swap">
<style>{STYLE}{POST_STYLE}</style>
{extra}</head>
<body>
"""

def cta():
    return f"""<aside class="cta"><strong>공사 날짜가 정해졌다면 연락 주세요.</strong><br>
현장 작업 중에는 통화가 어려울 수 있어요. 문자로 현장 사진을 보내주시면 작업 끝나는 대로 연락드립니다.<br>
<a href="tel:{cfg['PHONE_TEL']}">전화 {cfg['PHONE']}</a><a class="alt" href="sms:{cfg['PHONE_TEL']}">문자로 사진 보내기</a></aside>"""

for p in posts:
    url = f"{SITE}blog/{p['slug']}/"
    ld = json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":p["title"],
        "description":p["description"],"datePublished":p["date"],"mainEntityOfPage":url,
        "author":{"@type":"Organization","name":"마린에너지"},
        "publisher":{"@type":"Organization","name":"마린에너지"}}, ensure_ascii=False)
    out = head(p["title"]+" | 마린에너지", p["description"], url, f'<script type="application/ld+json">{ld}</script>\n')
    out += f"""<header><div class="wrap"><a class="brand" href="../../">마린에너지</a><a href="../../#ask">견적 문의</a></div></header>
<main class="wrap"><article>
<h1>{html.escape(p['title'])}</h1>
<p class="meta"><time datetime="{p['date']}">{p['date'].replace('-','.')}</time> · {html.escape(p['region'])}</p>
{p['body']}
{cta()}
</article>
<p class="more"><a href="../">← 현장 기록 전체 보기</a> · <a href="../../">마린에너지 홈</a></p>
</main>
</body>
</html>
"""
    d = root/"blog"/p["slug"]; d.mkdir(exist_ok=True)
    (d/"index.html").write_text(out, encoding="utf-8")

idx = (root/"blog/index.html").read_text(encoding="utf-8")
items = "\n".join(f'<li><a href="{p["slug"]}/">{html.escape(p["title"])}</a><time datetime="{p["date"]}">{p["date"].replace("-",".")} · {html.escape(p["region"])}</time></li>' for p in posts)
idx = re.sub(r"(<!-- POSTS:START.*?-->).*?(<!-- POSTS:END -->)",
             lambda m: f'{m.group(1)}\n<ul class="posts">\n{items}\n</ul>\n{m.group(2)}', idx, flags=re.S)
if posts:
    idx = idx.replace('<p class="empty">', '<p class="lead">')
(root/"blog/index.html").write_text(idx, encoding="utf-8")

urls = [SITE, SITE+"blog/"] + [f"{SITE}blog/{p['slug']}/" for p in posts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     "\n".join(f"<url><loc>{u}</loc></url>" for u in urls) + "\n</urlset>\n"
(root/"sitemap.xml").write_text(sm, encoding="utf-8")
(root/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
print(f"published {len(posts)} posts")
