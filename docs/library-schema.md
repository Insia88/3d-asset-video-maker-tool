# 공개 3D 연구 라이브러리 스키마

이 라이브러리는 직접 관찰과 선별을 마친 3D 참고 자료의 출처·조형·재질·제작 적용을 기록한다. 이미지나 영상 원본을 제공하는 에셋 저장소가 아니며, 3D처럼 보이는 이미지가 편집 가능한 메시를 제공한다는 뜻도 아니다. 생성 모델, 제작 도구, 메시, 오디오는 원 연구에서 개별 확인한 주장만 보존한다.

스키마 버전은 `1.0`이다. 도구는 Python 표준 라이브러리만 사용하고 네트워크 요청이나 미디어 다운로드를 하지 않는다.

## 파일 배치

```text
data/projects/<project>/
  references/
    index.json
    part-00001.jsonl
    part-00002.jsonl
    ...
  audit.json
docs/research/<date>/
  00_...md
  01_...md
  ...
  shot-counting.md
  analysis-schema.md
  reference-index/
    3d_references_...md
manifests/snapshot.json
```

`project`는 소문자 영문·숫자·하이픈으로 구성하고, `date`는 `YYYY-MM-DD`로 지정한다. `manifests/snapshot.json`의 `projects` 객체는 프로젝트별 최신 스냅샷을 등록한다. 다른 프로젝트 항목은 보존하지만, 같은 날짜의 같은 문서 경로에 서로 다른 내용을 덮어쓰려는 내보내기는 중단한다.

## 내보내기

```bash
python tools/import_research.py \
  --source ../finfluencer-format-20261004 \
  --destination . \
  --project finfluencer-beauty-etf \
  --date 2026-10-04

python tools/validate_library.py \
  --destination . \
  --project finfluencer-beauty-etf
```

입력 폴더의 `shot_audit.json`과 `shots_master.jsonl`이 같은 완료된 감사 결과를 나타내야 한다. 전체 목표 수량에 도달하기 전에도 완료된 관찰분의 스냅샷을 내보낼 수 있다. 이 경우 `remaining`과 `project_completion_claim=false`를 그대로 기록한다.

내보낼 행은 마스터 원장의 `count_eligible=true`이면서 `canonical_class=core3D`인 고유 단위다. 혼합형·2D·미관찰 메타데이터·대표에 통합된 변형은 제외한다. 한 이미지의 패널·오브젝트·캐릭터 수나 하나의 연속 모핑 중간 캡처를 다시 분할하지 않는다. 도구는 새로 수량을 추정하거나 직접 시각 판정을 수행하지 않는다.

입력 감사의 총 행 수, 선정 수, 원장별 수, 데이터 품질 메모를 확인한다. 선택된 행의 ID·관찰 근거·실제 화면 설명도 확인하고, 읽는 동안 원장·감사·문서가 바뀌면 저장 전에 중단한다. 출력물을 임시 폴더에서 먼저 검증하고, 각 파일을 임시 파일 작성 후 교체한다. 스냅샷 매니페스트는 마지막에 저장한다. 여러 파일의 교체 전체가 하나의 파일시스템 트랜잭션은 아니므로 읽는 쪽은 매니페스트의 해시를 확인해야 한다.

## `references/index.json`과 JSONL 분할 파일

`references/index.json`이 전체 참고 목록을 등록한다. `schema_version`, `project`, `reference_format=sharded_jsonl`, `total_references`, `shard_count`, `max_rows_per_shard=1000`, `max_bytes_per_shard=16777216`을 가지며, `shards` 배열에 순서대로 `part-00001.jsonl`부터 등록한다. 각 항목은 파일 이름 `path`, 행 수 `rows`, 원본 파일 SHA-256 `sha256`, 크기 `bytes`를 가진다.

각 분할 파일은 최대 **1,000행과 16MiB** 두 제한을 모두 지킨다. 다음 행을 넣으면 어느 제한이든 넘는 경우 새 파일로 이어가며, 원래 참고 순서를 유지한다. 단일 연구 행 자체가 16MiB를 넘으면 손실 없이 분할할 수 없으므로 내보내기를 중단한다. 한 참고를 여러 행으로 나눠 수량을 늘리지 않는다. 분할 파일은 인덱스가 등록한 순서로 읽어야 한다. 단일 대형 `references.jsonl`은 생성하지 않는다.

각 part 파일은 UTF-8 JSON Lines 형식이며, 각 행은 원 연구의 고유 참고 단위 하나다.

| 필드 | 형식·의미 |
|---|---|
| `schema_version` | `1.0` |
| `reference_id` | 원 마스터의 `canonical_shot_id`; 프로젝트 안에서 고유 |
| `source_id` | 원 마스터의 `canonical_source_id` 우선, 없으면 기록된 원본 ID |
| `class` | 항상 `core3D`; 입력 원장의 시각 분류를 보존 |
| `count_eligible` | 항상 `true`; 완료된 감사에서 선정된 행만 수록 |
| `unit_type` | `still_image`, `video_scene`, `reference_unit_unspecified` |
| `source` | 원작 제목·제작자·공개 URL·기록된 날짜 |
| `observation` | 실제 관찰 상태·수준·방법·시간 구간·원래 관찰 세부 정보 |
| `visual` | 실제 화면 설명·구도·재질·색·미감·귀여움·기록된 카메라 변화 |
| `application` | 뷰티/ETF 적용, 서사 역할, Higgsfield 난이도·모션 제안 |
| `provenance` | 제작/AI 출처, 개별 모델/네이티브 도구 근거, 교차 검토 |
| `hashes` | 원장에 기록된 SHA-256; 원래 필드 경로와 값 유지 |
| `lineage` | 원장 파일 이름과 행 번호; 로컬 절대 경로는 없음 |
| `source_record` | 원래 연구 필드를 공개본으로 정리한 객체; 정규화에서 고르지 않은 항목도 보존 |

`source_record`는 연구 의미를 손실 없이 보존하는 확장 영역이다. 공통 항목은 읽기 쉬운 별도 영역에도 배치하지만, 원장의 서로 다른 이름이나 교차 검토 객체를 폐기하지 않는다. 원본 해시, 모델 검증의 정밀도, 관찰 프레임의 시간·종류, 영상 컷 경계의 불확실성, 권리 표기 등은 원래 표현으로 남긴다. 로컬 파일 경로·인증 정보·비공개 실행 응답은 공개 연구 내용이 아니므로 아래 정리 규칙을 적용한다.

`source.urls`는 기록에서 확인되는 공개 HTTP(S) URL을 원래 필드 이름과 함께 보존한다. 공개 URL이 없는 사용자 제공 원본에는 `public_url_status=user_provided_local_reference`를 기록하고 URL을 새로 만들지 않는다. 다른 사유로 URL이 기록되지 않았다면 `no_public_source_url_in_record`다. 공개 노출은 재사용 허가를 뜻하지 않는다.

`observation.timing`의 시작·종료 시각은 원래 숫자와 경계 근거를 유지한다. 1fps 대표 프레임, 경계 후보 검토, 전체 실시간 재생은 서로 다른 관찰이다. 정지 이미지의 움직임과 ETF 설명 적용은 제작 제안이며 관찰 사실로 바꾸지 않는다. 원래 단위를 확정할 수 없으면 `reference_unit_unspecified`로 남긴다.

`provenance.model_and_native_tool_evidence`는 실제 원장이 가진 모델 이름·근거·검증 수준·네이티브 도구·메시 확인 항목을 보존한다. 플랫폼명·검색어·프롬프트의 렌더러 이름으로 개별 모델을 채우지 않으며, 내보내기가 추가 검증을 했다는 표시도 하지 않는다. `cross_review`는 독립 검토와 원장에 있는 변형/출처 비교를 보존한다.

## 공개본 정리 규칙

원본 이미지·영상·관찰판·3D 모델 파일은 복사하지 않는다. 로컬 파일, 캐시, 첨부 파일의 경로 값은 `로컬 관찰 근거`로 바꾼다. 인증 토큰·키·쿠키·비공개 계정·대화/작업 식별자·원시 도구/캐시 응답은 제거한다. 인증 정보가 들어간 URL은 공개 URL로 취급하지 않는다. 원본의 정지 이미지 SHA-256은 보존하지만, 원본 파일 내용은 배포하지 않는다.

입력 폴더 바로 아래의 번호 붙은 Markdown 문서, `shot-counting.md`, `analysis-schema.md`를 내보낸다. `reference-index`에서는 현재 `36_3D_고유참고_통합색인.md`에 실제 연결된 문서만 선택해 이전 집계의 겹치는 분할 문서가 섞이지 않게 한다. 이 통합색인이 없는 입력은 전체 색인 문서를 선택하며 그 방식을 감사와 스냅샷에 기록한다. 로컬 그림·영상·관찰판 링크는 `로컬 관찰 근거` 텍스트로 바꾸고, 저장되는 연구 문서끼리의 링크는 상대 경로로 고친다. 개별 JSONL 원장 링크는 프로젝트의 `references/index.json`으로 연결한다. 그 밖의 내보내지 않는 로컬 파일 링크는 로컬 관찰 근거로 바꾼다. 공개 출처 URL은 보존하며, 외부 미디어의 이미지 임베드는 출처 링크로 바꾼다.

문서의 과거 집계·관찰 한계·제작 제안은 임의로 다시 쓰지 않는다. 공개 Markdown은 LF 줄바꿈·줄끝 공백 제거·마지막 개행 한 개로 저장해 Git에서도 파일 해시가 유지되게 한다. 코드 블록 밖의 두 칸 공백 줄바꿈은 `<br>`로 보존한다. 각 공개 문서 첫머리에 원본 미디어가 포함되지 않는다는 점과 최신 집계의 위치를 표시하고, 해당 문서 위치에서 `audit.json` 및 `manifests/snapshot.json`으로 상대 링크를 연결한다. ‘로컬 관찰 근거’는 저장소에 재배포하지 않는 로컬 관찰 자료를 뜻한다. 스냅샷의 권위 있는 현재 집계는 `audit.json`과 `manifests/snapshot.json`이다.

이전 스냅샷에 등록됐지만 새 출력에서 빠진 파일은 자동 삭제하지 않는다. `managed_file_cleanup`에서 같은 날짜·본 프로젝트 소유·기존 해시 일치·다른 프로젝트 미사용 조건을 만족한 정리 후보만 표시한다. 수정된 파일, 공유 파일, 다른 날짜의 기록은 보존한다.

## `audit.json`

프로젝트·날짜·목표·현재 선정 수·남은 수·완료 여부, 원장별 내보낸 수, 입력 원장/감사 SHA-256을 기록한다. `reference_format`, `reference_index`, `shard_count`도 기록하고 분할 인덱스·스냅샷의 값과 일치해야 한다. `source_audit`는 공개본으로 정리한 원래 감사 결과다. 여기의 과거 비교 유형 수는 비교 기록의 이력이며, 내보낸 참고 행에 혼합형이나 2D가 포함됐다는 뜻이 아니다.

`eligible_observed_units`와 `exported_references`는 전체 part 파일의 실제 JSONL 행 수 합계와 같아야 한다. `classes`는 `{"core3D": <행 수>}` 하나다. `remaining=max(0,target-행 수)`이며 목표를 충족한 경우에만 `project_completion_claim=true`다. `privacy_redactions`는 정리 유형별 개수만 기록하고 삭제한 비공개 값을 기록하지 않는다.

## `manifests/snapshot.json`

최상위 `schema_version`과 `projects`를 가진다. 프로젝트별 `references`는 분할 인덱스 경로를 가리키며 `reference_format`과 `shard_count`를 기록한다. 감사 파일 경로, 연구 문서 폴더·개수, 현재 선정 수, 입력 원장/감사 해시, 원 문서의 상대 이름·해시, 인덱스와 모든 part 파일을 포함한 출력 파일별 상대 경로·SHA-256·바이트 수도 기록한다. 로컬 소스 폴더의 절대 경로는 기록하지 않는다. 스냅샷 매니페스트 자신의 해시는 자기 참조를 피하기 위해 파일 목록에 넣지 않는다.

재내보내기는 현재 인덱스가 등록한 파일만 최신 자료로 정의한다. 이전 내보내기의 단일 JSONL이나 더 이상 등록되지 않은 파일은 자동 삭제하지 않는다. 기존 공개 저장소의 정리는 매니페스트를 확인한 관리자가 별도로 수행해야 한다.

## 검증 범위

`validate_library.py`는 다음 항목을 확인하고 문제가 있으면 종료 코드 `1`을 반환한다. 통과하면 종료 코드 `0`과 JSON 결과를 출력한다. `--project`를 생략하면 등록된 모든 프로젝트를 검증한다.

- 스냅샷·감사·JSONL의 집계와 원장별 행 수 일치
- 분할 인덱스의 순서·행 수·파일 수·해시·크기, 각 part의 1,000행/16MiB 제한과 전체 수 일치
- 고유 참고 ID, 순수 `core3D`, 원 감사의 선정 조건, 미병합 중복 여부
- 기록된 관찰 근거와 실제 화면 설명의 존재
- 원본 SHA-256 형식과 출력 파일의 SHA-256·크기 일치
- 로컬 절대 경로, 비공개 첨부/대화 식별자, 인증 정보, 임베디드 원시 페이로드 금지
- 매니페스트의 출력 범위, 원본 미디어 재배포 금지, 상대 내부 링크의 저장 파일 존재
- 목표·남은 수·완료 여부와 실제 행 수 일치

검증은 기록의 구조와 공개본 정합성을 확인한다. 이미지 픽셀을 다시 관찰하거나, 원본 저작권·모델·메시·금융 수치를 새로 확인하지 않는다. 실제 관찰 판단과 변형 통합은 원 연구 단계에서 수행해야 한다. 저장소 경로 옵션 `--root`는 `--destination`의 별칭이다.
