# -*- coding: utf-8 -*-
"""10장 6.1절 실습 E '위키백과 조회수로 관심의 반감기 재기' 코드 전체 (『대중천문학개론』)

실행
    python ch10_labE_pageviews.py            # Wikimedia 조회수 API에서 새로 조회
    python ch10_labE_pageviews.py --offline  # data/fig10-4*.csv(고정 자료)로 같은 계산

User-Agent (Wikimedia User-Agent 정책, 2026-10-15 확인)
- 형식: <도구 이름>/<버전> (<연락처>). 연락처는 누리집 주소, 이메일, 위키 사용자 이름 가운데 하나.
- HTTP 머리글에는 ASCII 글자만 넣는다. 한글을 넣으면 requests가 UnicodeEncodeError를 낸다.
- 아래 example.org 주소와 메일을 자기 수업 누리집과 연락처로 바꾼다.
네 문서를 한꺼번에 세고 예외 처리를 확인하는 확장판은 ch10_labE_four_docs.py에 있다.
"""
import sys
from pathlib import Path

if "--offline" in sys.argv:                       # 인터넷 대신 data/ 폴더의 고정 자료로 응답하게 한다
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import offline_fixtures
    offline_fixtures.install()

# ---- 본문 코드 시작: 10장 6.1절 실습 E ----
# 실습 E: 위키백과 일별 조회수와 반감 일수
import requests
import pandas as pd
from urllib.parse import quote

BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
# "도구 이름/버전 (연락처)" 형식. 머리글에는 ASCII만 쓰므로 주소와 메일을 영문 그대로 자기 것으로 바꾼다
HEAD = {"User-Agent": "astro-class-lab/0.1 (https://example.org/class; contact@example.org)"}

def daily(project, title, start, end):
    url = f"{BASE}/{project}/all-access/user/{quote(title, safe='')}/daily/{start}/{end}"
    r = requests.get(url, headers=HEAD, timeout=30)
    r.raise_for_status()
    s = pd.Series({it["timestamp"][:8]: it["views"] for it in r.json()["items"]})
    s.index = pd.to_datetime(s.index, format="%Y%m%d")   # UTC 날짜
    return s

def half_days(v, peak):        # 정점의 절반 아래로 처음 떨어지기까지의 날수. 기간 안에 없으면 None
    after = v[v.index > peak]
    below = after[after < v[peak] / 2]
    return (below.index[0] - peak).days if len(below) else None

T = "Solar_eclipse_of_April_8,_2024"
v = daily("en.wikipedia", T, "20240320", "20240430")
peak = v.idxmax()
base = daily("en.wikipedia", T, "20240501", "20240531").median()   # 조용한 달의 중앙값
# 사건 전에 관심이 오르지 않는 문서는 정점 전 30일 중앙값을 쓴다:
# base = v[v.index < peak].tail(30).median()
ratio = round(v[peak] / base, 1) if base > 0 else None   # 기준선이 0이거나 결측이면 None
print(peak.date(), ratio, half_days(v, peak))   # 2024-04-08 1612.6 1
# ---- 본문 코드 끝 ----
