# APWM 직렬 공진형 컨버터 소신호 모델링

비대칭 PWM(Asymmetric PWM, APWM) 제어 기반 직렬 공진형 컨버터(Series Resonant Converter, SRC)의 소신호 모델을 Python으로 구현한 프로젝트입니다. Matlab 기준 코드의 계산식을 Python으로 옮기고, PLECS 주파수 응답 데이터와 비교해 논문의 Fig.3/Fig.4 결과를 재현했습니다.

## 이 프로젝트에서 확인할 수 있는 것

- 논문 Fig.3 재현: `Vg -> Vo`, `Duty -> Vo`, `Frequency -> Vo` 주파수 응답
- 논문 Fig.4 재현: 부하 조건별 `Duty -> Vo` 주파수 응답
- Matlab 코드 기반 APWM 소신호 모델의 Python 변환
- PLECS CSV 데이터와 Python 전달함수 결과 비교

## 재현 결과

### Fig.3 주파수 응답 결과

하나의 동작점에서 입력 종류에 따른 출력 전압 응답을 비교합니다.

![Figure 3 frequency response](docs/images/figure3_frequency_response.png)

### Fig.4 제어(듀티)-출력 주파수 응답

부하 저항과 듀티 조건이 달라질 때의 `Duty -> Vo` 응답을 비교합니다.

![Figure 4 duty-to-output response](docs/images/figure4_duty_to_output.png)

## 실행 방법

PyCharm 또는 터미널에서 아래 파일을 실행하면 됩니다.

```bash
python src/main_fig3.py
python src/main_fig4.py
```

각 실행 파일은 Matplotlib 그래프 창을 띄웁니다.

## 프로젝트 구조

```text
.
├── data/          Matlab 기준 코드와 PLECS CSV 데이터
├── docs/images/   README에 사용하는 이미지
└── src/           Python 구현 코드
```

| 파일 | 역할 |
| --- | --- |
| `src/parameters.py` | 동작점과 파생 파라미터 계산 |
| `src/apwm_model.py` | APWM 소신호 계수, 상태공간 행렬, 전달함수 계산 |
| `src/frequency_response.py` | Bode gain/phase 계산 및 PLECS 기준 phase 정렬 |
| `src/plecs.py` | PLECS CSV 데이터 로드 |
| `src/plot.py` | gain/phase 그래프 출력 유틸 |
| `src/main_fig3.py` | Fig.3 재현 실행 파일 |
| `src/main_fig4.py` | Fig.4 재현 실행 파일 |

## 논문 기반 모델링 개요

대상 회로는 풀브리지 직렬 공진형 컨버터입니다.

<p align="center">
  <img src="docs/images/paper_src_converter.png" alt="Full-Bridge Series Resonant Converter" width="560">
</p>

APWM 제어에서는 브리지 전압 `VAB`의 듀티를 비대칭으로 조절합니다. 논문에서는 이 스위칭 파형을 EDF(Extended Describing Function)로 근사하여 DC 성분, sine 성분, cosine 성분으로 나누고, 이를 공진 회로의 상태변수와 연결합니다.

<p align="center">
  <img src="docs/images/paper_apwm_vab_waveform.png" alt="APWM VAB waveform" width="560">
</p>

전체 모델링 흐름은 다음과 같습니다.

```text
비선형 SRC 상태방정식
  -> APWM 파형과 정류단 비선형성의 EDF 근사
  -> 정상상태 해 계산
  -> 소신호 선형화
  -> 상태공간 행렬 A, B, C, D 구성
  -> 입력별 전달함수 추출
  -> PLECS CSV와 주파수 응답 비교
```

## 논문 시스템 파라미터

논문 표에 제시된 시스템 파라미터는 아래와 같습니다.

| 파라미터 | 값 |
| --- | --- |
| `Vg` | `120 V` |
| `Vo` | `200 V` |
| `L` | `198 uH` |
| `C` | `51 nF` |
| `Cf` | `32 uF` |
| `RL` | `20 ohm / 5 ohm` |

이 저장소의 Python 재현은 `data/`에 포함된 Matlab/PLECS 검증 파일을 기준으로 실행합니다. 실제 실행에 사용되는 값은 `src/parameters.py`와 `data/cal_parameter_APWM.m`에서 확인할 수 있습니다.

## 기준 데이터

| 파일 | 역할 |
| --- | --- |
| `data/cal_parameter_APWM.m` | APWM 모델 파라미터와 상태공간 행렬의 Matlab 기준 코드 |
| `data/Control_to_Output_Duty_Paper.m` | Fig.4 제어(듀티)-출력 비교용 Matlab 기준 코드 |
| `data/CCM_Vg_APWM_D0.361_F1.05_R5_Vo200.csv` | `Vg -> Vo` PLECS 데이터 |
| `data/CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv` | `Duty -> Vo`, `R=5 ohm` PLECS 데이터 |
| `data/CCM_W_APWM_D0.361_F1.05_R5_Vo200.csv` | `Frequency -> Vo` PLECS 데이터 |
| `data/CCM_D_APWM_D0.185_F1.05_R20_Vo200.csv` | `Duty -> Vo`, `R=20 ohm` PLECS 데이터 |

## 참고 사항

- `data/`의 Matlab 코드와 PLECS CSV는 검증 기준이므로 수정하지 않습니다.
- Matlab은 입력 번호가 1부터 시작하지만, Python-control은 0부터 시작하므로 전달함수 추출 시 index를 변환합니다.
- PLECS CSV의 마지막 주파수는 `26.37 kHz`이므로 그래프도 해당 범위까지만 표시합니다.
- PLECS와 Python-control은 같은 phase를 360도 차이로 표현할 수 있어, 그래프 표시 단계에서만 phase를 PLECS 기준으로 정렬합니다.
