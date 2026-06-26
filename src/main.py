"""
main.py

MATLAB cal_parameter_APWM.m 실행 흐름을
Python으로 재현하는 첫 번째 단계
"""

from parameters import (
    get_apwm_case,
    calculate_derived_parameters,
)

from apwm_model import (
    calculate_model_parameters,
    build_state_space_matrices,
)


def main():
    case = get_apwm_case(
        duty=0.185,
        f_sn=1.05,
        load_resistance=20.0,
    )

    params = calculate_derived_parameters(case)
    model = calculate_model_parameters(params)

    a_matrix, b_matrix, c_matrix, d_matrix = build_state_space_matrices(
        params,
        model,
    )

    print("A shape:", a_matrix.shape)
    print("B shape:", b_matrix.shape)
    print("C shape:", c_matrix.shape)
    print("D shape:", d_matrix.shape)

    print("\nA matrix:")
    print(a_matrix)


if __name__ == "__main__":
    main()