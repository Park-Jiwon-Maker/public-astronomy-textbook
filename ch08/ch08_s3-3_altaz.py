# -*- coding: utf-8 -*-
"""8장 3.3절 '좌표 변환으로 짜는 관측 계획' 코드 전체 (『대중천문학개론』)

실행
    python ch08_s3-3_altaz.py            # SIMBAD에서 M31 좌표를 이름으로 조회(인터넷 필요)
    python ch08_s3-3_altaz.py --offline  # 이름 조회 대신 M31 좌표를 쓰고 IERS 자료 내려받기를 끈다

오프라인에서 쓰는 M31 좌표: ICRS RA 00h42m44.33s, Dec +41d16m07.5s (SIMBAD 기본 좌표).
IERS 자료를 내려받지 못하면 astropy가 내장 자료로 계산한다. 고도 값의 차이는 0.1° 미만이다.
본문 실습 D(대상 여러 개, 고도 곡선, 태양 고도 −18°)는 이 코드를 반복문으로 넓혀서 한다.
"""
import sys

if "--offline" in sys.argv:
    import warnings
    from astropy.utils import iers
    from astropy.coordinates import SkyCoord as _SkyCoord

    iers.conf.auto_download = False                                   # IERS 표를 내려받지 않는다
    warnings.filterwarnings("ignore", module="astropy.utils.iers")    # 내장 표 사용 경고 숨김
    _KNOWN = {"M31": ("00h42m44.33s", "+41d16m07.5s")}                 # SIMBAD 기본 좌표(ICRS)
    _SkyCoord.from_name = classmethod(lambda cls, name, **kw: cls(*_KNOWN[name], frame="icrs"))

# ---- 본문 코드 시작: 8장 3.3절 ----
# 적도좌표 → 지평좌표: "오늘 밤 이 대상은 몇 시에 가장 높이 뜨는가"
import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

# 관측지: 충북대학교 (위도 36.63°N, 경도 127.46°E, 고도 87 m)
site   = EarthLocation(lat=36.63*u.deg, lon=127.46*u.deg, height=87*u.m)
target = SkyCoord.from_name("M31")          # 이름으로 좌표 조회(SIMBAD)

# 한국시간 20시부터 12시간을 10분 간격으로 (UTC = KST − 9h)
t0    = Time("2026-10-15 11:00:00")          # = KST 20:00
times = t0 + np.arange(0, 12, 1/6) * u.hour

altaz = target.transform_to(AltAz(obstime=times, location=site))

best = np.argmax(altaz.alt)
print("최고 고도", f"{altaz.alt[best].deg:.1f}°",
      "시각(KST)", (times[best] + 9*u.hour).iso)
print("고도 30° 이상인 시간",
      f"{(altaz.alt > 30*u.deg).sum() / 6:.1f} 시간")
# ---- 본문 코드 끝 ----
