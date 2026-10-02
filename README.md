# 마린에너지 홈페이지

- `index.html` : 랜딩페이지 (네이버 파워링크 도착 페이지). 직접 고치지 말고 `src/page.html`, `src/config.json` 수정 후 `python3 src/build.py`.
- `src/config.json` : 전화번호, 카톡 채널 링크, 대표자명, 사업자번호, 면허번호, 주소, 사이트 주소.
- `blog/` : 현장 기록(블로그). 글은 `blog/<slug>/index.html`, 목록은 `blog/index.html`의 POSTS 주석 사이.
- `preview.html` : 미리보기용 조각 (배포 대상 아님).
- 배포: GitHub Pages (저장소 `marine-energy`).
