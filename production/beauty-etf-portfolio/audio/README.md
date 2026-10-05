# 132BPM 오리지널 음악의 출처

이 음악은 뷰티 ETF 영상의 180초 흐름을 위해 새로 작성한 원곡이다. 132BPM, 4/4박자에 드럼과 베이스, 뮤트 기타, 짧은 마림바·클라비넷 구절을 배치했다. 기존 녹음의 속도를 바꾸거나 기존 곡을 인용하지 않았으며, 보컬과 내레이션은 사용하지 않았다.

음표와 리듬 이벤트는 [FluidSynth](https://www.fluidsynth.org/)로 렌더링했고, S. Christian Collins의 **GeneralUser GS 2.0.3** 음색을 사용했다. [GeneralUser GS License 2.0](https://github.com/mrbumpy409/GeneralUser-GS/blob/main/documentation/LICENSE.txt)은 개인·상업적 음악 제작을 허용한다. 동시에 제작자는 일부 음색이 오래된 무료 SoundFont에서 이어졌으며 모든 샘플의 최초 출처를 완전히 확인하지 못했다고 밝힌다. 이 기록은 해당 라이선스와 출처의 한계를 함께 남긴다. 개별 샘플의 권리를 모두 독립적으로 추적했다는 의미는 아니다.

| 파일 | 바이트 | SHA-256 |
|---|---:|---|
| beauty-etf-bright-funk-132bpm-180s.wav | 51,840,102 | `8f7657d518b7767a639a67e670c7dd7ab690732beb44979183b25aa8c1f80d56` |
| beauty-etf-bright-funk-132bpm-180s.mp3 | 5,761,581 | `52344c1e1a257c0b48d6919ddeb406e3f08e1135d78d6e86685a629c5bd171ec` |
| beauty-etf-bright-original-132bpm.mid | 39,110 | `abc31a60ddbf827ae396ced68ac6e410a0f757b5ddfd174ab4dd54a01b568efd` |
| beauty-etf-bright-score-source.zip | 53,473,649 | `d7a6ec8425583c75fbce3147e88f109378754e7878dc7f36af121987008cb39d` |

WAV는 48kHz 스테레오 24비트, 정확히 180초이며 측정 음량은 −16.01LUFS, 최대 true peak는 −1.19dBTP다. MP3는 48kHz 스테레오 256kbps, −16.41LUFS와 −1.47dBTP다. MP3 컨테이너에는 인코더 패딩이 있어 180.024초로 표시되며, 영상에는 180초로 맞춰 사용한다.

WAV 음량은 완성 파일을 다시 입력한 FFmpeg loudnorm 분석의 input_i·input_tp 통계다. 해당 분석 기록의 추가 정규화 output 값과 구분한다.

소스 ZIP은 콘텐츠 12개와 제작 영수증 1개를 합친 13파일이며 CRC와 파일 해시를 확인했다. 180초 WAV, 18초 비교 MP3 두 종, 음표·박자 자료, 렌더 스크립트와 음색 라이선스를 담았다. 최종 180초 MP3와 MIDI는 별도 파일이며 ZIP에 들어 있지 않다. SoundFont 음색 은행 자체는 재배포하지 않았다.

편곡은 0–18초의 도입, 18–50초의 수출·시장 설명, 50–78초의 사업 역할, 78–118초의 ETF 바구니, 118–152초의 위험, 152–180초의 결론에 맞춰 변한다. 수치를 읽는 구간에서는 주선율을 덜어 내고, 마지막에는 주요 후크와 짧은 종결 악센트를 둔다.

WAV와 MP3의 전체 디코딩에서 오류는 없었다. 전곡과 짧은 비교본을 실제로 청취한 검수는 수행하지 않았으므로, 이 기술 기록만으로 음악의 밝기나 반복감·잡음에 대한 청취 평가를 대신하지 않는다.
