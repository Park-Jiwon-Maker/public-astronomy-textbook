# -*- coding: utf-8 -*-
"""10장 6.1절 실습 A 'OpenAlex로 검색에서 분석 대상까지' 코드 전체 (『대중천문학개론』)

실행
    python ch10_labA_openalex.py            # OpenAlex API에서 새로 조회
    python ch10_labA_openalex.py --offline  # data/fig10-3.csv(2026-10-14 조회값)로 같은 계산

API 조건(2026-10-15 OpenAlex Help Center에서 확인)
- 키 없이도 조회된다. 키가 없으면 하루 0.1달러, 무료 키가 있으면 하루 1달러 상당까지 쓸 수 있다.
- 제목·초록 검색(title_and_abstract.search)에 group_by를 붙인 요청은 1,000건에 1달러(한 번에 0.001달러)다.
- 무료 키는 openalex.org/settings/api 에서 받는다. 코드에 적지 말고 환경 변수 OPENALEX_API_KEY로 넘긴다.
- group_by 요청은 한 번에 끝나므로 페이지 넘김이 필요 없다.
오프라인이면 cost_usd 자리에 None이 찍힌다(고정 자료에 기록하지 않았다).
"""
import sys
from pathlib import Path

if "--offline" in sys.argv:                       # 인터넷 대신 data/ 폴더의 고정 자료로 응답하게 한다
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import offline_fixtures
    offline_fixtures.install()

# ---- 본문 코드 시작: 10장 6.1절 실습 A ----
# 실습 A: OpenAlex 연도별 건수와 천 건당 비율
import os
import requests
import pandas as pd
from urllib.parse import quote

URL = "https://api.openalex.org/works"
KEY = os.environ.get("OPENALEX_API_KEY")   # 무료 키(선택). 키를 코드에 직접 적지 않는다

def by_year(query):
    f = quote(f"title_and_abstract.search:{query},publication_year:2000-2025", safe=":,")
    r = requests.get(f"{URL}?filter={f}&group_by=publication_year",
                     params={"api_key": KEY} if KEY else {}, timeout=30)
    r.raise_for_status()
    js = r.json()
    print(query, js["meta"]["count"], js["meta"].get("cost_usd"))   # 질의 기록표로 옮긴다
    return pd.Series({int(g["key"]): g["count"] for g in js["group_by"]}).sort_index()

num = by_year('"astronomy education"')
den = by_year("astronomy")
num = num.reindex(den.index, fill_value=0)   # 0건인 해는 group_by 결과에 빠지므로 0으로 채운다
print((num / den * 1000).round(2).loc[2020:])   # astronomy 문헌 천 건당 비율
# ---- 본문 코드 끝 ----
