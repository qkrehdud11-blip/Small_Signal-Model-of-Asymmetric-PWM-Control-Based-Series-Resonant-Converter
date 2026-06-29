"""
main_fig3.py

Figure 3 frequency response result.
- Line-to-Output: Vg -> Vo
- Control-to-Output(Duty): D -> Vo
- Control-to-Output(Frequency): W -> Vo
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from parameters import (
    calculate_derived_parameters,
    get_apwm_case,
)

from apwm_model import (
    build_state_space_matrices,
    build_state_space_system,
    calculate_model_parameters,
    extract_transfer_function,
)

from plecs import load_plecs_csv
from plot import (
    finish_bode_axes,
    plot_response_pair,
    setup_bode_axes,
)


def make_transfer_function(duty, f_sn, load_resistance, input_index, output_index=0):
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

    return extract_transfer_function(
        system,
        input_index=input_index,
        output_index=output_index,
    )


def main():
    data_dir = Path(__file__).resolve().parent.parent / "data"

    duty = 0.361
    f_sn = 1.05
    r_load = 5.0

    responses = [
        {
            "name": "Line-to-Output",
            "input_index": 0,
            "csv": "CCM_Vg_APWM_D0.361_F1.05_R5_Vo200.csv",
            "color": "r",
        },
        {
            "name": "Control-to-Output(Duty)",
            "input_index": 1,
            "csv": "CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv",
            "color": "b",
        },
        {
            "name": "Control-to-Output(Frequency)",
            "input_index": 2,
            "csv": "CCM_W_APWM_D0.361_F1.05_R5_Vo200.csv",
            "color": "m",
        },
    ]

    frequency_hz = np.logspace(2, np.log10(2.637e4), 700)

    figure, gain_axis, phase_axis = setup_bode_axes(
        title="Figure 3 Frequency Response Result",
        gain_ylim=(-120, 70),
        phase_ylim=(-270, 560),
        xlim=(100, 26370),
    )

    for response in responses:
        transfer_function = make_transfer_function(
            duty=duty,
            f_sn=f_sn,
            load_resistance=r_load,
            input_index=response["input_index"],
        )
        plecs_data = load_plecs_csv(
            data_dir,
            response["csv"],
        )

        plot_response_pair(
            gain_axis=gain_axis,
            phase_axis=phase_axis,
            label=response["name"],
            transfer_function=transfer_function,
            plecs_data=plecs_data,
            frequency_hz=frequency_hz,
            color=response["color"],
        )

    finish_bode_axes(figure, gain_axis, phase_axis)
    plt.show()


if __name__ == "__main__":
    main()
