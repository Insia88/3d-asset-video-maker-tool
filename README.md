# 3D Asset Video Maker Tool

첫 프로젝트의 최종 산출물은 **핀플루언서 지원용 약 3분짜리 뷰티 ETF 소개 영상**입니다. 귀엽고 미감 좋은 3D와 빠른 전개로 뷰티 제품에서 기업·ETF 설명으로 시선을 연결하고, 금융 내용을 이해하기 쉽게 전달합니다.

PLUS KR·슈카친구들 포맷 분석, 25,000개 참고 수집, Higgsfield 에셋 설계는 이 영상의 설명력과 연출을 위한 제작 과정입니다. 최종 영상에 채택할 참고와 컷에는 뷰티 ETF 설명에서 맡을 역할을 명시합니다. 채널의 전달 방식·호흡을 참고하면서 지원자의 금융 설명력과 독자적인 시각 연출을 함께 보여 줍니다.

## 바로 보기

- [진행 현황과 실제 완료 수](data/projects/finfluencer-beauty-etf/audit.json)
- [채널 포맷·3D 조사 종합](docs/research/2026-10-05/00_포맷분석_종합.md)
- [PLUS KR A–Z 분석](docs/research/2026-10-05/01_PLUS_KR_A-Z.md)
- [슈카친구들·머니코믹스 A–Z 분석](docs/research/2026-10-05/02_슈카친구들_A-Z.md)
- [고유 3D 참고 색인](docs/research/2026-10-05/36_3D_고유참고_통합색인.md)
- [뷰티 ETF 기초 에셋 설계](docs/research/2026-10-05/17_3D_기초에셋_설계.md)
- [보송한 질감·노을빛·창가 구도의 시각 방향](docs/beauty-etf-visual-direction.md)
- [기초 에셋 프롬프트](prompts/beauty-etf/foundation.json)
- [반복 작업 순서](docs/workflow.md) · [Higgsfield 세팅 순서](docs/higgsfield-foundation.md)

## 현재 프로젝트의 범위

영상의 흐름은 **뷰티에 대한 관심 → 관련 기업·사업 → 선택한 ETF의 구성 → 확인할 기준과 위험 → 한 줄 결론**을 중심으로 설계합니다. 실제 ETF 상품은 확정 전이며, 상품·기업·비중·비용·위험에 관한 문구는 운용사·공시 원문을 확인한 뒤 대본에 적용합니다. 약 3분은 현재 제작 목표이며 실제 지원 규정은 별도로 확인합니다.

**3D만, 뷰티 소재 우선.** 미감이 좋거나 귀엽고 뽀짝한 입체 캐릭터·제품·미니어처·공간을 선별합니다. 목표는 직접 관찰한 고유 장면·샷·정지 이미지 **25,000개**입니다. 완료 수는 `audit.json`의 `eligible_observed_units`, 남은 수는 `remaining`으로 확인합니다. 현재 수집은 진행 중이며 목표 달성 전입니다. Higgsfield MCP의 마스터 생성·Element 등록은 수집 완료 뒤 실행합니다.

전체 정지 이미지 한 장·모델 시트 한 장은 한 단위입니다. 같은 캐릭터나 공간의 색상·복장·작은 구도 변형, 재게시·동일 픽셀은 대표로 묶습니다. 원작의 AI 제작 주장·생성 모델 표시와 실제 화면의 3D 스타일 판정은 각각 기록합니다. 이미지의 3D 스타일만으로 편집 가능한 메시·리깅이 있다고 판단하지 않습니다.

## 저장 구조

```text
docs/
  workflow.md                  조사 → 선별 → 검증 → 생성 → 편집
  higgsfield-foundation.md      마스터·Element·파생 이미지 순서
  library-schema.md            원장 필드와 집계 조건
  decisions.md                 채택한 범위와 변경 규칙
  research/2026-10-05/          최신 채널 A–Z와 실제 3D 관찰 보고서
data/projects/finfluencer-beauty-etf/
  references/index.json        원장 묶음의 개수·경로·해시
  references/part-*.jsonl       전역 중복 제거 후 선정된 참고 원장
  audit.json                  실제 완료 수·제외 수·미완료 상태
manifests/
  snapshot.json                내보내기 시점과 원장 해시
prompts/beauty-etf/
  foundation.json              8개 기초 마스터와 생성 의존 관계
tools/
  import_research.py           로컬 조사에서 공개 기록 가져오기
  validate_library.py          집계·원장·링크·공개 경로 검사
```

## 자료 추가하기

Python 3에서 실행합니다. 로컬 조사 폴더의 최신 감사가 끝난 뒤 가져오며, 실제 관찰·선정된 원장만 완료 수에 반영합니다.

```sh
python tools/import_research.py --source /path/to/research --destination . --project finfluencer-beauty-etf --date 2026-10-05
python tools/validate_library.py --root . --project finfluencer-beauty-etf
```

검증 후 추가 자료를 Git 커밋으로 누적합니다. GitHub의 push·pull request마다 같은 검증을 자동 실행합니다. 새 프로젝트에는 별도 `data/projects/<project>/`와 날짜별 조사 문서를 사용합니다. 기존 프로젝트의 근거를 수정할 때는 수정 이유와 집계 변화를 함께 기록합니다.

## 출처와 재사용

각 관찰에는 원작 URL과 가능한 경우 개별 이미지 URL·원본 해시·확인한 모델 표시·독립 교차 검토를 연결합니다. 로컬 관찰판과 원본 영상은 로컬 증거로 관리합니다. 공개 저장소에는 분석·출처·설계·검증 도구를 담습니다. 제3자 에셋의 다운로드와 영상 사용은 개별 원작의 라이선스·귀속 조건을 확인합니다. 서로 다른 플랫폼의 같은 원본을 새 참고로 추가하지 않습니다.

ETF 상품·보유 기업·비중·비용·기준일은 실제 운용사·공시 원문을 확인한 뒤 대본에 적용합니다. 현재 기초 에셋의 다섯 기업 토큰과 색채는 제작용 예시입니다.
