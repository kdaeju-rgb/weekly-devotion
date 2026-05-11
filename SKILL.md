---
name: weekly-devotion
description: 주일 설교 .md 한 편을 성인/청년 소그룹 5일 묵상 인터랙티브 HTML 한 장으로 변환한다. 데스크톱은 16:9 슬라이드, 모바일은 100dvh 풀스크린으로 자동 분기. Anthropic claude.com 디자인 + 나눔명조 ExtraBold + SUIT Bold + SVG 라인 일러스트 인라인. 출력 파일명 = 설교 .md 파일명. GitHub Pages 푸시는 선택사항. 사용자 트리거 — "/weekly-devotion [설교 .md 경로]", "이 설교로 5일 묵상 만들어줘", "주간 묵상 자료 만들어줘".
---

# weekly-devotion

주일 설교 한 편을 성인 예배 / 청년 소그룹 성도가 매일 들고 묵상할 수 있는 5일 시리즈로 변환. **단 하나의 self-contained HTML 파일** (CSS·JS·SVG 모두 인라인) → 카톡으로 링크 한 줄 보내면 폰/PC 어디서나 자동 적응.

## 입력

- 설교 메인 노트 `.md` 절대경로 (frontmatter + `## [[제목]]` 형태의 설교조각 메모 6~7개 + `# 원본 설교문` 섹션)
- 옵시디언 볼트 표준 위치: `~/Library/Mobile Documents/com~apple~CloudDocs/Dae Ju Kim DB_Ver1/200_설교&예배/201_주일 설교/{년도}/`

옵션 플래그:
- `--template={classic|narrative|poster}` — 디자인 템플릿 선택 (지정 안 하면 Claude가 사용자에게 물어봄)
  - `classic` — 정형 16장. 모든 day가 hero / 묵상 / 적용 동일 박자. cream + coral 톤.
  - `narrative` — 스토리 아크 변주 19장. 인트로 2장 분리, Day 3 전체 dark + watermark, 풀-블리드 타이포 1장, drop cap 좌우 2단, 세 단어 단독 슬라이드.
  - `poster` — 미니멀 포스터 8장. 각 day가 단 1장 (거대 숫자 + 핵심 한 줄 + 구절 + 질문 1개 + 기도 1줄). day별 고유 배경 틴트. 폰에서 휙휙 넘기기 좋음.
- `--with-codex-review` — 콘텐츠 초안 후 codex 한 번 더 의견 받음 (3-5분 추가)
- `--push` — GitHub Pages에 자동 푸시 (레포 설정이 완료된 경우에만)
- `--ai-images` — 별도 OpenAI 키(`OPENAI_API_KEY` 환경변수)가 있을 때만. 기본은 SVG 라인 일러스트

## 출력

**단 하나의 self-contained HTML 파일**:
- 위치: `~/Sites/weekly-devotion/devotional/{sermon_filename}.html`
- 파일명: 설교 .md 파일명에서 `.md`만 제거 (예: `05-10-2026_주일설교.html`)
- 모든 자산 인라인 (CSS · JS · SVG 일러스트 5장 모두 `<style>` / `<script>` / `<symbol>` 태그 내부)
- 외부 의존성: 나눔명조 웹폰트 CDN만 (Google Fonts `<link>`)

**반응형 자동 분기 (한 파일)**:
- 데스크톱 (≥834px): 16:9 `aspect-ratio` 컨테이너로 슬라이드 데크 모드
- 모바일 (<833px): `100dvh` 풀스크린, 단일 컬럼, day-tile 세로 리스트, Safari 주소창 회피 (`env(safe-area-inset-bottom)`)
- 가로 폰: 16:9 느낌 일부 복원

---

## 절차 (필수, 순서대로)

### Step 0. 사전 확인

1. 입력 설교 `.md` 파일 존재 확인 (iCloud 경로는 터미널 직접 접근 불가 — 사용자에게 내용 붙여넣기 요청하거나 경로 확인)
2. 출력 폴더: `~/Sites/weekly-devotion/devotional/` — 없으면 생성
3. 스크립트 폴더: `~/Sites/weekly-devotion/scripts/` — 없으면 사용자에게 스크립트 복사 안내

### Step 0.5. 템플릿 선택 (필수)

`--template=` 플래그가 없으면 **사용자에게 어느 시안으로 만들지 반드시 묻고 선택받는다**. 다음 3종 중 하나:

| 옵션 | 슬라이드 수 | 시그니처 | 본보기 파일 |
|---|---|---|---|
| `classic` | 16장 | 정형 cream/coral, 동일 박자, hero/묵상/적용 패턴 | `~/Sites/weekly-devotion/scripts/template_classic_example.html` |
| `narrative` | 19장 | 스토리 아크 변주, 인트로 2장, dark Day, drop cap, 풀-블리드, 세 단어 | `~/Sites/weekly-devotion/scripts/template_narrative_example.html` |
| `poster` | 8장 | 미니멀 포스터, 거대 숫자, day별 배경 틴트, 폰 친화 | `~/Sites/weekly-devotion/scripts/template_poster_example.html` |

**선택된 템플릿의 example HTML을 Step 4에서 참고로 Read**하고, 새 설교 콘텐츠로 같은 디자인 어휘를 재구성한다.

### Step 1. 설교 파싱

설교 `.md` 읽고 다음을 추출:
- **frontmatter**: `성경구절` (wikilink 배열), `본문`, `대상` 등 존재하는 항목
- **설교조각 메모 N개**: `## [[제목]]` 헤딩으로 구분된 섹션들 (각 메모는 핵심 한 문장 + 본문 인용 + 해설)
- **원본 설교문**: `# 원본 설교문` 이후 전체 본문

### Step 2. 5일 묵상 구조화 (Claude가 직접 작성)

설교조각 메모를 기반으로 5일치 콘텐츠를 짜되, 다음 분배 원칙:

| Day | 일반 매핑 |
|---|---|
| 1 | 도입 — 설교의 핵심 명제를 삶의 현실적 질문·상황과 연결 |
| 2 | 핵심 1 — 첫 번째 본문 구절 + 신학적 의미 + 삶 적용 |
| 3 | 핵심 2 — 두 번째 본문 구절 + 신학적 의미 + 삶 적용 |
| 4 | 핵심 3 — 세 번째 본문 구절 + 신학적 의미 + 삶 적용 |
| 5 | 마무리 — 종합 + 한 주간 결단 + 기도 |

각 일자 출력 구조:

```json
{
  "series_title": "예수의 길",
  "series_subtitle": "마태복음 13장 · 씨 뿌리는 비유",
  "days": [
    {
      "label": "척박한 땅에서",        // 8자 이내, 헤더에 표시
      "title_line1": "말씀은",          // 8자 이내
      "title_line2": "그 자리에 뿌려집니다.", // 14자 이내, 마침표 포함
      "subhead": "온갖 불신앙 한가운데서도 ...", // 1문장, 35자 이내
      "scripture": "씨 뿌리는 비유를 들으라", // 본문 핵심 1구절, 50자 이내
      "scripture_cite": "마태복음 13:18",
      "key1": "하나님의 말씀은,",       // pull quote 1행, 12자 이내
      "key2": "가장 척박한 곳에 씨앗처럼 뿌려집니다.", // 2행
      "med_p1": "...",                  // 묵상 본문 1단락 100~140자
      "med_p2": "...",                  // 묵상 본문 2단락 100~140자
      "app_headline": "오늘 하루, 말씀 한 구절을 붙잡고 살기.",
      "q1": "이번 주 나의 밭은 어떤 상태였나요?", // 적용 질문 50자 이내
      "q2": "말씀이 막혔던 자리는 어디였나요?",
      "prayer": "주님,\n오늘도 제 삶의 한복판에 ...\n말씀대로 살아갈 힘을 주소서." // 3-4행, \n으로 구분
    }
    /* 4 more days */
  ]
}
```

**톤 원칙** (성인/청년 소그룹 대상):
- 존댓말 기반, 2인칭 "우리" 또는 호격 없이 직접 서술
- 신학적 개념어 사용 가능하되 반드시 일상 언어로 풀어내기 (예: "칭의" → "하나님 앞에 의롭다 여겨지는 것")
- 한 문장 30자 내외 권장
- 적용 질문은 직장·가정·신앙 성숙의 구체적 맥락 포함 가능
- 기도: "하나님"/"주님" 호칭, 삶의 구체적 현장 언급 (일, 관계, 결단)
- 깊이 있는 묵상 가능 — 청소년 대비 단락 길이 10~20자 더 허용

### Step 3. SVG 일러스트 5장 생성

`~/Sites/weekly-devotion/scripts/generate_svg_images.py` 실행 → `img/day{1..5}.svg` 생성.

스크립트가 없으면 Claude가 직접 SVG 코드를 인라인으로 작성 (단색 coral `#cc785c` stroke, 1024×1024 viewBox, 손그린 미니멀). 설교 주제에 맞는 이미지 5종:

- 기본 예시: 씨앗·뿌리 / 척박한 돌밭 / 빛으로 수렴하는 길 / 자라나는 싹 / 열매 맺는 나무
- 설교 주제가 다르면 그에 맞춰 새로 짜기

`--ai-images` 플래그 + `OPENAI_API_KEY` 환경변수 발견 시: `~/Sites/weekly-devotion/scripts/generate_ai_images.py` 실행.

### Step 4. HTML 한 장 빌드

**Claude가 직접 작성**. 선택된 템플릿의 본보기 파일을 Read한 후 같은 디자인 어휘로 새 설교 콘텐츠를 채워 넣는다.

- `--template=classic` → `~/Sites/weekly-devotion/scripts/template_classic_example.html` 참고 (16장 정형)
- `--template=narrative` → `~/Sites/weekly-devotion/scripts/template_narrative_example.html` 참고 (19장 스토리 아크)
- `--template=poster` → `~/Sites/weekly-devotion/scripts/template_poster_example.html` 참고 (8장 미니멀 포스터)

**파일 위치**: `~/Sites/weekly-devotion/devotional/{설교 .md 파일명 .md → .html}`
- 예: 입력 `05-10-2026 주일설교.md` → 출력 `05-10-2026 주일설교.html`

**필수 디자인 토큰** (변경 금지):
- 색상: cream `#faf9f5` + coral `#cc785c` + dark `#181715`
- 폰트: 나눔명조 ExtraBold (display, Google Fonts) + SUIT Bold (body, jsdelivr CDN)
- 16:9 `.deck { aspect-ratio: 16/9 }` 컨테이너 (데스크톱)
- 모바일 `@media (max-width: 833px)`: `.deck { aspect-ratio: auto; height: 100dvh }` + `env(safe-area-inset-bottom)`
- `word-break: keep-all; overflow-wrap: break-word;` 모든 한국어 텍스트
- `.slide { overflow: auto }` (긴 본문 잘림 X)
- 인트로 day-tile `data-goto` + 클릭 핸들러
- 키보드 ←→/Space + 터치 스와이프 + 좌우 클릭

**필수 폰트 크기**:
- 디스플레이: clamp(44px, 5.8vw, 82px)
- 핵심 풀-quote: clamp(34px, 4vw, 56px)
- 부제: clamp(20px, 2vw, 27px) SUIT Medium
- 본문: clamp(18px, 1.7vw, 23px) SUIT Regular
- 성경 인용: clamp(22px, 2.3vw, 30px) 나눔명조 Bold
- 성경 출처: clamp(15px, 1.3vw, 19px) SUIT Bold
- 푸터: 14px

**SVG 5장 인라인** (`<svg width="0" height="0">` 안에 `<symbol id="day1-svg">...</symbol>` 5개, 슬라이드에서 `<use href="#day1-svg"/>`로 참조).

**총 슬라이드 수**: `classic` 16장, `narrative` 19장, `poster` 8장. 각 본보기 파일의 슬라이드 구조를 그대로 따른다.

### Step 5. 옵션 — codex review

`--with-codex-review` 플래그 시:

```bash
codex exec "Review devotional/{filename}.html for: AI-slop tells, awkward Korean line breaks, font size issues, overflow risks, mobile-portrait usability. Cite line numbers. Be brutal. Top 3 fixes by impact-per-effort." \
-C "$HOME/Sites/weekly-devotion" -s read-only -c 'model_reasoning_effort="medium"'
```

받은 피드백 → 사용자에게 그대로 보여주고 적용 여부 확인.

### Step 6. (선택) 푸시 + 라이브 URL 반환

`--push` 플래그가 있고 git 레포가 설정된 경우에만 실행:

```bash
cd ~/Sites/weekly-devotion
git add devotional/
git -c user.email=kdaeju@gmail.com -c user.name="danielkim" commit -m "Add devotional: {sermon title}"
git push
```

레포 미설정 시: HTML 파일 로컬 경로만 안내. GitHub Pages 설정이 필요하면 사용자에게 안내.

---

## 절대 규칙

1. **콘텐츠 파일(설교 .md)은 절대 수정하지 않는다** — 읽기 전용
2. **기존 HTML 덮어쓰기 전에 사용자 확인**
3. **iCloud 경로 직접 접근 불가** — 설교 파일은 사용자가 내용을 붙여넣거나 다른 경로로 복사 후 진행
4. **푸시 전에 `git status`로 변경 내역 사용자에게 미리 보고**
5. **한국어 폰트 함정 회피**: PPT 빌드 시 `set_korean_font(run, font, bold)` 헬퍼만 사용

## 출력 보고 형식

작업 완료 후 사용자에게:

```
✓ 묵상 자료 빌드 완료

로컬 파일:
- ~/Sites/weekly-devotion/devotional/{sermon_filename}.html

5일 콘텐츠 매핑:
- Day 1: {title} ({scripture})
- Day 2: ...
- Day 3: ...
- Day 4: ...
- Day 5: ...

브라우저에서 열기:
open ~/Sites/weekly-devotion/devotional/{sermon_filename}.html
```

## 기존 디자인 결정 (변경 시 사용자 확인 필요)

- **5일 분배** = 설교조각 메모 6~7개 중 핵심 5개 선별 (도입+종합 포함)
- **이미지** = SVG 라인 일러스트 기본 (claude.com 미학)
- **폰트** = 나눔명조 ExtraBold + SUIT Bold
- **디자인 시스템** = Anthropic claude.com (cream/coral/dark 3-surface)
- **슬라이드 비율** = 16:9 (강의실/웹 표준)
- **모바일** = 100dvh 풀스크린, day-card 점프, 스와이프
- **대상** = 성인 예배 / 청년 소그룹
