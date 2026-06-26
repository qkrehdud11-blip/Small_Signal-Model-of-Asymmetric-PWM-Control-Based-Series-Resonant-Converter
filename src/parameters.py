# APWM 기반 직렬 공진형 컨버터 논문 파라미터 계산 파일
# 논문 Table 1의 시스템 파라미터를 기준으로 작성했습니다.

import numpy as np


def calculate_parameters(load_resistance=20.0, normalized_frequency=1.05):
    """
    논문 Table 1 기준 시스템 파라미터를 계산합니다.

    Args:
        load_resistance (float): 부하 저항 [ohm], 논문에서는 20Ω / 5Ω 사용
        normalized_frequency (float): 정규화 스위칭 주파수 fs/fr

    Returns:
        dict: 회로 및 주파수 파라미터
    """

    # 입력 전압 [V]
    vg = 120.0

    # 출력 전압 [V]
    vo = 200.0

    # 공진 인덕터 [H]
    l_resonant = 198e-6

    # 공진 커패시터 [F]
    c_resonant = 51e-9

    # 출력 필터 커패시터 [F]
    c_filter = 32e-6

    # 부하 저항 [ohm]
    r_load = load_resistance

    # 공진 주파수 [Hz]
    f_resonant = 1 / (2 * np.pi * np.sqrt(l_resonant * c_resonant))

    # 스위칭 주파수 [Hz]
    f_switching = normalized_frequency * f_resonant

    # 각주파수 [rad/s]
    omega_resonant = 2 * np.pi * f_resonant
    omega_switching = 2 * np.pi * f_switching

    # 특성 임피던스 [ohm]
    z_resonant = np.sqrt(l_resonant / c_resonant)

    return {
        "vg": vg,
        "vo": vo,
        "l_resonant": l_resonant,
        "c_resonant": c_resonant,
        "c_filter": c_filter,
        "r_load": r_load,
        "f_resonant": f_resonant,
        "f_switching": f_switching,
        "omega_resonant": omega_resonant,
        "omega_switching": omega_switching,
        "z_resonant": z_resonant,
        "normalized_frequency": normalized_frequency,
    }


if __name__ == "__main__":
    params = calculate_parameters(load_resistance=20.0)

    for key, value in params.items():
        print(f"{key}: {value}")