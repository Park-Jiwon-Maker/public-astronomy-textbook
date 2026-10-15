# -*- coding: utf-8 -*-
"""8장 3.2절 '대체 자료: 파일이 없을 때 쓰는 모의 영상' 상자 코드 전체 (『대중천문학개론』)

실행
    python ch08_s3-2_synthetic.py     # 인터넷·파일이 필요 없다(--offline을 붙여도 같다)

배경 잡음 위에 가우스 별상 40개를 얹은 256×256 배열을 만들고 합계를 찍는다.
ch08_s3-2_fits.py --offline이 이 파일을 불러 모의 영상을 만든다.
"""
# ---- 본문 코드 시작: 8장 3.2절 '대체 자료' 상자 ----
import numpy as np
rng = np.random.default_rng(0)            # 시드 고정: 누구나 같은 영상
ny, nx = 256, 256
y, x = np.mgrid[:ny, :nx]
data = rng.normal(100.0, 5.0, (ny, nx))   # 하늘 배경 + 잡음
for cx, cy, amp in rng.uniform([20, 20, 200], [236, 236, 3000], (40, 3)):
    # 가우스 별상 40개를 얹는다
    data += amp * np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * 2.2**2))
header = {"OBJECT": "synthetic (교육용 모의 영상)", "EXPTIME": 60}
print(data.sum())              # 표시를 바꿔도 이 합은 같아야 한다
# ---- 본문 코드 끝 ----
