# Biomarker Dictionary

This document defines each biomarker used in the EEG Biomarker Platform.

## Required fields for every biomarker

| Field | Description |
|-------|-------------|
| `biomarker_name` | Unique identifier used in code and database |
| `description` | Plain-language description |
| `mathematical_definition` | Formal definition |
| `input_data` | What data/model outputs are required |
| `output_level` | subject-level, window-level, or both |
| `units` | Units or "dimensionless" |
| `expected_range` | Approximate expected range (dataset-dependent) |
| `quality_checks` | What to check for invalid values |
| `owner` | Team member responsible |

---

## LOCF Biomarkers

### K_norm

- **Description:** Frobenius norm of the Kalman gain matrix K derived from the LOCF state-space model
- **Definition:** `K_norm = ||K||_F` where K is the fitted Kalman gain (n_states × n_channels)
- **Input:** Single EEG window → LOCF model fit
- **Output level:** window-level, subject-level (mean, std)
- **Units:** dimensionless (model units)
- **Expected range:** dataset-dependent; check for stability across windows
- **Quality checks:** NaN, inf, values >> expected range, failed fits (converged=False)
- **Owner:** Pawan

### L_norm

- **Description:** Frobenius norm of the observer gain matrix L
- **Definition:** `L_norm = ||L||_F` where L is the fitted observer gain (n_states × n_channels)
- **Input:** Single EEG window → LOCF model fit
- **Output level:** window-level, subject-level (mean, std)
- **Units:** dimensionless (model units)
- **Expected range:** dataset-dependent
- **Quality checks:** NaN, inf, unstable fits
- **Owner:** Pawan

### K_norm_mean / K_norm_std

- **Description:** Mean and standard deviation of K_norm across windows for a subject/session
- **Definition:** `mean(K_norm_windows)`, `std(K_norm_windows)`
- **Output level:** subject-level
- **Units:** dimensionless
- **Owner:** Pawan

### L_norm_mean / L_norm_std

- **Description:** Mean and standard deviation of L_norm across windows
- **Output level:** subject-level
- **Owner:** Pawan

---

## Standard EEG Features

### bandpower_{band}

- **Description:** Mean power spectral density in a frequency band, optionally normalized by total power
- **Bands:** delta (1–4 Hz), theta (4–8 Hz), alpha (8–13 Hz), beta (13–30 Hz), gamma (30–40 Hz)
- **Definition:** `mean(PSD[f_min:f_max])`, normalized by `sum(PSD[1:f_nyq])`
- **Input:** Preprocessed EEG window
- **Output level:** window-level (n_channels), subject-level (mean over channels and windows)
- **Units:** µV²/Hz (or normalized, dimensionless)
- **Owner:** Pawan

### connectivity

- **Description:** Pairwise spectral connectivity between EEG channels
- **Method:** Coherence (default), PLV, or PLI
- **Input:** Preprocessed EEG epochs
- **Output level:** subject-level (n_channels × n_channels matrix)
- **Units:** dimensionless (0–1 for coherence)
- **Owner:** Pawan

---

## Adding a New Biomarker

1. Add an entry to this file following the template above.
2. Implement extraction in `src/biomarkers/` or `src/features/`.
3. Add the biomarker name to `configs/biomarkers.yaml` under `biomarkers:`.
4. Add a unit test in `tests/`.
5. Open a PR linked to the relevant GitHub issue.
