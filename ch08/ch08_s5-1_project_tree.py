# -*- coding: utf-8 -*-
"""8장 5.1절 '폴더 구조'의 최소 구조를 실제 폴더로 만든다 (『대중천문학개론』)

실행
    python ch08_s5-1_project_tree.py                 # 지금 폴더에 m51_photometry/ 를 만든다
    python ch08_s5-1_project_tree.py 내프로젝트       # 이름을 바꿔 만든다
    (--offline을 붙여도 같다. 인터넷을 쓰지 않는다)

이미 있는 파일은 덮어쓰지 않는다. 본문의 폴더 구조 전체는 아래 TREE와 같다.
"""
import json
import sys
from pathlib import Path

# ---- 본문 코드 시작: 8장 5.1절 폴더 구조 ----
TREE = """\
m51_photometry/
├─ data/
│  ├─ raw/          # 내려받은 원본. 절대 수정하지 않는다
│  └─ processed/    # 가공 결과. 언제든 코드로 다시 만들 수 있어야 한다
├─ code/
│  ├─ 01_inspect.ipynb
│  ├─ 02_photometry.ipynb
│  └─ 03_figures.ipynb
├─ fig/            # 보고서에 넣을 그림. 코드가 자동 저장
├─ docs/
│  ├─ SOURCES.md    # 데이터 출처·DOI·접속일
│  └─ LOG.md        # 날짜별 작업 기록과 판단 근거
└─ README.md        # 이 프로젝트가 무엇이고 어떻게 실행하는가
"""
# ---- 본문 코드 끝 ----

TEMPLATES = {
    "docs/SOURCES.md": "# 데이터 출처\n\n| 파일 | 출처(아카이브·관측소) | DOI 또는 URL | 검색식 | 접속일 | 전처리 |\n|---|---|---|---|---|---|\n",
    "docs/LOG.md": "# 작업 기록\n\n## YYYY-MM-DD\n- 한 일:\n- 판단과 근거:\n",
    "README.md": "# {name}\n\n무엇을 하는 프로젝트인가, 어떤 순서로 실행하는가(code/01 → 02 → 03)를 적는다.\n",
}
EMPTY_NOTEBOOK = {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    name = args[0] if args else "m51_photometry"
    root = Path(name)
    for d in ("data/raw", "data/processed", "code", "fig", "docs"):
        (root / d).mkdir(parents=True, exist_ok=True)
        keep = root / d / ".gitkeep"
        if not any((root / d).iterdir()):
            keep.touch()
    for nb in ("01_inspect.ipynb", "02_photometry.ipynb", "03_figures.ipynb"):
        p = root / "code" / nb
        if not p.exists():
            p.write_text(json.dumps(EMPTY_NOTEBOOK, indent=1), encoding="utf-8")
    for rel, text in TEMPLATES.items():
        p = root / rel
        if not p.exists():
            p.write_text(text.replace("{name}", name), encoding="utf-8")
    print(TREE.replace("m51_photometry/", f"{name}/", 1), end="")
    print("만든 폴더:", root.resolve().name)


if __name__ == "__main__":
    main()
