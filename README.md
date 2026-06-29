# APWM Series Resonant Converter Small-Signal Model

Python implementation of the small-signal model for an Asymmetric PWM(APWM) controlled Series Resonant Converter(SRC). The model is translated from the Matlab reference and compared with PLECS frequency-response data.

## What This Project Shows

- Reproduces the paper's Fig.3 frequency responses: `Vg -> Vo`, `Duty -> Vo`, `Frequency -> Vo`
- Reproduces the paper's Fig.4 duty-to-output comparison under two load conditions
- Keeps Matlab scripts and PLECS CSV files as reference data
- Uses Python-control to build transfer functions from the APWM state-space model

## Results

### Fig.3 Frequency Response

Single operating point comparison for line, duty, and frequency inputs.

![Figure 3 frequency response](docs/images/figure3_frequency_response.png)

### Fig.4 Duty-to-Output Response

Duty-to-output response comparison for two load conditions.

![Figure 4 duty-to-output response](docs/images/figure4_duty_to_output.png)

## Run

```bash
python src/main_fig3.py
python src/main_fig4.py
```

`main_fig3.py` and `main_fig4.py` open Matplotlib windows in PyCharm or a local Python environment.

## Project Layout

```text
.
├── data/          Matlab reference files and PLECS CSV data
├── docs/images/   README figures
└── src/           Python implementation
```

| Path | Purpose |
| --- | --- |
| `src/parameters.py` | Operating point and derived parameter calculation |
| `src/apwm_model.py` | APWM small-signal coefficients, A/B/C/D matrices, transfer functions |
| `src/frequency_response.py` | Bode gain/phase calculation and phase alignment |
| `src/plecs.py` | PLECS CSV loader |
| `src/plot.py` | Gain/phase plotting utilities |
| `src/main_fig3.py` | Fig.3 reproduction script |
| `src/main_fig4.py` | Fig.4 reproduction script |

## Modeling Background

The target converter is a full-bridge Series Resonant Converter driven by APWM.

<p align="center">
  <img src="docs/images/paper_src_converter.png" alt="Full-Bridge Series Resonant Converter" width="560">
</p>

APWM changes the duty of the bridge voltage `VAB`. In the paper, this waveform is approximated with EDF(Extended Describing Function) terms so that the resonant current and capacitor-voltage dynamics can be linearized.

<p align="center">
  <img src="docs/images/paper_apwm_vab_waveform.png" alt="APWM VAB waveform" width="560">
</p>

The implementation follows this flow:

```text
Operating point
  -> derived parameters
  -> APWM EDF coefficients
  -> state-space matrices
  -> transfer functions
  -> Bode comparison with PLECS CSV
```

## Paper Parameters

The paper lists the following system parameters.

| Parameter | Value |
| --- | --- |
| `Vg` | `120 V` |
| `Vo` | `200 V` |
| `L` | `198 uH` |
| `C` | `51 nF` |
| `Cf` | `32 uF` |
| `RL` | `20 ohm / 5 ohm` |

The Python reproduction uses the Matlab/PLECS reference files included in `data/`. Check `src/parameters.py` and `data/cal_parameter_APWM.m` for the exact values used by the executable code.

## Reference Data

| File | Role |
| --- | --- |
| `data/cal_parameter_APWM.m` | Matlab reference for APWM model parameters and state-space matrices |
| `data/Control_to_Output_Duty_Paper.m` | Matlab reference for Fig.4 duty-to-output comparison |
| `data/CCM_Vg_APWM_D0.361_F1.05_R5_Vo200.csv` | PLECS data for `Vg -> Vo` |
| `data/CCM_D_APWM_D0.361_F1.05_R5_Vo200.csv` | PLECS data for `Duty -> Vo`, `R=5 ohm` |
| `data/CCM_W_APWM_D0.361_F1.05_R5_Vo200.csv` | PLECS data for `Frequency -> Vo` |
| `data/CCM_D_APWM_D0.185_F1.05_R20_Vo200.csv` | PLECS data for `Duty -> Vo`, `R=20 ohm` |

## Notes

- PLECS CSV data ends at `26.37 kHz`; the plots are trimmed to that frequency.
- Matlab uses 1-based input numbering, while Python-control uses zero-based indexing.
- PLECS and Python-control can express the same phase with different 360-degree offsets, so phase alignment is applied only for plotting.
