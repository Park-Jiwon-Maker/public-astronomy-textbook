# -*- coding: utf-8 -*-
"""10장 실습 E 확장: 네 문서의 배수, 반감 일수, 절반 넘은 날 수 (『대중천문학개론』)

본문 실습 E 3–5단계(다른 세 문서도 세기, Baram-Tsabari와 Segev(2018)의 정의로 다시 세기)를 한 번에 한다.
본문 코드(ch10_labE_pageviews.py)의 daily()와 half_days()를 그대로 쓰고, 기준선이 0이거나 결측일 때를 함수로 뺐다.

실행
    python ch10_labE_four_docs.py            # Wikimedia 조회수 API에서 새로 조회
    python ch10_labE_four_docs.py --offline  # data/fig10-4*.csv(고정 자료)로 같은 계산

기준선: 사건 문서는 2024년 5월, 개념 문서는 2024년 2월의 하루 중앙값(828, 2,978, 15, 34).
"""
import sys
from pathlib import Path

if "--offline" in sys.argv:                       # 인터넷 대신 data/ 폴더의 고정 자료로 응답하게 한다
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import offline_fixtures
    offline_fixtures.install()

import requests
import pandas as pd
from urllib.parse import quote

BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
HEAD = {"User-Agent": "astro-class-lab/0.1 (https://example.org/class; contact@example.org)"}

# 문서 네 개: (프로젝트, 제목, 기준선 기간). 기준선은 사건과 떨어진 조용한 달의 중앙값이다
DOCS = [
    ("en.wikipedia", "Solar_eclipse_of_April_8,_2024", ("20240501", "20240531")),
    ("en.wikipedia", "Solar_eclipse",                  ("20240201", "20240229")),
    ("ko.wikipedia", "2024년_4월_8일_일식",            ("20240501", "20240531")),
    ("ko.wikipedia", "일식",                           ("20240201", "20240229")),
]


def daily(project, title, start, end):
    url = f"{BASE}/{project}/all-access/user/{quote(title, safe='')}/daily/{start}/{end}"
    r = requests.get(url, headers=HEAD, timeout=30)
    r.raise_for_status()
    s = pd.Series({it["timestamp"][:8]: it["views"] for it in r.json()["items"]})
    s.index = pd.to_datetime(s.index, format="%Y%m%d")   # UTC 날짜
    return s


def half_days(v, peak):
    """정점 뒤 처음으로 정점의 절반 아래로 떨어진 날까지의 일수. 관찰 기간 내 미도달이면 None."""
    after = v[v.index > peak]
    below = after[after < v[peak] / 2]
    return (below.index[0] - peak).days if len(below) else None


def ratio(peak_views, base):
    """정점/기준선 배수. 기준선이 0이거나 결측(None, NaN)이면 None."""
    return round(peak_views / base, 1) if pd.notna(base) and base > 0 else None


print("문서 | 정점 날짜(UTC) | 정점/기준선 배수 | 반감 일수 | 절반 넘은 날 수")
series = {}
for project, title, (b0, b1) in DOCS:
    v = daily(project, title, "20240320", "20240430")
    base = daily(project, title, b0, b1).median()
    peak = v.idxmax()
    above = int((v > v[peak] / 2).sum())   # Baram-Tsabari와 Segev(2018)식: 최댓값의 절반을 넘은 날 수
    print(f"{project} {title}", peak.date(), ratio(v[peak], base), half_days(v, peak), above, sep=" | ")
    series[title] = v

# 예외 처리 확인: 정점 날짜에서 끝나는 짧은 창(관찰 기간 내 미도달), 기준선 0과 결측
v = series["Solar_eclipse_of_April_8,_2024"].loc[:"2024-04-08"]
print("짧은 창(3/20–4/8) 반감 일수:", half_days(v, v.idxmax()),
      "| 기준선 0일 때 배수:", ratio(v.max(), 0), "| 기준선 결측일 때 배수:", ratio(v.max(), float("nan")))
