# APWM 직렬 공진형 컨버터 소신호 모델링

비대칭 PWM(Asymmetric PWM, APWM) 제어 기반 직렬 공진형 컨버터(Series Resonant Converter, SRC)의 소신호 모델을 Python으로 구현한 프로젝트입니다.

Matlab 기준 소신호 모델을 Python 코드로 옮기고, PLECS CSV 데이터와 비교해 논문의 Fig.3/Fig.4 주파수 응답을 재현했습니다.

## 모델링 배경

대상 회로는 풀브리지 직렬 공진형 컨버터입니다. SRC는 공진 인덕터 `L`과 공진 커패시터 `C`를 이용해 스위칭 주파수 부근에서 에너지를 전달하며, 소프트 스위칭을 통해 스위칭 손실을 줄일 수 있습니다.

<p align="center">
  <img src="docs/images/paper_src_converter.png" alt="Full-Bridge Series Resonant Converter" width="560">
</p>

<p align="center"><b>풀브리지 직렬 공진형 컨버터 회로</b></p>

일반적인 상태공간 평균화는 한 주기 평균값을 중심으로 모델을 만들기 때문에, 공진 탱크의 교류 성분을 충분히 표현하기 어렵습니다. 이 논문은 APWM으로 구동되는 SRC를 CCM 조건에서 해석하고, 공진 성분을 보존하기 위해 EDF(Extended Describing Function)를 사용합니다.

<p align="center">
  <img src="docs/images/paper_apwm_vab_waveform.png" alt="APWM VAB waveform" width="560">
</p>

<p align="center"><b>APWM 제어에 따른 브리지 출력전압 VAB 파형</b></p>

## 논문 이론 정리

APWM 제어에서는 브리지 출력전압 `VAB`의 듀티를 비대칭으로 조절합니다. 듀티가 변하면 `VAB`의 기본파 성분과 DC 성분이 함께 변하고, 이 변화가 공진 탱크 전류와 출력전압 응답에 영향을 줍니다.

논문에서 사용하는 모델링 핵심은 다음과 같습니다.

| 구분 | 내용 |
| --- | --- |
| 비선형 상태방정식 | `VAB`, 공진 전류 `i`, 공진 커패시터 전압, 출력 필터 전압을 포함한 SRC의 비선형 방정식을 세움 |
| EDF 근사 | `VAB`, `sgn(i) * vCf`, `|i|` 같은 비선형 항을 DC, sine, cosine 성분으로 근사 |
| APWM 특성 | APWM의 `VAB` 파형은 기본파 성분뿐 아니라 DC 성분도 포함하므로 이를 별도로 반영 |
| 선형화 | 정상상태 주변에서 변동분을 잡고 A/B/C/D 상태공간 행렬을 구성 |
| 전달함수 | 상태공간 모델에서 `Vg -> Vo`, `D -> Vo`, `W -> Vo` 전달함수를 추출해 주파수 응답을 계산 |

EDF를 적용하면 공진 탱크의 상태를 평균값 하나로 없애지 않고, sine/cosine 성분으로 나누어 다룰 수 있습니다. 이 때문에 듀티 변화와 스위칭 주파수 변화가 공진 전류, 공진 커패시터 전압, 출력전압에 미치는 영향을 주파수 영역에서 확인할 수 있습니다.

## 소신호 모델링 과정

Python 코드의 계산 흐름은 다음과 같습니다.

```text
동작 조건 설정
  -> 공진주파수와 스위칭 주파수 계산
  -> 정상상태 전압/전류 계산
  -> APWM EDF 기반 소신호 계수 계산
  -> 상태공간 행렬 A, B, C, D 구성
  -> 입력별 전달함수 추출
  -> Python Bode 응답과 PLECS CSV 비교
```

Matlab 기준 함수 `cal_parameter_APWM.m`에서 계산하던 정상상태 값, APWM 계수, A/B/C/D 행렬, 전달함수 계산을 Python 코드로 분리해 구현했습니다.

| 논문/Matlab 계산 | Python 구현 |
| --- | --- |
| 공진주파수, 스위칭 주파수, 정상상태 계산 | `src/parameters.py` |
| EDF 기반 APWM 계수 계산 | `src/apwm_model.py` |
| A/B/C/D 상태공간 행렬 구성 | `src/apwm_model.py` |
| 입력별 전달함수 추출 | `src/apwm_model.py` |
| Bode gain/phase 계산 | `src/frequency_response.py` |
| PLECS CSV와 그래프 비교 | `src/plecs.py`, `src/plot.py` |

## 시뮬레이션 결과

### Fig.3: 입력별 출력 응답

`D=0.361`, `Fsn=1.05`, `R=5 ohm` 조건에서 입력전압, 듀티, 주파수 변화가 출력전압 `Vo`에 미치는 응답을 비교합니다.

| 입력 | 의미 | PLECS 데이터 |
| --- | --- | --- |
| `Vg` | 입력전압 -> 출력전압 | `CCM_Vg_APWM_D0.361_F1.05_R5_Vo200.csv` |
| `D` | 듀티 -> 출력전압 | `CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv` |
| `W` | 주파수 -> 출력전압 | `CCM_W_APWM_D0.361_F1.05_R5_Vo200.csv` |

![Figure 3 frequency response](docs/images/figure3_frequency_response.png)

### Fig.4: 부하 조건별 Duty-to-Output 응답

`Fsn=1.05` 조건에서 부하와 듀티가 다른 두 케이스의 `D -> Vo` 응답을 비교합니다.

| Duty | Load | PLECS 데이터 |
| --- | --- | --- |
| `0.361` | `5 ohm` | `CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv` |
| `0.185` | `20 ohm` | `CCM_D_APWM_D0.185_F1.05_R20_Vo200.csv` |

![Figure 4 duty-to-output response](docs/images/figure4_duty_to_output.png)

## 실행

Python 3.12 환경에서 확인했습니다.

```bash
pip install -r requirements.txt
python src/main_fig3.py
python src/main_fig4.py
```

## 파라미터 기준

현재 Python 코드는 `data/`에 포함된 Matlab/PLECS 기준 조건에 맞춰 실행됩니다.

| 파라미터 | 값 |
| --- | --- |
| `Vg` | `400 V` |
| `Vo` | `200 V` |
| `L` | `197 uH` |
| `C` | `51 nF` |
| `Cf` | `32 uF` |
| `rs` | `1e-3 ohm` |
| `rc` | `1e-3 ohm` |
| `Fsn` | `1.05` |
| `R` | `5 ohm`, `20 ohm` |

## 코드 구조

| 파일 | 역할 |
| --- | --- |
| `src/parameters.py` | 동작점, 공진주파수, 정상상태 전압/전류 계산 |
| `src/apwm_model.py` | Matlab `cal_parameter_APWM.m`의 APWM 계수, A/B/C/D 행렬, 전달함수 계산 |
| `src/frequency_response.py` | 전달함수의 gain/phase 계산, PLECS 기준 phase 정렬 |
| `src/plecs.py` | PLECS CSV 로드 |
| `src/plot.py` | gain/phase 그래프 출력 |
| `src/main_fig3.py` | Fig.3 실행 |
| `src/main_fig4.py` | Fig.4 실행 |

## 데이터 구조

| 파일 | 역할 |
| --- | --- |
| `data/cal_parameter_APWM.m` | APWM 소신호 모델의 Matlab 기준 코드 |
| `data/Control_to_Output_Duty_Paper.m` | Fig.4 조건과 Matlab plotting 기준 |
| `data/CCM_Vg_APWM_D0.361_F1.05_R5_Vo200.csv` | Fig.3 `Vg -> Vo` PLECS 데이터 |
| `data/CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv` | Fig.3/Fig.4 `D -> Vo`, `R=5 ohm` PLECS 데이터 |
| `data/CCM_W_APWM_D0.361_F1.05_R5_Vo200.csv` | Fig.3 `W -> Vo` PLECS 데이터 |
| `data/CCM_D_APWM_D0.185_F1.05_R20_Vo200.csv` | Fig.4 `D -> Vo`, `R=20 ohm` PLECS 데이터 |

## 참고 사항

- `data/`의 Matlab 코드와 PLECS CSV는 검증 기준이므로 수정하지 않습니다.
- Matlab 입력 번호는 `1=Vg`, `2=D`, `3=W`, `4=Io`입니다.
- Python-control은 0부터 index가 시작하므로 코드에서 입력 index를 변환합니다.
- PLECS CSV의 마지막 주파수는 `26.37 kHz`이므로 그래프도 해당 범위까지만 표시합니다.
- PLECS와 Python-control의 phase 표현이 360도 단위로 다를 수 있어, 그래프 표시 단계에서만 phase를 정렬합니다.
