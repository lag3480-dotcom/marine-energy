"""모든 페이지 </head> 앞에 네이버 공통 스크립트(통합 전환추적)를 넣는다. 여러 번 돌려도 같은 결과.
전환: tel: 링크 클릭 = lead(전화 문의), sms: 링크 클릭 = custom001(문자 문의).
페이지 스크립트에서 직접 보낼 땐 window.mrnConv('lead' | 'custom001')."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((root/"src/config.json").read_text(encoding="utf-8"))
WA = cfg.get("NAVER_WA", "")
DOMAIN = re.sub(r"^https?://([^/]+).*$", r"\1", cfg["SITE_URL"])
START, END = "<!-- NAVER_WCS:START -->", "<!-- NAVER_WCS:END -->"
SNIPPET = f"""{START}
<script type="text/javascript" src="//wcs.naver.net/wcslog.js"></script>
<script type="text/javascript">
if (!wcs_add) var wcs_add = {{}};
wcs_add["wa"] = "{WA}";
if (!_nasa) var _nasa = {{}};
if (window.wcs) {{
  wcs.inflow("{DOMAIN}");
  wcs_do();
}}
window.mrnConv = function (type) {{
  try {{ if (window.wcs) {{ var _conv = {{}}; _conv.type = type; wcs.trans(_conv); }} }} catch (e) {{}}
}};
document.addEventListener("click", function (e) {{
  var a = e.target.closest && e.target.closest('a[href^="tel:"],a[href^="sms:"]');
  if (a) window.mrnConv(a.getAttribute("href").indexOf("tel:") === 0 ? "lead" : "custom001");
}}, true);
</script>
{END}
"""

def inject(s):
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    s = s.replace("<!-- NAVER_WCS: 네이버 광고 공통 스크립트 자리 -->\n", "")
    return s.replace("</head>", SNIPPET + "</head>", 1) if WA else s

def apply_all():
    n = 0
    for p in root.rglob("*.html"):
        if any(part.startswith((".", "_")) for part in p.relative_to(root).parts) or p.name == "preview.html":
            continue
        s = p.read_text(encoding="utf-8"); t = inject(s)
        if t != s: p.write_text(t, encoding="utf-8"); n += 1
    print("naver wcs:", n, "files updated")

if __name__ == "__main__":
    apply_all()
