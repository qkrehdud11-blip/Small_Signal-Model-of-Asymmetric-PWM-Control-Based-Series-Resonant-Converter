"""
main.py

MATLAB Control_to_Output_Duty_Paper.m의 for문 구조를 Python으로 재현
"""

import numpy as np
import matplotlib.pyplot as plt
import control

from parameters import (
    get_apwm_case,
    calculate_derived_parameters,
)

from apwm_model import (
    calculate_model_parameters,
    build_state_space_matrices,
    build_state_space_system,
    extract_transfer_function,
)


def make_transfer_function(duty, f_sn, load_resistance):
    """Duty, F_sn, R 조건에 대한 Duty-to-Output 전달함수를 생성합니다."""

    case = get_apwm_case(
        duty=duty,
        f_sn=f_sn,
        load_resistance=load_resistance,
    )

    params = calculate_derived_parameters(case)
    model = calculate_model_parameters(params)

    a_matrix, b_matrix, c_matrix, d_matrix = build_state_space_matrices(
        params,
        model,
    )

    system = build_state_space_system(
        a_matrix,
        b_matrix,
        c_matrix,
        d_matrix,
    )

    # MATLAB Input=2(Duty), Output=1(Vo)
    return extract_transfer_function(
        system,
        input_index=1,
        output_index=0,
    )


def main():
    # MATLAB:
    # mDuty = [0.361, 0.185]
    # SwitchingFrequency = [1.05, 1.05]
    # mR = [5, 20]
    cases = [
        {"duty": 0.361, "f_sn": 1.05, "r_load": 5.0},
        {"duty": 0.185, "f_sn": 1.05, "r_load": 20.0},
    ]

    frequency_hz = np.logspace(2, 5, 500)
    omega = 2 * np.pi * frequency_hz

    plt.figure(figsize=(8, 5))
    for case in cases:
        g_vd = make_transfer_function(
            duty=case["duty"],
            f_sn=case["f_sn"],
            load_resistance=case["r_load"],
        )

        magnitude, phase, _ = control.bode(
            g_vd,
            omega,
            plot=False,
        )

        gain_db = 20 * np.log10(magnitude)

        label = (
            f"Python Fs=Fo×{case['f_sn']} / "
            f"Duty={case['duty']} / "
            f"R={case['r_load']}Ω"
        )

        plt.semilogx(
            frequency_hz,
            gain_db,
            linewidth=2,
            label=label,
        )

    plt.grid(True, which="both")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Gain [dB]")
    plt.title("Duty-to-Output Gain Comparison")
    plt.legend()

    plt.figure(figsize=(8, 5))
    for case in cases:
        g_vd = make_transfer_function(
            duty=case["duty"],
            f_sn=case["f_sn"],
            load_resistance=case["r_load"],
        )

        magnitude, phase, _ = control.bode(
            g_vd,
            omega,
            plot=False,
        )

        phase_deg = np.degrees(phase)

        label = (
            f"Python Fs=Fo×{case['f_sn']} / "
            f"Duty={case['duty']} / "
            f"R={case['r_load']}Ω"
        )

        plt.semilogx(
            frequency_hz,
            phase_deg,
            linewidth=2,
            label=label,
        )

    plt.grid(True, which="both")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Phase [deg]")
    plt.title("Duty-to-Output Phase Comparison")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()