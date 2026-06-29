# 비대칭 PWM 제어 기반 직렬 공진형 컨버터의 소신호 모델링

논문 **「비대칭 PWM 제어 기반 직렬 공진형 컨버터의 소신호 모델링」**에서 제안한 APWM(Asymmetric PWM) 기반 SRC(Series Resonant Converter) 소신호 모델을 Python으로 재현한 프로젝트입니다.

Matlab 원본 코드의 모델 계산식을 Python으로 옮기고, PLECS 주파수 응답 데이터와 비교해 논문의 Fig.3, Fig.4 결과를 확인합니다.

## 재현 결과

### Fig.3 주파수 응답 결과

하나의 동작점에서 세 입력에 대한 출력전압 응답을 비교합니다.

- `Vg -> Vo`: 입력전압 변화에 대한 출력전압 응답
- `Duty -> Vo`: 듀티 변화에 대한 출력전압 응답
- `Frequency -> Vo`: 스위칭 주파수 변화에 대한 출력전압 응답

![Figure 3 frequency response](docs/images/figure3_frequency_response.png)

### Fig.4 제어(듀티)-출력 주파수 응답

스위칭 주파수를 고정하고, 부하 저항과 듀티 조건이 달라질 때의 `Duty -> Vo` 응답을 비교합니다.

- `Duty=0.361`, `R=5 ohm`
- `Duty=0.185`, `R=20 ohm`

![Figure 4 duty-to-output response](docs/images/figure4_duty_to_output.png)

## 실행 방법

Python 3.12 환경에서 확인했습니다. 먼저 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

그 다음 PyCharm 또는 터미널에서 아래 파일을 실행합니다.

```bash
python src/main_fig3.py
python src/main_fig4.py
```

각 실행 파일은 Matplotlib 그래프 창을 띄웁니다.

## 프로젝트 목적

직렬 공진형 컨버터는 공진 탱크의 전류와 전압이 스위칭 주파수 부근에서 교류 성분으로 동작합니다. 일반적인 상태공간 평균화만 적용하면 공진 회로의 동특성을 제대로 표현하기 어렵기 때문에, 논문에서는 EDF(Extended Describing Function)를 이용해 APWM 스위칭 파형과 정류단 비선형성을 근사합니다.

이 프로젝트는 논문의 모델링 흐름을 Python 코드로 정리해, Matlab/Python 모델과 PLECS 데이터의 주파수 응답을 비교하는 것을 목표로 합니다.

## 논문에서 다루는 회로와 APWM 파형

대상 회로는 풀브리지 직렬 공진형 컨버터입니다.

<p align="center">
  <img src="docs/images/paper_src_converter.png" alt="Full-Bridge Series Resonant Converter" width="560">
</p>

APWM 제어에서는 브리지 출력전압 `VAB`의 듀티를 비대칭으로 조절합니다. 논문에서는 이 파형을 DC 성분, sine 성분, cosine 성분으로 나누어 공진 회로 상태변수와 연결합니다.

<p align="center">
  <img src="docs/images/paper_apwm_vab_waveform.png" alt="APWM VAB waveform" width="560">
</p>

## 모델링 흐름

논문과 Matlab 코드의 계산 흐름은 아래와 같이 정리할 수 있습니다.

```text
비선형 SRC 상태방정식
  -> APWM VAB 파형의 EDF 근사
  -> 정류단 비선형 항의 EDF 근사
  -> 정상상태 전압/전류 계산
  -> 소신호 계수 계산
  -> 상태공간 행렬 A, B, C, D 구성
  -> 입력별 전달함수 추출
  -> Matlab/Python 모델과 PLECS 주파수 응답 비교
```

Python 코드에서는 이 흐름이 다음 파일로 나뉩니다.

| 단계 | Python 파일 |
| --- | --- |
| 동작점 및 파생 파라미터 계산 | `src/parameters.py` |
| APWM 계수와 상태공간 행렬 계산 | `src/apwm_model.py` |
| 전달함수의 주파수 응답 계산 | `src/frequency_response.py` |
| PLECS CSV 데이터 로드 | `src/plecs.py` |
| Fig.3/Fig.4 그래프 출력 | `src/main_fig3.py`, `src/main_fig4.py` |

## 기준 파일

`data/` 폴더는 Python 구현의 기준이 되는 Matlab 코드와 PLECS 검증 데이터를 담고 있습니다.

| 파일 | 역할 |
| --- | --- |
| `data/cal_parameter_APWM.m` | APWM 소신호 계수, A/B/C/D 행렬, 전달함수 계산의 Matlab 기준 코드 |
| `data/Control_to_Output_Duty_Paper.m` | Fig.4 조건과 Matlab plotting 흐름 기준 |
| `data/CCM_Vg_APWM_D0.361_F1.05_R5_Vo200.csv` | Fig.3 `Vg -> Vo` PLECS 데이터 |
| `data/CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv` | Fig.3/Fig.4 `Duty -> Vo`, `R=5 ohm` PLECS 데이터 |
| `data/CCM_W_APWM_D0.361_F1.05_R5_Vo200.csv` | Fig.3 `Frequency -> Vo` PLECS 데이터 |
| `data/CCM_D_APWM_D0.185_F1.05_R20_Vo200.csv` | Fig.4 `Duty -> Vo`, `R=20 ohm` PLECS 데이터 |

## 파라미터 기준

논문 표에는 시스템 파라미터가 아래와 같이 제시되어 있습니다.

| 파라미터 | 논문 표 기준 |
| --- | --- |
| `Vg` | `120 V` |
| `Vo` | `200 V` |
| `L` | `198 uH` |
| `C` | `51 nF` |
| `Cf` | `32 uF` |
| `RL` | `20 ohm / 5 ohm` |

현재 저장소의 Python 코드는 `data/`에 포함된 Matlab/PleCS 검증 파일을 그대로 재현하는 것을 우선합니다. 따라서 실제 실행 기준은 아래와 같습니다.

| 파라미터 | 실행 코드 기준 |
| --- | --- |
| `Vg` | `400 V` |
| `Vo` | `200 V` |
| `L` | `197 uH` |
| `C` | `51 nF` |
| `Cf` | `32 uF` |
| `rs` | `1e-3 ohm` |
| `rc` | `1e-3 ohm` |
| `Fsn` | `1.05` |
| `RL` | `5 ohm`, `20 ohm` |

이 값들은 `src/parameters.py`와 `data/Control_to_Output_Duty_Paper.m`의 값을 기준으로 맞춰져 있습니다. 논문 표와 일부 값이 다르지만, 현재 프로젝트의 목적은 포함된 Matlab/PleCS 검증 데이터와 Python 코드가 같은 조건에서 비교되도록 하는 것입니다.

## 프로젝트 구조

```text
.
├── data/          Matlab 기준 코드와 PLECS CSV 데이터
├── docs/images/   README에 사용하는 이미지
└── src/           Python 구현 코드
```

## 참고 사항

- `data/`의 Matlab 코드와 PLECS CSV는 검증 기준이므로 수정하지 않습니다.
- Matlab은 입력 번호가 1부터 시작하지만, Python-control은 0부터 시작하므로 전달함수 추출 시 index를 변환합니다.
- Matlab 기준 입력 번호는 `1=Vg`, `2=Duty`, `3=Frequency`, `4=Io`입니다.
- PLECS CSV의 마지막 주파수는 `26.37 kHz`이므로 그래프도 해당 범위까지만 표시합니다.
- PLECS와 Python-control은 같은 phase를 360도 차이로 표현할 수 있어, 그래프 표시 단계에서만 phase를 PLECS 기준으로 정렬합니다.
