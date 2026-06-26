# MATLAB cal_parameter_APWM.m 기준 파라미터 설정 파일

import numpy as np


def get_apwm_case(duty=0.185, f_sn=1.05, load_resistance=20.0):
    """
    cal_parameter_APWM(Duty, F_sn, R, r_s, r_c, C, L, C_f, V_g, Input, Output)
    MATLAB 함수에 들어가는 입력 파라미터를 Python dict로 정리합니다.
    """

    return {
        "duty": duty,
        "f_sn": f_sn,
        "r_load": load_resistance,

        # MATLAB 코드 기준
        "r_s": 1e-3,
        "r_c": 1e-3,
        "c_resonant": 51e-9,
        "l_resonant": 197e-6,
        "c_filter": 32e-6,
        "v_g": 400.0,
        "v_o": 200.0,
    }


def calculate_derived_parameters(params):
    """
    MATLAB cal_parameter_APWM.m의 앞부분 계산식 변환
    """

    duty = params["duty"]
    f_sn = params["f_sn"]
    r_load = params["r_load"]
    r_s = params["r_s"]
    r_c = params["r_c"]
    c = params["c_resonant"]
    l = params["l_resonant"]
    c_f = params["c_filter"]
    v_g = params["v_g"]

    f_o = 1 / (2 * np.pi * np.sqrt(l * c))
    w_o = 2 * np.pi * f_o
    f_s = f_sn * f_o
    w_s = 2 * np.pi * f_s

    r_cc = r_c * r_load / (r_c + r_load)

    v_dc = v_g * (2 * duty - 1)
    v_es = v_g * 2 / np.pi * (1 - np.cos(2 * np.pi * duty))
    v_ec = v_g * 2 / np.pi * np.sin(2 * np.pi * duty)

    r_e = 8 / np.pi**2 * (1 - r_cc / r_load) * (r_c / r_cc) * r_load

    alpha = 1 - w_s**2 * l * c
    beta = w_s * c * (r_e + r_s)
    theta = alpha * beta / (alpha**2 + beta**2)

    v_s = ((v_dc * alpha + v_dc * beta) * theta + v_es * alpha + v_ec * beta) / (
        alpha**2 + beta**2
    )
    v_c = ((v_dc * alpha - v_dc * beta) * theta + v_ec * alpha - v_es * beta) / (
        alpha**2 + beta**2
    )

    i_s = -w_s * c * v_c
    i_c = w_s * c * v_s
    i_p = np.sqrt(i_s**2 + i_c**2)
    v_cf = np.pi / 4 * i_p * r_e

    return {
        **params,
        "f_o": f_o,
        "w_o": w_o,
        "f_s": f_s,
        "w_s": w_s,
        "r_cc": r_cc,
        "v_dc": v_dc,
        "v_es": v_es,
        "v_ec": v_ec,
        "r_e": r_e,
        "alpha": alpha,
        "beta": beta,
        "theta": theta,
        "v_s": v_s,
        "v_c": v_c,
        "i_s": i_s,
        "i_c": i_c,
        "i_p": i_p,
        "v_cf": v_cf,
    }


if __name__ == "__main__":
    case = get_apwm_case(duty=0.185, f_sn=1.05, load_resistance=20.0)
    params = calculate_derived_parameters(case)

    for key, value in params.items():
        print(f"{key}: {value}")