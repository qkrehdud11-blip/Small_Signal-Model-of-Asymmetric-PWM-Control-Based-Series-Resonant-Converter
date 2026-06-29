import matplotlib.pyplot as plt

from frequency_response import (
    align_phase_to_reference,
    calculate_bode_from_tf,
)


def plot_response_pair(
    gain_axis,
    phase_axis,
    label,
    transfer_function,
    plecs_data,
    frequency_hz,
    color,
):
    # Plot PLECS and Python model on the same gain/phase axes.
    gain_db, phase_deg = calculate_bode_from_tf(
        transfer_function,
        frequency_hz,
    )
    phase_deg = align_phase_to_reference(
        frequency_hz,
        phase_deg,
        plecs_data,
    )

    gain_axis.semilogx(
        plecs_data.iloc[:, 0],
        plecs_data.iloc[:, 1],
        "-.",
        color=color,
        linewidth=2,
        label=f"PLECS {label}",
    )
    gain_axis.semilogx(
        frequency_hz,
        gain_db,
        "--",
        color=color,
        linewidth=2,
        label=f"Python {label}",
    )

    phase_axis.semilogx(
        plecs_data.iloc[:, 0],
        plecs_data.iloc[:, 2],
        "-.",
        color=color,
        linewidth=2,
        label=f"PLECS {label}",
    )
    phase_axis.semilogx(
        frequency_hz,
        phase_deg,
        "--",
        color=color,
        linewidth=2,
        label=f"Python {label}",
    )


def setup_bode_axes(title, gain_ylim=None, phase_ylim=None, xlim=(100, 100000)):
    figure, (gain_axis, phase_axis) = plt.subplots(
        2,
        1,
        figsize=(8.2, 6.2),
        sharex=True,
    )
    figure.suptitle(title)

    gain_axis.set_ylabel("Magnitude [dB]")
    phase_axis.set_ylabel("Phase [deg]")
    phase_axis.set_xlabel("Frequency [Hz]")

    for axis in (gain_axis, phase_axis):
        axis.grid(True, which="both")
        axis.set_xlim(*xlim)

    if gain_ylim is not None:
        gain_axis.set_ylim(*gain_ylim)
    if phase_ylim is not None:
        phase_axis.set_ylim(*phase_ylim)

    return figure, gain_axis, phase_axis


def finish_bode_axes(
    figure,
    gain_axis,
    phase_axis,
    legend_outside=False,
):
    if legend_outside:
        handles, labels = gain_axis.get_legend_handles_labels()
        figure.legend(
            handles,
            labels,
            loc="lower left",
            bbox_to_anchor=(0.08, 0.02),
            fontsize=8,
            ncol=2,
            frameon=True,
        )
        figure.tight_layout(rect=(0, 0.16, 1, 1))
        return

    gain_axis.legend(loc="best", fontsize=8)
    phase_axis.legend(loc="best", fontsize=8)
    figure.tight_layout()
