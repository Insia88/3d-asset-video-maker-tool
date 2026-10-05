# 뷰티 ETF 영상 v1.4

작은 중앙 화면으로 바뀌던 컷을 모두 9:16 화면을 채우는 구도로 수정했다. 같은 원본에서 이어지는 구간은 연결하고, 전환에 최대 6프레임의 짧은 겹침을 적용했다. 가로 장면은 브랜드·제조·유통의 세 역할을 차례로 보여주는 팬으로 구성했다.

180초 · 1080×1920 · 30fps · 5,400프레임 · 93개 영상 구간. 문어체 자막 v4와 밝은 132BPM 연주곡을 유지하며 내레이션과 보컬은 없다.

실제 인코딩된 142개 고유 프레임의 독립 검수에서 화면 축소, 네 문제 경계의 잔류 화면, 세 역할 장면 누락이 교정됐다. 전체 파일 디코딩은 오류 없이 끝났고, 명시한 검정 구간 탐지 조건의 검출은 0건이었다. 검수는 표본 관찰과 기술 검사이며 전편 연속 재생·청취의 완료를 의미하지 않는다.

편집 원본 ZIP에는 40개 payload와 상대 경로로 연결된 34개 에셋이 있다. 모든 payload의 SHA-256과 ZIP CRC를 재검증하고 빈 폴더에 복원해 경로를 확인했다. 원본 프레임레이트는 변경하지 않았으며 보간과 60fps 변환은 적용하지 않았다.

[180초 수정본](https://drive.google.com/file/d/13rFWu-i0S3yTvpXjsNPo0mDzZpEHSVf6/view) · [편집 원본](https://drive.google.com/file/d/1JjqGbUJ6kqOkg0B7S0OtSfFpyCkcn6xW/view) · [검수 표본 묶음](https://drive.google.com/file/d/1x9HoTbnGLM3oPi30sAGHDjbd15nDsg8i/view)

[수정본과 편집 원본 폴더](https://drive.google.com/drive/folders/1gXrXhwhR8i4yo3fqc6PwHke6NHJgFjas)

금융 문장과 출처는 기존판과 같다. 한국 화장품의 세계 2위는 2025년 수출액 순위이며 시장 점유율 순위가 아니다. 산업 성장률은 ETF 수익률을 뜻하지 않는다. 생산 에셋은 3D 참고 수집 집계에 더하지 않는다.

이전 [v1.3 전달 기록](history/v1.3/delivery.md)과 원본은 보존했다. 현재 편집 원본은 단일 ZIP이며, 이전 v1.3의 다섯 ZIP과 섞어서 복원하지 않는다. ZIP의 movie/project.json을 기준으로 fonts와 media 상대 경로를 유지하면 된다. 포함된 패치 스크립트는 이전 v1.3 기준자료를 필요로 하며, 현재 project.json의 재편집에는 그 스크립트를 실행할 필요가 없다.
