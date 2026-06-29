"""
frequency_response.py

MATLAB bodeplot 흐름에 맞춰 전달함수의 Gain/Phase를 계산합니다.
"""

import control
import numpy as np


def calculate_bode_from_tf(transfer_function, frequency_hz):
    """
    TransferFunction의 Bode 응답을 Gain[dB], Phase[deg]로 반환합니다.
    """

    omega = 2 * np.pi * frequency_hz

    magnitude, phase_rad, _ = control.frequency_response(
        transfer_function,
        omega,
    )

    gain_db = 20 * np.log10(np.asarray(magnitude, dtype=float))
    phase_deg = np.degrees(np.unwrap(np.asarray(phase_rad, dtype=float)))

    return gain_db, phase_deg


def align_phase_to_reference(frequency_hz, phase_deg, reference_data):
    """
    PLECS CSV의 phase 기준에 맞도록 360도 단위 오프셋을 적용합니다.

    Python-control은 phase를 보통 -180도 근처로 감아 반환하고, PLECS
    데이터는 360도 또는 540도 근처의 연속 위상으로 저장되어 있습니다.
    전달함수 자체는 바꾸지 않고 표시 기준만 맞춥니다.
    """

    reference_frequency = reference_data.iloc[:, 0].to_numpy(dtype=float)
    reference_phase = reference_data.iloc[:, 2].to_numpy(dtype=float)

    overlap = (
        (frequency_hz >= reference_frequency.min())
        & (frequency_hz <= reference_frequency.max())
    )

    if not np.any(overlap):
        return phase_deg

    interpolated_reference = np.interp(
        frequency_hz[overlap],
        reference_frequency,
        reference_phase,
    )

    aligned_phase = phase_deg.copy()
    phase_error = interpolated_reference - aligned_phase[overlap]
    phase_offset = 360 * np.round(phase_error / 360)
    aligned_phase[overlap] = aligned_phase[overlap] + phase_offset

    return aligned_phase
