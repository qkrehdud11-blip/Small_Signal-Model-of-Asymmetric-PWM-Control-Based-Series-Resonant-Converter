"""
APWM Small-Signal Model

MATLAB:
cal_parameter_APWM.m

중간 파라미터 계산 부분을 Python으로 그대로 변환
"""

import numpy as np


def calculate_model_parameters(params):
    """
    MATLAB cal_parameter_APWM.m
    중간 파라미터 계산
    """

    duty = params["duty"]

    v_g = params["v_g"]

    l = params["l_resonant"]
    c = params["c_resonant"]

    r_s = params["r_s"]

    w_s = params["w_s"]

    v_cf = params["v_cf"]

    i_s = params["i_s"]
    i_c = params["i_c"]
    i_p = params["i_p"]

    v_s = params["v_s"]
    v_c = params["v_c"]

    # MATLAB 그대로 변환
    k_vs = 2 / np.pi * (1 - np.cos(2 * np.pi * duty))

    k_vc = 2 / np.pi * np.sin(2 * np.pi * duty)

    e_ds = 4 * v_g * np.sin(2 * np.pi * duty)

    e_dc = 4 * v_g * np.cos(2 * np.pi * duty)

    e_s = l * i_c

    e_c = l * i_s

    z_s = (
        w_s * l
        + (4 / np.pi)
        * v_cf
        * i_s
        * i_c
        / ((i_p ** 2) ** (3 / 2))
    )

    z_c = (
        -w_s * l
        + (4 / np.pi)
        * v_cf
        * i_s
        * i_c
        / ((i_p ** 2) ** (3 / 2))
    )

    g = w_s * c

    k_s = 2 / np.pi * i_s / i_p

    k_c = 2 / np.pi * i_c / i_p

    j_s = c * v_c

    j_c = c * v_s

    r_s_equivalent = (
        r_s
        + (4 / np.pi)
        * v_cf
        * i_c ** 2
        / (i_p ** 3)
    )

    r_c_equivalent = (
        r_s
        + (4 / np.pi)
        * v_cf
        * i_s ** 2
        / (i_p ** 3)
    )

    i_d = 2 * (
        -i_s * np.sin(2 * np.pi * duty)
        + i_c * np.cos(2 * np.pi * duty)
    )

    return {
        "k_vs": k_vs,
        "k_vc": k_vc,
        "e_ds": e_ds,
        "e_dc": e_dc,
        "e_s": e_s,
        "e_c": e_c,
        "z_s": z_s,
        "z_c": z_c,
        "g": g,
        "k_s": k_s,
        "k_c": k_c,
        "j_s": j_s,
        "j_c": j_c,
        "r_s_equivalent": r_s_equivalent,
        "r_c_equivalent": r_c_equivalent,
        "i_d": i_d,
    }