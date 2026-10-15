# ch08 data

본문 3.2절 코드는 지금 폴더의 `m51_r.fits`를 읽는다. 공개 아카이브(MAST, ESO Archive 등)나 소속 관측소에서 받은 R 밴드 영상을
`m51_r.fits`라는 이름으로 `ch08` 폴더에 두거나, 다른 파일이면 코드의 `path = "m51_r.fits"` 줄을 고친다.
파일명, 출처, 내려받은 날짜, 전처리(바이어스·플랫 보정 여부)를 관측일지나 `docs/SOURCES.md`에 적어 둔다.

파일이 없으면 `python ch08_s3-2_fits.py --offline`으로 모의 영상을 쓴다. 이 폴더에는 저작권 문제로 FITS 파일을 넣지 않았다.
