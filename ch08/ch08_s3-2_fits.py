# -*- coding: utf-8 -*-
"""8장 3.2절 '20줄로 하는 FITS 시각화' 코드 전체 (『대중천문학개론』)

실행
    python ch08_s3-2_fits.py              # 지금 폴더의 m51_r.fits를 읽는다(본문 코드 그대로)
    python ch08_s3-2_fits.py --offline    # 파일 없이 '대체 자료' 상자의 모의 영상으로 실행

--offline이면 ch08_s3-2_synthetic.py(상자 코드)로 모의 영상을 만들어 synthetic.fits로 저장하고,
본문 코드가 m51_r.fits 대신 그 파일을 열게 한다. 그림은 fig/synthetic_asinh.png로 이름을 바꿔 둔다.
FITS 머리글에는 ASCII 글자만 들어가므로 OBJECT 값은 영어로 적는다.
모의 영상은 관측자료가 아니며 M51의 대체물로 인용하지 않는다.
"""
import sys

import matplotlib
matplotlib.use("Agg")   # 창을 띄우지 않고 파일로만 저장한다

OFFLINE = "--offline" in sys.argv
if OFFLINE:
    import runpy
    from pathlib import Path
    from astropy.io import fits as _fits

    print("모의 영상 합계", end=" ")
    _mock = runpy.run_path(str(Path(__file__).resolve().parent / "ch08_s3-2_synthetic.py"))
    _hdr = _fits.Header({"OBJECT": "synthetic (educational mock image)", "EXPTIME": 60})
    _fits.PrimaryHDU(_mock["data"], header=_hdr).writeto("synthetic.fits", overwrite=True)
    _open = _fits.open
    _fits.open = lambda name, *a, **k: _open("synthetic.fits" if name == "m51_r.fits" else name, *a, **k)

# ---- 본문 코드 시작: 8장 3.2절 ----
# FITS를 읽고, 헤더를 확인하고, 보기 좋게 표시한다
# 예제 파일 m51_r.fits: 공개 아카이브나 소속 관측소에서 받은 R 밴드 영상. 파일명·출처·
# 내려받은 날짜·전처리(바이어스/플랫 여부)를 관측일지에 적어 둔다. 파일이 없으면 아래 상자의 모의 영상을 쓴다.
import os
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ZScaleInterval, AsinhStretch, ImageNormalize

path = "m51_r.fits"

with fits.open(path) as hdul:
    hdul.info()                       # 어떤 확장(HDU)이 있는지 목록
    # 영상은 기본 HDU가 아니라 확장 HDU에 있을 수도 있다: 2차원 데이터를 가진 첫 HDU를 고른다
    hdu    = next(h for h in hdul if h.data is not None and h.data.ndim == 2)
    data   = hdu.data                 # 2차원 배열 = 픽셀별 계수
    header = hdu.header

for key in ("OBJECT", "DATE-OBS", "EXPTIME", "FILTER", "TELESCOP"):
    print(f"{key:10s}", header.get(key, "— 없음"))

# zscale 로 표시 구간을 잡고, asinh 로 어두운 구조를 끌어올린다
norm = ImageNormalize(data,
                      interval=ZScaleInterval(),
                      stretch=AsinhStretch())

plt.figure(figsize=(6, 6))
plt.imshow(data, origin="lower", cmap="gray", norm=norm)
plt.colorbar(label="ADU")
plt.title(header.get("OBJECT", "unknown"))
os.makedirs("fig", exist_ok=True)   # 저장 폴더가 없으면 만든다
plt.savefig("fig/m51_r_asinh.png", dpi=150, bbox_inches="tight")
# ---- 본문 코드 끝 ----

if OFFLINE:
    import os
    os.replace("fig/m51_r_asinh.png", "fig/synthetic_asinh.png")
    print("저장 fig/synthetic_asinh.png")
    print("표시 후 합계", data.sum())    # norm은 표시만 바꾸므로 위의 합계와 같다
else:
    print("저장 fig/m51_r_asinh.png")
