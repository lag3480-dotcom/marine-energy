"""src/page.html + src/config.json -> index.html (배포용), preview.html (미리보기용 조각)."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((root/"src/config.json").read_text(encoding="utf-8"))
page = (root/"src/page.html").read_text(encoding="utf-8")
for k, v in cfg.items():
    page = page.replace(f"__{k}__", v)
title, rest = page.split("\n", 1)
head = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<meta name="description" content="부산·경남 식당·업소용 가스공사. 신규 오픈 매장 가스배관, 업소용 가스레인지 설치·교체, 기구 추가·이전. 가정집 이사 도시가스 연결은 하지 않습니다. 가스시설시공업 등록업체 마린에너지 {cfg['PHONE']}">
<link rel="canonical" href="{cfg['SITE_URL']}">
<meta property="og:type" content="website">
<meta property="og:title" content="마린에너지 | 부산 식당 가스공사">
<meta property="og:description" content="식당·업소 전용 가스시설 공사. 부산·경남.">
<meta property="og:url" content="{cfg['SITE_URL']}">
<!-- NAVER_VERIFY: 네이버 서치어드바이저 소유확인 메타태그 자리 -->
<!-- NAVER_WCS: 네이버 광고 공통 스크립트 자리 -->
"""
out = head + rest.split("<style>",1)[0] + "<style>" + rest.split("<style>",1)[1].split("</style>",1)[0] + "</style>\n</head>\n<body>\n" + rest.split("</style>",1)[1] + "\n</body>\n</html>\n"
(root/"index.html").write_text(out, encoding="utf-8")
(root/"preview.html").write_text(page, encoding="utf-8")
print("built", len(out))
