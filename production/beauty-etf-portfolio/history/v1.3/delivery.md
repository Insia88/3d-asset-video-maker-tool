# 완성본의 형식과 전달 상태

132BPM 자체 연주곡과 새 항공·동작을 적용한 180초 Higgsedit 편집본 v1.3이다. 문어체 자막 v4를 사용한다.

| 항목 | 확인 결과 |
|---|---|
| 길이·해상도 | 180.000초 · 1080×1920 · 9:16 |
| 프레임 | 30fps · 5,400프레임 |
| 구성 | 105컷: 영상 35개·정지 70개 · 지속 자막 40그룹 |
| 음악 | 132BPM 오리지널 연주곡 · 무내레이션·무보컬 |
| 최종 음량 | 실제 AAC 입력 분석 −16.04LUFS · −0.98dBTP |
| 기술 검사 | 전체 디코딩 오류 0 · 검정 구간 0 |
| 시각 검사 | 실제 자막 중간 화면 40개 · 최종 인코딩 표본 15개 |
| 파일 | 74,797,657바이트 |
| SHA-256 | `8817f7b7c51b564d9d615b3f818a2e4a6433af3793a5055720deea4dff7a97e0` |

[180초 완성본 v1.3](https://drive.google.com/file/d/1lsCMVUakZQ2YZMoHtxNZerGaX-A-A6Dv/view) · [공유 기획안](https://docs.google.com/document/d/1a1AHSuMrylfhS2jx9jOgBu2UurlWVNwJkBV3mwmj2ro) · [기획안 PDF](https://drive.google.com/file/d/1mf4ountHHj9xfOOn4QYVC-AX4ci3p7vN/view)

같은 영상 링크에서 실제 MP4 바이트를 교체하고 이름·크기·부모 폴더를 독립 대조했다. 권한은 바꾸지 않았다. 원격 파일 바이트의 SHA를 다시 계산한 것으로 표시하지 않는다.

## 재편집 소스

아래 다섯 ZIP은 같은 빈 폴더에 모두 풀어야 한다. 122개 실제 파일의 CRC·SHA와 중복 없는 합집합을 확인했고, 34개 네이티브 에셋 경로가 정상이다. 제작자는 빈 폴더 복구 후 항공·지수 종료·마지막 장면의 세 PNG가 원래 렌더와 동일한 해시임을 확인했다.

| 부분 | 파일 | 바이트 |
|---|---|---:|
| 1 | [beauty-etf-v1.3-editable-source-part-01.zip](https://drive.google.com/file/d/1ptyRGpHL8bJOKPXN_rVO3lzVNyG93s7P/view) | 85,572,051 |
| 2 | [beauty-etf-v1.3-editable-source-part-02.zip](https://drive.google.com/file/d/10b-6Mq5mkZgTzKL8mZSlGeSEsyfiAn8o/view) | 87,412,054 |
| 3 | [beauty-etf-v1.3-editable-source-part-03.zip](https://drive.google.com/file/d/14KPu2-wsSoWMgzJ5lRo8r_1ZYSeyWE1y/view) | 87,191,143 |
| 4 | [beauty-etf-v1.3-editable-source-part-04.zip](https://drive.google.com/file/d/1TOd6886hcoWhZugSUx_yzPa8aAI5hobw/view) | 84,478,912 |
| 5 | [beauty-etf-v1.3-editable-source-part-05.zip](https://drive.google.com/file/d/1Mk0mH2bqRwDiXjgqjAEpYTzMpmfEKMXl/view) | 68,033,344 |

[원본·음악·MIDI·자막 백업 폴더](https://drive.google.com/drive/folders/1WA8Vv43dkLC6bf_fz3S09ZgFIy36UG9X)에서 음악 소스 ZIP과 별도 MIDI/MP3도 확인할 수 있다. 네이티브 편집 소스의 메타데이터·복구 해시는 [패키지 검사](qc/package_check.json)에 있다.

## 이전 Adobe 작업

[이전 원고의 180초 AEP](https://drive.google.com/file/d/1rFHV53faEN48DjT5UDOL_zffQHKYR0uh/view)와 [문어체 v3의 실제 AE 12초 프리뷰](https://drive.google.com/file/d/1CeuuQzRnmb_iw0h61cK-pHk6EkNMkhjo/view)는 별도 제작 이력이다. 프리뷰는 19,421,230바이트·30fps·360프레임이며, AEP의 최신 portable 의존파일 묶음은 완료되지 않았다. 현재 v1.3의 재편집 소스는 위 Higgsedit 다섯 ZIP이다.

40개 중간 화면과 15개 최종 표본을 직접 확인한 검수는 전편 연속 시청이나 전곡 청취를 뜻하지 않는다. 실제 파일 형식·해시·범위는 [전달 JSON](delivery_status.json)에 있다. 원본 미디어와 편집 바이너리는 공개 Git에 넣지 않는다.
