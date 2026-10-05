# 뷰티 ETF 영상: 추가 키 이미지와 금융 근거

20~30대 뷰티 관심 투자자를 위한 약 180초 핀플루언서 지원 영상이다. [8페이지 Google Docs 기획안](https://docs.google.com/document/d/1a1AHSuMrylfhS2jx9jOgBu2UurlWVNwJkBV3mwmj2ro)은 작은 화장대의 제품에서 브랜드·제조·판매와 ETF 구성으로 설명을 확장한다.

기초 이미지 5개에 추가 장면 10개를 더해 **채택 이미지 15개**를 사용한다. 실제 생성 성공은 누적 16개이며, 이 중 초기 S07 한 개는 캐릭터 형태 차이로 제외하고 S07 v2로 교체했다. 생성 이미지가 25,000개 참고 조사에 추가한 수는 **0개**다. 기초 이미지와 Element 4개의 기록은 [기초 에셋 폴더](../beauty-etf-foundation/)에 보존한다.

## 에셋과 제작 기록

- [추가 10종 PNG 원본 폴더](https://drive.google.com/drive/folders/1G7Kmb2qxX-j_bYXJd0HN3iZJ2w1y17bm)
- [후속 영상용 10종 사용안내](후속영상용10종사용안내.md) · [Drive 사용안내](https://drive.google.com/file/d/1GNT8Ui0OwAxe0q6m9Kp0LuTL6C4erjIo/view)
- [생성·채택·참조 메타데이터](expansion_assets_manifest_handoff.json)
- [잠금 파일 10개](media/) · [복구용 기록 ZIP](https://drive.google.com/file/d/11dVy26txzJ845h413xQKqbPpcCye0YeN/view)

PNG와 대용량 원문 PDF는 이 폴더에 복제하지 않는다. Drive의 PNG를 원래 파일명으로 내려받아 프로젝트의 assets 폴더에 두면 잠금 파일의 상대 경로와 연결된다. 각 잠금 파일은 원래 프롬프트, 이미지 작업 ID, 치수와 SHA256을 보존한다. 이미지 참조는 실제 성공한 image job ID로 실행했으며, 3D 스타일 PNG는 편집 가능한 메시나 리깅 파일과 구분한다.

추가 11개 생성 성공 중 10개를 채택했다. index 13·15의 최초 429 응답 2건은 작업이 접수되지 않은 submission_failed이며 재접수 후 성공했다. 생성 작업 실패 수로 더하지 않는다. S10은 크림·립스틱만 보이고 향수는 없다. S09의 넓고 차가운 그림자는 약하므로 후속 I2V에서 그림자 이동 한 동작을 지정한다.

## 금융 근거

[금융 근거 4개 원본의 Drive 폴더](https://drive.google.com/drive/folders/1ZLTDk4vAniJ0Kht7scY6WZY75DG7k1CP)

- [세계 뷰티 시장 CAGR: 정의·기간·원문](research/beauty_cagr_primary.md)
- [ETF 공식 구성과 영상용 사업 역할 재분류](research/etf_composition_primary.md)
- [전체 구성표 CSV](research/holdings.csv) · [출처와 계산을 포함한 JSON](research/holdings.json)

맥킨지의 전망은 스킨케어·헤어케어·색조·향수의 세계 시장을 대상으로 하며 ETF 수익률 전망이 아니다. ETF 자료는 TIGER 화장품(2026-10-05), HANARO K-뷰티와 SOL 화장품TOP3플러스(각 2026-10-02)의 운용사 구성종목 PDF(설정·환매용 바스켓)를 담는다. 영상의 브랜드·ODM/OEM·유통·용기 비중은 제작진이 기업의 대표 사업 역할에 따라 합산한 값으로, 운용사의 표준 산업 섹터 통계나 매출 비중으로 읽지 않는다.

각 파일에 기준일·공식 URL·계산 방법을 보존했다. JSON의 원문 PDF 파일명과 해시는 출처 식별 정보이며, PDF 자체는 포함하지 않는다. 정확한 금융 숫자·상품명·출처는 검증된 근거로 후편집하고, 마을·모듈·바구니 토큰의 크기와 개수를 실제 비중으로 사용하지 않는다.
