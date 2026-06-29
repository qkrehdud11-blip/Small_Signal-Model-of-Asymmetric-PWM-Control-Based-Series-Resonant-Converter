"""
APWM Small-Signal Model

MATLAB:
cal_parameter_APWM.m

중간 파라미터 계산 부분을 Python으로 그대로 변환
"""

import numpy as np
import control


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

    # MATLAB:
    # K_vs = 2/pi*(1-cos(2*pi*Duty));
    k_vs = 2 / np.pi * (1 - np.cos(2 * np.pi * duty))

    # MATLAB:
    # K_vc = 2/pi*sin(2*pi*Duty);
    k_vc = 2 / np.pi * np.sin(2 * np.pi * duty)

    # MATLAB:
    # E_ds = 4*V_g*sin(2*pi*Duty);
    e_ds = 4 * v_g * np.sin(2 * np.pi * duty)

    # MATLAB:
    # E_dc = 4*V_g*cos(2*pi*Duty);
    e_dc = 4 * v_g * np.cos(2 * np.pi * duty)

    # MATLAB:
    # E_s = L*I_c;
    e_s = l * i_c

    # MATLAB:
    # E_c = L*I_s;
    e_c = l * i_s

    # MATLAB:
    # Z_s = Ws*L+4/pi*V_cf*I_s*I_c/(I_p^2)^(3/2);
    z_s = (
        w_s * l
        + (4 / np.pi)
        * v_cf
        * i_s
        * i_c
        / ((i_p ** 2) ** (3 / 2))
    )

    # MATLAB:
    # Z_c = -Ws*L+4/pi*V_cf*I_s*I_c/(I_p^2)^(3/2);
    z_c = (
        -w_s * l
        + (4 / np.pi)
        * v_cf
        * i_s
        * i_c
        / ((i_p ** 2) ** (3 / 2))
    )

    # MATLAB:
    # G = Ws*C;
    g = w_s * c

    # MATLAB:
    # K_s = 2/pi*I_s/I_p;
    k_s = 2 / np.pi * i_s / i_p

    # MATLAB:
    # K_c = 2/pi*I_c/I_p;
    k_c = 2 / np.pi * i_c / i_p

    # MATLAB:
    # J_s = C*V_c;
    j_s = c * v_c

    # MATLAB:
    # J_c = C*V_s;
    j_c = c * v_s

    # MATLAB:
    # R_s = r_s + 4/pi*V_cf*I_c^2/I_p^3;
    r_s_equivalent = (
        r_s
        + (4 / np.pi)
        * v_cf
        * i_c ** 2
        / (i_p ** 3)
    )

    # MATLAB:
    # R_c = r_s + 4/pi*V_cf*I_s^2/I_p^3;
    r_c_equivalent = (
        r_s
        + (4 / np.pi)
        * v_cf
        * i_s ** 2
        / (i_p ** 3)
    )

    # MATLAB:
    # I_d = 2*(-I_s*sin(2*pi*Duty)+I_c*cos(2*pi*Duty));
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


def build_state_space_matrices(params, model):
    """
    MATLAB cal_parameter_APWM.m의 A, B, CC, DD 행렬 생성 부분을 Python으로 변환합니다.
    """

    duty = params["duty"]
    r_load = params["r_load"]
    r_c = params["r_c"]
    c = params["c_resonant"]
    l = params["l_resonant"]
    c_f = params["c_filter"]
    v_g = params["v_g"]
    r_cc = params["r_cc"]
    theta = params["theta"]

    k_vs = model["k_vs"]
    k_vc = model["k_vc"]
    e_ds = model["e_ds"]
    e_dc = model["e_dc"]
    e_s = model["e_s"]
    e_c = model["e_c"]
    z_s = model["z_s"]
    z_c = model["z_c"]
    g = model["g"]
    k_s = model["k_s"]
    k_c = model["k_c"]
    j_s = model["j_s"]
    j_c = model["j_c"]
    r_s_equivalent = model["r_s_equivalent"]
    r_c_equivalent = model["r_c_equivalent"]
    i_d = model["i_d"]

    # MATLAB A matrix
    a_matrix = np.array([
        [-r_s_equivalent / l, z_s / l, -1 / l, 0, -2 * k_s / l, 0],
        [z_c / l, -r_c_equivalent / l, 0, -1 / l, -2 * k_c / l, 0],
        [1 / c, 0, 0, g / c, 0, 0],
        [0, 1 / c, -g / c, 0, 0, 0],
        [
            k_s * r_cc / (c_f * r_c),
            k_c * r_cc / (c_f * r_c),
            0,
            0,
            -r_cc / (r_load * c_f * r_c),
            0,
        ],
        [0, 0, 0, 0, 0, 0],
    ])

    # MATLAB B matrix
    b_matrix = np.array([
        [k_vs / l, e_ds / l, e_s / l, 0],
        [k_vc / l, e_dc / l, -e_c / l, 0],
        [0, 0, j_s / c, 0],
        [0, 0, -j_c / c, 0],
        [0, 0, 0, r_cc / (c_f * r_c)],
        [theta * (2 * duty - 1), theta * v_g * 2, 0, 0],
    ])

    # MATLAB CC matrix
    c_matrix = np.array([
        [k_s * r_cc, k_c * r_cc, 0, 0, r_cc / r_c, 0],
        [
            1 / np.pi * (1 - np.cos(2 * np.pi * duty)),
            1 / np.pi * np.sin(2 * np.pi * duty),
            0,
            0,
            0,
            0,
        ],
    ])

    # MATLAB DD matrix
    d_matrix = np.array([
        [0, 0, 0, r_cc],
        [0, i_d, 0, 0],
    ])

    return a_matrix, b_matrix, c_matrix, d_matrix


def build_state_space_system(a_matrix, b_matrix, c_matrix, d_matrix):
    """
    A, B, C, D 행렬을 이용해 상태공간 시스템을 생성합니다.
    """
    return control.ss(a_matrix, b_matrix, c_matrix, d_matrix)


def extract_transfer_function(system, input_index=1, output_index=0):
    """
    MATLAB:
        [num, den] = ss2tf(A, B, C, D, Input)
        G = tf(num(Output, :), den)
    """

    siso_system = system[output_index, input_index]
    transfer_function = control.ss2tf(siso_system)

    return transfer_function