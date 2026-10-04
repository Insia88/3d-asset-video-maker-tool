> 공개본에는 원본 이미지·영상과 로컬 관찰판을 포함하지 않는다. ‘로컬 관찰 근거’는 저장소에 재배포하지 않는 로컬 관찰 자료를 가리킨다. 공개 출처 링크와 관찰·제작 제안은 보존하며, 문서별 과거 수량보다 [프로젝트 감사 집계](<../../../data/projects/finfluencer-beauty-etf/audit.json>)와 [스냅샷 매니페스트](<../../../manifests/snapshot.json>)의 집계가 최신 기준이다.

# Atoon 3D — 귀여운 캐릭터와 디자인 변형 분석

검토일 2026-10-04. [제작자 공개 포트폴리오](<https://atoon3d.artstation.com/projects>)의 32개 원작 페이지를 각각 열었다. 17개 페이지에서 확보한 실제 정지 이미지 75장을 7개 식별자 보드로 모두 직접 관찰하고 독립 3D 디자인 14개를 채택했다. 나머지 61장은 동일 모델의 의상·표정·포즈·각도·크롭·리깅/클레이·기본형 독립성 미확정으로 제외했다. 영상만 있는 15개 페이지는 이 배치에서 재생을 분석하지 않았으며 집계는 0이다.

## 제작 근거와 관찰 구분

제작자 프로필은 3D Artist, Character Design, Animator로 소개한다. 개별 원작 본문은 Blender 모델링·리깅·텍스처·Eevee/Cycles 렌더와 일부 Marvelous Designer 의복을 명시한다. 이는 생성 AI 사용 증거가 아니며 전통 CG 비교자료로 기록했다. 공개 게시일은 미검증이고 CDN 숫자를 날짜로 추정하지 않는다.

[CG213 Santa](<https://atoon3d.artstation.com/projects/1NyldX>)는 과장 비례와 핸드페인트의 애니메이션/게임용 모델을 설명한다. [CG217](<https://atoon3d.artstation.com/projects/8BVVwm>)은 Blender 모델·텍스처·리깅과 옷/헤어 시뮬레이션, [CG224](<https://atoon3d.artstation.com/projects/aoyYQL>)는 Blender3.5/Cycles의 단편용 두 캐릭터, [CG230](<https://atoon3d.artstation.com/projects/nE5r2r>)은 Blender3.2 스컬프팅과 Marvelous Designer 의복을 설명한다. 정지 이미지에서 움직임·컷·BPM을 측정했다고 쓰지 않는다.

## 귀여움의 조형 문법

| 관찰 | 대표 | 차용 규칙 |
|---|---|---|
| 큰 얼굴·아주 작은 손발 | CG220, CG223, CG233, CG240 | 몸 비례를 먼저 잠그고 제품/소품과의 크기를 유지 |
| 큰 헤어/모자 외곽 | CG217 곱슬머리, CG220 두 방울 비니, CG228 산타 모자 | 외곽 특징 하나를 크게 두고 작은 부속은 줄임 |
| 얼굴의 분명한 색 구획 | CG225 고양이, CG236 레서판다 | 눈·코·볼의 대비를 한눈에 읽히게 설계 |
| 동물의 과장된 긴 외곽 | CG238 긴 목과 귀 | 늘씬한 목과 큰 귀를 고유 실루엣으로 새로 구성 |
| 의복 두 색과 반사 눈 | CG214 청록/분홍, CG223 분홍/보라 | 눈의 광택과 의복의 무광을 분리 |
| 커플/의상 시트를 한 단위로 | CG224 두 인물, CG231 두 의상 | 한 장의 구성과 같은 모델의 변형을 개별 수로 더하지 않음 |

## 교차 중복과 보류

CG212 선물 자루 산타는 CG213 산타 기본형의 워크사이클 정지 표본이라 CG213-A01 한 디자인으로 병합했다. CG222의 파란 비니 꼬마는 CG220의 같은 얼굴/몸 비례에 모자·의복만 바뀐 것으로 판단해 CG220-A01에 병합했다. CG225 고양이의 정장·하와이안 셔츠·칼라·사이보그 눈·의사복도 같은 얼굴 기본형 한 디자인으로 묶었다.

CG238 라마의 의복·포즈·머리 스카프·각도 16장을 한 디자인으로 묶었다. CG231의 검정 의상과 노란 드레스 역시 한 캐릭터 시트다. CG229 메이크업 팔레트/브러시 여성은 뷰티 적용 비교로 남겼지만 CG217과 기본형이 독립인지 충분히 검증하지 못해 추가 집계를 보류했다. 보류는 동일 모델이라고 확정한 판정과 다르다.

## Higgsfield 자산 설계 제안

아래는 정지 조형을 바탕으로 한 제작 제안이며 관찰된 영상 속도값이 아니다.

1. 새로운 뽀짝 캐릭터를 정면/옆/뒤로 확정한다. 큰 얼굴, 외곽 특징 하나, 작은 손발과 의복 주색 두 개를 먼저 결정한다.
2. 같은 캐릭터의 의상·표정·포즈는 변형 자산으로 묶는다. 고양이/팬아트의 얼굴을 재현하지 않고 비례·재질 대비·외곽의 원리만 적용한다.
3. 투명 제형 병이나 작은 ETF 바구니는 독립 제품 자산으로 만든다. 얼굴/손/제품 경계가 겹쳐 소실되는지를 첫 움직임 시험에서 확인한다.
4. 초기 움직임은 작은 고개 기울임과 한 손짓, 작은 카메라 전진으로 제한해 일관성을 확인한다. 정보·편입비중·출처 글자는 후편집에서 합성한다.

## 채택한 디자인

| ID | 실제 형상 | 재질·빛 | ETF/뷰티 응용 | 원작 |
|---|---|---|---|---|
| CG213-A01-S01 | 커다란 눈·흰 수염·둥근 안경·붉은 의복의 산타가 선물 상자를 들고 있다. | 붉은 매트 의복·흰 털·큰 광택 눈, 굵고 단순한 실루엣. | 직접 복제 대신 큰 머리/수염 대비 원리로 선물형 ETF 바구니 안내자 제작. | [원작](<https://atoon3d.artstation.com/projects/1NyldX>) · [이미지](<https://cdnb.artstation.com/p/assets/images/images/093/951/357/medium/atoon-animations-santa-2.webp?1764020490>) |
| CG214-A01-S01 | 큰 갈색 눈의 원숭이가 분홍 후드/테두리의 청록 집업과 검정 반바지를 입고 양손을 벌린다. | 갈색 털 덩어리·매트 의복·광택 눈, 청록과 분홍의 선명한 대비. | 제형 병이나 수출 상자를 양손에 든 새 동물 안내자 비례 참고. | [원작](<https://atoon3d.artstation.com/projects/zxGmD6>) · [이미지](<https://cdna.artstation.com/p/assets/images/images/091/854/162/medium/atoon-animations-asset.webp?1758009624>) |
| CG217-A02-S01 | 큰 눈·갈색 긴 곱슬머리의 여성이 흰 꽃무늬 크롭과 주황 플레어 스커트·긴 검정 부츠를 입는다. | 큰 곱슬머리 덩어리·매끄러운 피부면·가벼운 의복 주름, 흰/주황/검정. | 뷰티 소비자 역할을 맡는 새 스타일 캐릭터의 큰 얼굴/의복 색 대비 참고. | [원작](<https://atoon3d.artstation.com/projects/8BVVwm>) · [이미지](<https://cdnb.artstation.com/p/assets/images/images/089/981/255/medium/atoon-animations-asset.jpg?1752532519>) |
| CG220-A01-S01 | 큰 눈의 꼬마가 둥근 방울 두 개의 노란 비니·파란 멜빵·흰 티셔츠·분홍 신발을 입는다. | 매트 뜨개 비니와 파랑 의복, 큰 반사 눈, 짧은 팔다리. | 질문을 던지는 작은 관찰자, 두 방울 대신 고유 실루엣으로 재설계. | [원작](<https://atoon3d.artstation.com/projects/3EkLk2>) · [이미지](<https://cdnb.artstation.com/p/assets/images/images/088/863/941/medium/atoon-animations-asset.jpg?1749404689>) |
| CG223-A02-S01 | 주근깨·주황 양갈래의 꼬마가 분홍 티셔츠·달 무늬 보라 멜빵을 입고 초록 의자에 앉아 있다. | 둥근 광택 눈·매트 보라 의복·초록 의자, 머리카락의 큰 덩어리. | 작은 의자 위 제품 관찰자, 주색 두 개와 큰 헤어 형태를 먼저 고정. | [원작](<https://atoon3d.artstation.com/projects/Gv2a6V>) · [이미지](<https://cdnb.artstation.com/p/assets/images/images/083/949/891/medium/atoon-animations-asset.jpg?1737158830>) |
| CG224-A02-S01 | 파란 재킷의 갈색 피부 남성과 밝은 파랑 원숄더 드레스·올림머리 여성의 두 인물 디자인 시트. | 크고 반사하는 눈·매트 의복·간단한 피부면, 파랑 계열 두 실루엣. | 서로 다른 시각의 두 안내자를 한 세트로 구성하는 비례/색 대비. | [원작](<https://atoon3d.artstation.com/projects/aoyYQL>) · [이미지](<https://cdnb.artstation.com/p/assets/images/images/061/691/489/medium/atoon-animations-asset.jpg?1681401279>) |
| CG225-A01-S01 | 큰 귀·초록 눈·분홍 코·중앙 흰 줄무늬의 갈색 고양이가 검정 줄무늬 정장과 넥타이를 입는다. | 털 머리·유광 눈·매트 정장, 얼굴의 흰 중앙 띠가 먼저 읽힌다. | 고양이 얼굴을 복제하지 않고 명확한 얼굴 색 구획과 작은 의복 참고. | [원작](<https://atoon3d.artstation.com/projects/VJgEGP>) · [이미지](<https://cdna.artstation.com/p/assets/images/images/060/358/602/medium/atoon-animations-asset.jpg?1678380149>) |
| CG228-A02-S01 | 큰 눈·짧은 밝은 갈색 단발의 여성이 흰 가장자리의 붉은 산타 드레스와 모자를 입는다. | 단순 매트 의복·큰 광택 눈, 빨강과 흰색의 분명한 대비. | 큰 모자와 단순 의복으로 안내자 실루엣을 확정하는 비교. | [원작](<https://atoon3d.artstation.com/projects/B3Zbz9>) · [이미지](<https://cdna.artstation.com/p/assets/images/images/057/568/002/medium/atoon-animations-asset.jpg?1671997271>) |
| CG230-A03-S01 | 갈색 피부·짧은 금발 드레드의 청년이 검정 마스크 도안 주황 티셔츠·목걸이·검정 바지를 입는다. | 큰 헤어 묶음·매트 주황 의복·반사하는 금속 목걸이. | 스타일 소비자 보조 인물의 헤어 덩어리/옷 색 대비 참고. | [원작](<https://atoon3d.artstation.com/projects/nE5r2r>) · [이미지](<https://cdna.artstation.com/p/assets/images/images/053/856/912/medium/atoon-animations-untitled.jpg?1663178242>) |
| CG231-A02-S01 | 갈색 곱슬 단발의 같은 여성을 검정 크롭/반바지와 노란 꽃무늬 드레스 두 의상으로 나란히 보여 준다. | 큰 눈·둥근 입술·큰 곱슬 헤어 덩어리, 노랑과 검정 의복. | 의상 두 버전을 한 캐릭터 시트로 묶는 자산 관리 비교. | [원작](<https://atoon3d.artstation.com/projects/mzY2PY>) · [이미지](<https://cdnb.artstation.com/p/assets/images/images/051/887/141/medium/atoon-animations-asset.jpg?1658410363>) |
| CG233-A02-S01 | 큰 눈·검정 올림머리·붉은 리본의 작은 발레리나가 분홍 튀튀와 발레 신발을 입는다. | 짧은 팔다리·매트 피부·겹치는 튀튀, 분홍과 붉은 리본. | 꽃/제형을 소개하는 새 작은 캐릭터의 둥근 비례와 단순 주색. | [원작](<https://atoon3d.artstation.com/projects/1432WZ>) · [이미지](<https://cdna.artstation.com/p/assets/images/images/049/595/640/medium/atoon-animations-asset.jpg?1652861701>) |
| CG236-A01-S01 | 붉은 털·흰 귀/볼·검정 반점의 레서판다 머리가 걱정스러운 눈과 작은 이를 드러낸다. | 조밀한 털과 매끄러운 광택 눈/이, 주황/흰/검정 큰 구획. | 익숙한 팬아트는 복제하지 않고 털 덩어리와 감정 가독성 비교. | [원작](<https://atoon3d.artstation.com/projects/8woV4q>) · [이미지](<https://cdna.artstation.com/p/assets/images/images/048/774/044/medium/atoon-animations-asset.jpg?1650910811>) |
| CG238-A05-S01 | 큰 귀·큰 검정 눈·긴 얼굴과 목의 의인화 라마가 흰 꽃무늬 크롭과 청바지를 입는다. | 밝은 갈색 털·매트 의복·큰 반사 눈, 긴 목과 귀가 외곽을 정의한다. | 길고 단순한 목/귀 실루엣의 새 동물 안내자 제작 참고. | [원작](<https://atoon3d.artstation.com/projects/X1OG0a>) · [이미지](<https://cdna.artstation.com/p/assets/images/images/089/454/030/medium/atoon-animations-asset.jpg?1750990891>) |
| CG240-A04-S01 | 아주 큰 꿀색 눈·갈색 앞머리의 작은 꼬마가 수박 무늬의 연두 후드 원피스를 입는다. | 큰 머리와 작은 몸/발, 매트 후드와 유광 눈의 대비. | 제품보다 작은 뽀짝 안내자의 크기와 몸 비례 참고. | [원작](<https://atoon3d.artstation.com/projects/OmGdR8>) · [이미지](<https://cdnb.artstation.com/p/assets/images/images/044/363/765/medium/atoon-animations-asset.jpg?1639768802>) |

## 원작별 실제 관찰 범위

| 원작 | 정지 이미지 직접 관찰 | 채택 | 본문 제작 근거 |
|---|---:|---|---|
| [CG210 · 3D Stylized Character Animation](<https://atoon3d.artstation.com/projects/ndw9x1>) | 0 | 0 | SOMO XR 교육 사이트 광고용 캐릭터/환경 설계 전체 Blender 작업이라고 제작자 설명. |
| [CG211 · 3D SHORT TRIBUTE ANIMATION](<https://atoon3d.artstation.com/projects/3E591v>) | 0 | 0 | 고인을 기리는 가족 의뢰 애니메이션이라고 제작자 설명. 스틸 미확보, 영상 미관찰. |
| [CG212 · 3D Stylized character Animation](<https://atoon3d.artstation.com/projects/0lQBW5>) | 1 | 0 | 선물을 운반하는 Santa 워크사이클이라고 제작자 설명. |
| [CG213 · 3D Stylized Cartoon Santa Claus](<https://atoon3d.artstation.com/projects/1NyldX>) | 6 | A01 | 과장 비례·핸드페인트·애니메이션/게임용 Santa 모델이라고 제작자 설명; 판매 표기는 구매 실행 근거로 사용하지 않음. |
| [CG214 · 3D Monkey Avatar Commissioned for Commercial Advertising](<https://atoon3d.artstation.com/projects/zxGmD6>) | 1 | A01 | 상업 광고용 원숭이 마스코트 의뢰, 얼굴/몸 애니메이션이라고 제작자 설명. |
| [CG215 · 3D Stylized Character Walk Cycle Animation](<https://atoon3d.artstation.com/projects/8BdGgE>) | 0 | 0 | Blender 모델링과 워크사이클이라고 제작자 설명. 영상 미관찰. |
| [CG216 · 3D animation for an Upcoming Kids Educational Channel](<https://atoon3d.artstation.com/projects/8BdLRO>) | 0 | 0 | 어린이 교육 채널 애니메이션·캐릭터 리깅/모델링 담당이라고 제작자 설명. 영상 미관찰. |
| [CG217 · 3D Cute Stylized Character](<https://atoon3d.artstation.com/projects/8BVVwm>) | 7 | A02 | Blender 모델·텍스처·리깅과 워크사이클의 옷/헤어 시뮬레이션이라고 제작자 설명. |
| [CG218 · 3D Cute Stylized Character Walk Cycle](<https://atoon3d.artstation.com/projects/Ez88L0>) | 0 | 0 | Blender4.0 모델링/힐 워크사이클이라고 제작자 설명. 영상 미관찰. |
| [CG219 · 3D Avatar Animation For Hotel Bellboy](<https://atoon3d.artstation.com/projects/K3VkJX>) | 0 | 0 | 호텔 벨보이 의뢰 캐릭터 설계·리깅·얼굴/몸 애니메이션·보이스오버라고 제작자 설명. 영상 미관찰. |
| [CG220 · 3D Cute Character Animation](<https://atoon3d.artstation.com/projects/3EkLk2>) | 5 | A01 | Blender 캐릭터 모델링·얼굴/몸 리깅·소개 애니메이션이라고 제작자 설명. |
| [CG221 · 3D Love Story Animated Short Film](<https://atoon3d.artstation.com/projects/QKYWb4>) | 0 | 0 | Blender 전체 제작의 대사 없는 로맨스 단편이라고 제작자 설명. 영상 미관찰. |
| [CG222 · 3D Dance Animation || Blender 3D](<https://atoon3d.artstation.com/projects/3EPdAv>) | 3 | 0 | Blender 모델링·리깅·텍스처·춤/얼굴 애니메이션이라고 제작자 설명. |
| [CG223 · 3D Stylized Character Walk Cycle Animation](<https://atoon3d.artstation.com/projects/Gv2a6V>) | 2 | A02 | Blender 모델링·리깅·앉기/워크사이클이라고 제작자 설명. |
| [CG224 · 3D Stylized Character Design](<https://atoon3d.artstation.com/projects/aoyYQL>) | 7 | A02 | 제작 중 단편용 두 캐릭터를 Blender3.5 모델링·Cycles 렌더했다고 제작자 설명. |
| [CG225 · 3D NFT CAT](<https://atoon3d.artstation.com/projects/VJgEGP>) | 5 | A01 | Blender3.0 고양이 모델이라고 제작자 설명. NFT 판매/거래 조사 아님. |
| [CG226 · 3D Character Animation || Blender 3.0](<https://atoon3d.artstation.com/projects/8wQzNR>) | 0 | 0 | Blender3.0 애니메이션·Reverig/Faceit 얼굴 리깅·Rigify 몸 리깅이라고 제작자 설명. 영상 미관찰. |
| [CG227 · Christmas Santa Animation](<https://atoon3d.artstation.com/projects/EaAqVA>) | 0 | 0 | 크리스마스 Santa 의상 캐릭터 애니메이션이라고 제작자 설명. 영상 미관찰. |
| [CG228 · 3D Stylized Character || Christmas Santa](<https://atoon3d.artstation.com/projects/B3Zbz9>) | 4 | A02 | Blender3.0 Santa 캐릭터 모델링과 춤 애니메이션이라고 제작자 설명. |
| [CG229 · 3D Stylized Character Design](<https://atoon3d.artstation.com/projects/vJeWLx>) | 4 | 0 | Blender3.0 모델·헤어 그룸과 Eevee 렌더라고 제작자 설명. |
| [CG230 · 3D Stylized Character Design](<https://atoon3d.artstation.com/projects/nE5r2r>) | 3 | A03 | Blender3.2 스컬프팅·Marvelous Designer 의복·Cycles 렌더라고 제작자 설명. |
| [CG231 · 3D Character Design](<https://atoon3d.artstation.com/projects/mzY2PY>) | 4 | A02 | Blender3.2 모델/헤어 그룸과 Cycles 렌더라고 제작자 설명. |
| [CG232 · 3D Walk Cycle Animation](<https://atoon3d.artstation.com/projects/KO5V5G>) | 0 | 0 | Blender3.3 워크사이클 애니메이션이라고 제작자 설명. 영상 미관찰. |
| [CG233 · 3D Stylized Ballerina Character](<https://atoon3d.artstation.com/projects/1432WZ>) | 2 | A02 | Blender3.1 발레 모델/리깅/애니메이션과 Cycles 렌더라고 제작자 설명. |
| [CG234 · Stylized Character Animation](<https://atoon3d.artstation.com/projects/4Xqo9L>) | 0 | 0 | Blender3.0 발레 애니메이션이라고 제작자 설명. 영상 미관찰. |
| [CG235 · Stylized Character Animation](<https://atoon3d.artstation.com/projects/d0Pvn3>) | 0 | 0 | Blender3.0 캐릭터 점프/춤 애니메이션이라고 제작자 설명. 영상 미관찰. |
| [CG236 · Sculpting Turning Red Character in Blender 3.0](<https://atoon3d.artstation.com/projects/8woV4q>) | 1 | A01 | Blender 스컬프팅·헤어 그룸, Filmora9Pro 편집이라고 제작자 설명. |
| [CG237 · 3D NFT Model using Blender 3.0](<https://atoon3d.artstation.com/projects/B3ekx8>) | 0 | 0 | Blender3.0 스컬프팅·Cycles 렌더라고 제작자 설명. 영상 미관찰. |
| [CG238 · Lama Mama](<https://atoon3d.artstation.com/projects/X1OG0a>) | 16 | A05 | Blender3.0 라마 캐릭터 모델링이라고 제작자 설명. |
| [CG239 · Stylized Character || Run Cycle || Blender 3.0](<https://atoon3d.artstation.com/projects/JebkQd>) | 0 | 0 | Blender 런사이클 애니메이션이라고 제작자 설명. 영상 미관찰. |
| [CG240 · New character model](<https://atoon3d.artstation.com/projects/OmGdR8>) | 4 | A04 | 3D Character Minnie라는 제목/본문. 정확한 제작도구/AI 여부 미확인. |
| [CG241 · Walk Cycle || Blender 3.0 || Stylized](<https://atoon3d.artstation.com/projects/NGy8eP>) | 0 | 0 | Blender3.0 워크사이클과 Eevee 렌더라고 제작자 설명. 영상 미관찰. |

## 근거 파일

로컬 관찰 근거 · 로컬 관찰 근거 · 로컬 관찰 근거 · 로컬 관찰 근거.

영상만 있는 페이지와 실제 관찰 이미지를 구분하며, 판매/NFT 설명을 매매 요청이나 실행 근거로 취급하지 않는다.
