# -*- coding: utf-8 -*-
"""오프라인 실행용 고정 자료 (『대중천문학개론』 10장)

install()을 부르면 requests.get이 인터넷 대신 data/ 폴더의 CSV로 응답한다.
본문 코드는 한 글자도 바꾸지 않고 그대로 돈다.

- OpenAlex 연도별 건수(group_by=publication_year): data/fig10-3.csv (2026-10-14 조회)
  고정 자료에는 cost_usd를 기록하지 않았으므로 응답에서 뺀다. 그래서 본문 코드는 그 자리에 None을 찍는다.
- Wikimedia 일별 조회수: data/fig10-4.csv (2024-03-20~04-30, 2026-10-14 조회)와
  data/fig10-4_baseline.csv (기준선으로 쓰는 조용한 달, 2026-10-15 조회)
고정 자료에 없는 질의나 기간을 요청하면 RuntimeError를 낸다.
"""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pandas as pd

DATA = Path(__file__).resolve().parent / "data"

OPENALEX_COLS = {'"astronomy education"': "astronomy_education", "astronomy": "astronomy"}
WIKI_COLS = {
    ("en.wikipedia", "Solar_eclipse_of_April_8,_2024"): "en_event",
    ("en.wikipedia", "Solar_eclipse"): "en_concept",
    ("ko.wikipedia", "2024년_4월_8일_일식"): "ko_event",
    ("ko.wikipedia", "일식"): "ko_concept",
}


class _Response:
    status_code = 200

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


def _openalex(url):
    q = unquote(url)
    m = re.search(r"title_and_abstract\.search:(.+?),publication_year:(\d{4})-(\d{4})", q)
    if not m or "group_by=publication_year" not in q or m.group(1) not in OPENALEX_COLS:
        raise RuntimeError(f"오프라인 자료에 없는 OpenAlex 질의다: {q}")
    df = pd.read_csv(DATA / "fig10-3.csv", comment="#", index_col="year")
    s = df[OPENALEX_COLS[m.group(1)]].loc[int(m.group(2)):int(m.group(3))].astype(int)
    groups = [{"key": str(y), "key_display_name": str(y), "count": int(c)}
              for y, c in s.sort_values(ascending=False).items() if c > 0]   # API처럼 건수 순, 0건인 해는 뺀다
    return {"meta": {"count": int(s.sum())}, "group_by": groups}


def _views(col):
    wide = pd.read_csv(DATA / "fig10-4.csv", comment="#", index_col="date_utc", parse_dates=True)[col]
    base = pd.read_csv(DATA / "fig10-4_baseline.csv", comment="#", parse_dates=["date_utc"])
    base = base[base["doc"] == col].set_index("date_utc")["views"]
    return pd.concat([wide, base]).sort_index()


def _pageviews(url):
    path = unquote(urlsplit(url).path)
    m = re.search(r"/per-article/([^/]+)/all-access/user/(.+)/daily/(\d{8})/(\d{8})$", path)
    key = (m.group(1), m.group(2)) if m else None
    if key not in WIKI_COLS:
        raise RuntimeError(f"오프라인 자료에 없는 문서다: {path}")
    want = pd.date_range(pd.to_datetime(m.group(3)), pd.to_datetime(m.group(4)), freq="D")
    s = _views(WIKI_COLS[key])
    if not want.isin(s.index).all():
        raise RuntimeError(f"오프라인 자료에 없는 기간이다: {m.group(3)}-{m.group(4)}")
    return {"items": [{"project": key[0], "article": key[1], "granularity": "daily",
                       "timestamp": d.strftime("%Y%m%d") + "00", "access": "all-access",
                       "agent": "user", "views": int(s[d])} for d in want]}


def fake_get(url, params=None, headers=None, timeout=None, **kwargs):
    host = urlsplit(url).netloc
    if host == "api.openalex.org":
        return _Response(_openalex(url))
    if host == "wikimedia.org":
        return _Response(_pageviews(url))
    raise RuntimeError(f"오프라인 모드에서는 이 주소를 부를 수 없다: {url}")


def install():
    import requests
    requests.get = fake_get
