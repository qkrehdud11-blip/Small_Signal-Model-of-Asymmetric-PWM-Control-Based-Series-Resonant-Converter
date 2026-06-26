# APWM SRC 회로 파라미터 계산 파일
# MATLAB의 cal_parameter_APWM.m 역할을 Python으로 옮기기 위한 기본 구조입니다.

import numpy as np


def calculate_parameters():
    """
    APWM 기반 직렬 공진형 컨버터의 기본 파라미터를 계산합니다.
    이후 apwm_model.py에서 전달함수 계산에 사용됩니다.
    """

    # 입력 전압 [V]
    vin = 390

    # 출력 전압 [V]
    vo = 200

    # 출력 전력 [W]
    po = 2000

    # 부하 저항 [ohm]
    r_load = vo ** 2 / po

    # 공진 인덕터 [H]
    lr = 33e-6

    # 공진 커패시터 [F]
    cr = 22e-9

    # 공진 주파수 [Hz]
    fr = 1 / (2 * np.pi * np.sqrt(lr * cr))

    # 스위칭 주파수 [Hz]
    fs = 1.05 * fr

    # 각주파수 [rad/s]
    wr = 2 * np.pi * fr
    ws = 2 * np.pi * fs

    # 정규화 주파수
    fn = fs / fr

    # 특성 임피던스 [ohm]
    zo = np.sqrt(lr / cr)

    # 품질 계수
    q = zo / r_load

    return {
        "vin": vin,
        "vo": vo,
        "po": po,
        "r_load": r_load,
        "lr": lr,
        "cr": cr,
        "fr": fr,
        "fs": fs,
        "wr": wr,
        "ws": ws,
        "fn": fn,
        "zo": zo,
        "q": q,
    }


if __name__ == "__main__":
    params = calculate_parameters()

    for key, value in params.items():
        print(f"{key}: {value}")