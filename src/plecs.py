from pathlib import Path

import pandas as pd


def load_plecs_csv(data_dir: Path, csv_filename: str):
    """
    PLECS CSV 데이터를 읽습니다.

    CSV 구조:
    1열: Frequency [Hz]
    2열: Gain [dB]
    3열: Phase [deg]
    """

    csv_path = data_dir / csv_filename

    plecs_data = pd.read_csv(csv_path)

    # MATLAB bodeplot 범위와 맞추기 위해 100 Hz 이상만 사용
    plecs_data = plecs_data[
        plecs_data.iloc[:, 0] >= 100
    ]

    return plecs_data