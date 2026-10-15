# 『대중천문학개론』 실습 코드와 자료

『대중천문학개론』은 충북대학교 천문우주학과 「대중천문학개론 및 실습(캡스톤 디자인)」을 위해 쓴 대학 교재다.
천문 교육과 과학 커뮤니케이션의 이론, 교구와 관측 현장, 공개 데이터와 계량 연구를 함께 다룬다.
이 저장소에는 책 8장(디지털 도구와 공개데이터)과 10장(과학계량과 대체지표)의 실습 코드 전체와 고정 자료를 둔다.
본문에는 원리가 드러나는 핵심 줄만 싣고, 코드 아래의 QR 코드가 이 저장소의 해당 파일을 가리킨다.

모든 스크립트는 `--offline`을 붙이면 인터넷 없이 끝까지 돌고, `expected/` 폴더의 출력과 같은 값을 낸다.
마지막 검증: 2026-10-15 (Windows 11, Python 3.12.10, 오프라인 전부와 온라인 일부 실행)

## 장별 실습 목록

본문 위치는 장·절과 상자 이름으로 적었다.

| 장·절 | 본문 상자·코드 | 파일 |
|---|---|---|
| 8장 3.2절 | 짧은 코드로 하는 FITS 시각화 (FITS 읽기, 헤더, zscale·asinh 표시) | [`ch08/ch08_s3-2_fits.py`](ch08/ch08_s3-2_fits.py) |
| 8장 3.2절 | 대체 자료 상자 「파일이 없을 때 쓰는 모의 영상」 | [`ch08/ch08_s3-2_synthetic.py`](ch08/ch08_s3-2_synthetic.py) |
| 8장 3.3절 | 좌표 변환으로 짜는 관측 계획 (M31, 충북대), 실습 D의 출발점 | [`ch08/ch08_s3-3_altaz.py`](ch08/ch08_s3-3_altaz.py) |
| 8장 3.2–3.3절 | 위 세 코드를 한 노트북으로 | [`ch08/ch08_astropy.ipynb`](ch08/ch08_astropy.ipynb) |
| 8장 5.1절 | 폴더 구조 (재현 가능한 프로젝트의 최소 구조를 실제 폴더로 만든다) | [`ch08/ch08_s5-1_project_tree.py`](ch08/ch08_s5-1_project_tree.py) |
| 10장 6.1절 | 실습 A 「OpenAlex로 검색에서 분석 대상까지」 | [`ch10/ch10_labA_openalex.py`](ch10/ch10_labA_openalex.py), [`.ipynb`](ch10/ch10_labA_openalex.ipynb) |
| 10장 6.1절 | 실습 E 「위키백과 조회수로 관심의 반감기 재기」 | [`ch10/ch10_labE_pageviews.py`](ch10/ch10_labE_pageviews.py), [`.ipynb`](ch10/ch10_labE_pageviews.ipynb) |
| 10장 6.1절 | 실습 E 3–5단계: 네 문서의 배수, 반감 일수, 절반 넘은 날 수 | [`ch10/ch10_labE_four_docs.py`](ch10/ch10_labE_four_docs.py) |

각 `.py` 파일의 `# ---- 본문 코드 시작 ----`과 `# ---- 본문 코드 끝 ----` 사이는 책에 처음 실었던 코드 전체를 한 글자도 바꾸지 않고 옮긴 것이다.
그 앞뒤의 몇 줄은 `--offline` 실행을 위한 준비다.

```
public-astronomy-textbook/
├─ README.md  LICENSE  CITATION.cff  requirements.txt  .gitignore
├─ ch08/
│  ├─ ch08_s3-2_fits.py  ch08_s3-2_synthetic.py  ch08_s3-3_altaz.py  ch08_s5-1_project_tree.py
│  ├─ ch08_astropy.ipynb
│  ├─ data/README.md            # FITS 파일을 두는 곳(저작권 때문에 파일은 넣지 않았다)
│  └─ expected/                 # 오프라인 실행의 예상 출력과 모의 영상 그림
└─ ch10/
   ├─ ch10_labA_openalex.py / .ipynb
   ├─ ch10_labE_pageviews.py / .ipynb  ch10_labE_four_docs.py
   ├─ offline_fixtures.py       # --offline일 때 requests.get 대신 data/의 CSV로 응답한다
   ├─ data/fig10-3.csv          # OpenAlex 2026-10-14 조회값(그림 10-3 자료)
   ├─ data/fig10-4.csv          # Wikimedia 2026-10-14 조회값(그림 10-4 자료)
   ├─ data/fig10-4_baseline.csv # 실습 E 기준선(조용한 달) 일별 조회수, 2026-10-15 조회
   └─ expected/
```

## 설치

Python 3.10 이상이면 된다. 검증한 버전은 `requirements.txt`에 적었다.

```
python -m pip install -r requirements.txt
```

| 항목 | 검증한 버전 |
|---|---|
| Python | 3.12.10 |
| numpy · pandas · requests | 2.5.4 · 3.0.6 · 2.34.2 |
| matplotlib | 3.11.2 |
| astropy | 8.0.1 (astropy-iers-data 0.2026.10.12.1.3.27, pyerfa 2.0.1.5) |
| 노트북을 열 때: ipykernel · nbformat · nbclient | 7.4.0 · 5.11.1 · 0.11.0 |

## 오프라인 실행

각 장 폴더에서 실행한다. `ch08` 스크립트는 지금 폴더에 `fig/`와 `synthetic.fits`를 만든다.

```
cd ch08
python ch08_s3-2_fits.py --offline       # 모의 영상으로 (m51_r.fits가 있으면 --offline 없이)
python ch08_s3-2_synthetic.py            # 대체 자료 상자의 모의 영상
python ch08_s3-3_altaz.py --offline      # M31 좌표 직접 입력, IERS 내려받기 끔
python ch08_s5-1_project_tree.py         # m51_photometry/ 폴더 구조를 만든다

cd ../ch10
python ch10_labA_openalex.py --offline   # data/fig10-3.csv로
python ch10_labE_pageviews.py --offline  # data/fig10-4*.csv로
python ch10_labE_four_docs.py --offline
```

`--offline`을 빼면 OpenAlex, Wikimedia, SIMBAD에서 새로 조회한다. 데이터베이스가 갱신되면 값이 조금 달라진다.
예를 들어 2026-10-15 온라인 조회에서 OpenAlex 분모는 82,914건이 아니라 82,908건이었고, 2024년 비율은 13.38이 아니라 13.40이었다.
노트북은 첫 셀의 `OFFLINE = True`를 `False`로 바꾸면 온라인으로 돈다. 노트북은 그 장 폴더에서 열어야 `data/`를 찾는다.

### 예상 결과 (요약)

```
ch08_s3-2_fits.py --offline      모의 영상 합계 8452420.58712957 … 표시 후 합계 8452420.58712957
ch08_s3-3_altaz.py --offline     최고 고도 85.2° 시각(KST) 2026-10-15 23:40:00.000 / 고도 30° 이상인 시간 9.0 시간
ch10_labA_openalex.py --offline  "astronomy education" 1055 None / astronomy 82914 None / 2025 24.42
ch10_labE_pageviews.py --offline 2024-04-08 1612.6 1
```

전체 출력은 각 장의 `expected/` 폴더에 있다. 오프라인에서 OpenAlex의 `cost_usd`는 `None`으로 찍힌다(온라인이면 0.001).

## Colab에서 열기

설치 없이 브라우저에서 돌리려면 아래 주소로 노트북을 연다. 첫 코드 셀이 Colab임을 알아채고 이 저장소를 내려받아 장 폴더로 옮긴다.

- 8장: https://colab.research.google.com/github/Park-Jiwon-Maker/public-astronomy-textbook/blob/main/ch08/ch08_astropy.ipynb
- 10장 실습 A: https://colab.research.google.com/github/Park-Jiwon-Maker/public-astronomy-textbook/blob/main/ch10/ch10_labA_openalex.ipynb
- 10장 실습 E: https://colab.research.google.com/github/Park-Jiwon-Maker/public-astronomy-textbook/blob/main/ch10/ch10_labE_pageviews.ipynb

GitHub에서 노트북 파일을 연 뒤 주소의 `github.com`을 `colab.research.google.com/github`로 바꿔도 같다.

## API 조건 (2026-10-15 확인)

- **OpenAlex**: 키 없이 조회된다. 키가 없으면 하루 0.1달러, 무료 키가 있으면 하루 1달러 상당까지 쓴다. 제목·초록 검색에
  `group_by`를 붙인 요청은 1,000건에 1달러(한 번에 0.001달러)다. 목록은 한 번에 최대 100건(`per-page=100`)이며,
  100건이 넘으면 `cursor=*`로 시작해 응답의 `meta.next_cursor`를 다음 요청에 넘기는데 둘째 쪽부터는 무료 키가 필요하다(없으면 401).
  키는 openalex.org/settings/api 에서 받아 코드에 적지 말고 환경 변수로 넘긴다.
  ```
  set OPENALEX_API_KEY=발급받은키        (Windows 명령 프롬프트)
  $env:OPENALEX_API_KEY="발급받은키"     (PowerShell)
  export OPENALEX_API_KEY=발급받은키     (macOS·Linux)
  ```
- **Wikimedia 조회수 API**: 계정이 필요 없다. 대신 User-Agent 머리글에 `도구 이름/버전 (연락처)` 형식으로 연락처를 적는다
  (Wikimedia Foundation User-Agent Policy). 코드의 `https://example.org/class; contact@example.org`를 자기 것으로 바꾸고, ASCII 글자만 쓴다.

## 자주 나는 오류

| 증상 | 원인 | 해결 |
|---|---|---|
| `UnicodeEncodeError: 'latin-1' codec can't encode characters` | User-Agent 등 HTTP 머리글에 한글을 넣었다 | 머리글에는 ASCII만 쓴다 |
| Wikimedia `403 Forbidden` | User-Agent를 비웠거나 일반 값을 썼다 | `도구/버전 (연락처)` 형식으로 적는다 |
| Wikimedia `404 Not Found` | 제목 철자, 띄어쓰기(밑줄로), 날짜 형식(YYYYMMDD) 오류 | 브라우저에서 같은 URL을 열어 본다 |
| OpenAlex `401 Unauthorized` | 키 없이 둘째 쪽을 요청했다 | 무료 키를 `OPENALEX_API_KEY`로 넘긴다 |
| OpenAlex `429 Too Many Requests` | 초당 요청 수나 하루 한도를 넘었다 | 요청 사이에 `time.sleep(0.2)`, 한도는 자정(UTC)에 초기화 |
| `ModuleNotFoundError` | 패키지 미설치 또는 다른 파이썬에 설치 | 같은 `python`으로 `python -m pip install -r requirements.txt` |
| `RuntimeError: 오프라인 자료에 없는 …` | `--offline`에서 고정 자료에 없는 질의·기간을 요청했다 | 본문과 같은 질의로 돌리거나 `--offline`을 뺀다 |
| `FileNotFoundError: m51_r.fits` | FITS 파일이 없다 | 파일을 장 폴더에 두거나 `--offline`으로 모의 영상을 쓴다 |
| `StopIteration` (FITS) | 2차원 영상 HDU가 없다(표나 3차원 큐브) | `hdul.info()` 출력에서 영상이 든 HDU를 확인한다 |
| `NameResolveError` (좌표 변환) | `SkyCoord.from_name`이 SIMBAD에 닿지 못했다 | `--offline`으로 좌표를 직접 넣는다 |
| IERS 관련 경고 | 지구 자전 자료를 내려받지 못했다 | 경고일 뿐이다. 고도 차이는 0.1° 미만이다 |
| 그림 제목의 한글이 네모로 나온다 | matplotlib 기본 글꼴에 한글이 없다 | `plt.rcParams["font.family"] = "Malgun Gothic"`(Windows) 또는 `"AppleGothic"`(macOS) |

## 오류 신고와 수정 이력

- 코드나 자료에서 오류를 찾으면 이 저장소의 Issues에 남긴다. 책의 장·쪽, 실행한 명령, 오류 메시지 전체, 운영체제와 Python 버전을 적어 주면 빨리 고칠 수 있다.
- 코드는 책을 다시 찍지 않고 이 저장소에서 고친다. 고친 내용은 커밋 기록(Commits)에 날짜와 함께 남고, 책 내용과 결과가 달라지는 수정은 아래 표에도 적는다.
- 보고서에 코드를 쓸 때는 내려받은 날짜나 커밋 번호를 함께 적는다.

| 날짜 | 파일 | 바뀐 내용 |
|---|---|---|
| 2026-10-15 | 전체 | 첫 공개. 책 8장·10장 코드 전체, 오프라인 고정 자료, 예상 출력 |

## 인용

이 저장소의 코드나 자료를 쓰면 책과 함께 인용한다. 서지 정보는 `CITATION.cff`에 있으며, GitHub 저장소 화면의 "Cite this repository"에서 APA·BibTeX 형식을 받을 수 있다.

```
(저자 추가 예정). (2026). 『대중천문학개론』 실습 코드와 자료 [소프트웨어]. GitHub. https://github.com/Park-Jiwon-Maker/public-astronomy-textbook
```

## 라이선스

코드는 MIT 라이선스(`LICENSE`)로 공개하는 것을 제안한다. 저자가 다른 라이선스로 바꿀 수 있다.
`ch10/data/`의 CSV는 OpenAlex(CC0)와 Wikimedia 조회수 API(CC0) 응답을 옮긴 것이다. 책 본문과 그림은 이 저장소에 들어 있지 않으며 저작권은 책의 저자에게 있다.
