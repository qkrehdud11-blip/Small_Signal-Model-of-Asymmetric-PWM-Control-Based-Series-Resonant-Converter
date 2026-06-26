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
)


def main():
    """
    APWM 모델 계산 실행
    """

    # MATLAB
    # Duty = 0.185
    # F_sn = 1.05
    # R = 20Ω

    case = get_apwm_case(
        duty=0.185,
        f_sn=1.05,
        load_resistance=20.0,
    )

    # MATLAB 앞부분 계산
    params = calculate_derived_parameters(case)

    # MATLAB 중간 계산
    model = calculate_model_parameters(params)

    print("=" * 50)
    print("APWM Small Signal Parameters")
    print("=" * 50)

    for key, value in model.items():
        print(f"{key:20s} : {value}")


if __name__ == "__main__":
    main()