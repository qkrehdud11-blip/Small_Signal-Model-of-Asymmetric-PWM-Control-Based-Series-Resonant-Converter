"""
main_fig4.py

Figure 4 control-to-output(Duty) frequency response comparison.
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


def make_transfer_function(duty, f_sn, load_resistance):
    # Fig.4 compares Duty-to-Output, which is MATLAB Input=2.
    # Python-control uses zero-based indexing, so Duty input is index 1.
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
        input_index=1,
        output_index=0,
    )


def main():
    data_dir = Path(__file__).resolve().parent.parent / "data"

    cases = [
        {
            "label": "Fs=Fo x 1.05 / Duty=0.361 / R=5ohm",
            "duty": 0.361,
            "f_sn": 1.05,
            "r_load": 5.0,
            "csv": "CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv",
            "color": "r",
        },
        {
            "label": "Fs=Fo x 1.05 / Duty=0.185 / R=20ohm",
            "duty": 0.185,
            "f_sn": 1.05,
            "r_load": 20.0,
            "csv": "CCM_D_APWM_D0.185_F1.05_R20_Vo200.csv",
            "color": "b",
        },
    ]

    # PLECS CSV data ends at 26.37 kHz, so the model line is trimmed there.
    frequency_hz = np.logspace(2, np.log10(2.637e4), 700)

    figure, gain_axis, phase_axis = setup_bode_axes(
        title="Figure 4 Control-to-Output(Duty)",
        gain_ylim=(0, 70),
        phase_ylim=(135, 390),
        xlim=(100, 26370),
    )
    phase_axis.set_yticks([135, 180, 225, 270, 315, 360])

    for case in cases:
        transfer_function = make_transfer_function(
            duty=case["duty"],
            f_sn=case["f_sn"],
            load_resistance=case["r_load"],
        )
        plecs_data = load_plecs_csv(
            data_dir,
            case["csv"],
        )

        plot_response_pair(
            gain_axis=gain_axis,
            phase_axis=phase_axis,
            label=case["label"],
            transfer_function=transfer_function,
            plecs_data=plecs_data,
            frequency_hz=frequency_hz,
            color=case["color"],
        )

    finish_bode_axes(figure, gain_axis, phase_axis)
    plt.show()


if __name__ == "__main__":
    main()
