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

    system = build_state_space_system(
        a_matrix,
        b_matrix,
        c_matrix,
        d_matrix,
    )

    # MATLAB: Input = 2, Output = 1
    # Python: input_index = 1, output_index = 0
    g_vd = extract_transfer_function(
        system,
        input_index=1,
        output_index=0,
    )

    print("Duty-to-Output Transfer Function:")
    print(g_vd)


if __name__ == "__main__":
    main()