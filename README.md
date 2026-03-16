# EEG Biomarker Platform

A reproducible pipeline for EEG-based biomarker extraction using the **Linear Observer Control Framework (LOCF)**, with a dashboard for cohort- and subject-level visualization.

**Project Supervisor:** Zheng Wang

---

## Overview

This platform:
1. Ingests raw EEG data (starting with the [LEMON dataset](https://www.nature.com/articles/sdata2018308))
2. Preprocesses and quality-checks recordings
3. Extracts standard EEG features and LOCF-derived biomarkers (K_norm, L_norm, etc.)
4. Stores outputs in a structured biomarker database
5. Displays results in an interactive dashboard

**Longer-term targets:** sleep, mood, depression, meditation, PBM, digital-twin applications.

---

## Repository Structure

```
src/
  ingestion/        # data loading, metadata parsing
  preprocessing/    # artifact rejection, filtering, epoching
  features/         # standard EEG feature extraction
  biomarkers/       # LOCF biomarker computation
  database/         # schema, write/read utilities
  dashboard/        # Dash/Streamlit app

scripts/            # CLI entry points
notebooks/          # exploratory and onboarding notebooks
configs/            # pipeline configs and path templates
docs/               # biomarker dictionary, design docs
tests/              # unit and smoke tests
outputs/            # generated outputs (not committed)
```

---

## Team

| Name     | Owns |
|----------|------|
| Pawan    | preprocessing, feature extraction, biomarker extraction, LEMON validation |
| Vedansh  | database schema, backend/API, dashboard UI |
| Aditya   | data ingestion, metadata parsing, orchestration, config, reproducibility |

---

## Getting Started

### 1. Clone the repo

```bash
git clone <repo-url>
cd eeg-biomarker-platform
```

### 2. Create environment

```bash
conda env create -f environment.yml
conda activate eeg-biomarker-platform
```

or

```bash
pip install -r requirements.txt
```

### 3. Configure data paths

```bash
cp configs/paths.example.yaml configs/paths.local.yaml
```

Edit `configs/paths.local.yaml` to point to your local LEMON data (synced from Google Drive).

### 4. Run environment check

```bash
jupyter notebook notebooks/00_environment_check.ipynb
```

### 5. Run one sample subject

```bash
python scripts/run_preprocessing.py --config configs/preprocessing.yaml --subject sub-0001
python scripts/run_biomarkers.py --config configs/biomarkers.yaml --subject sub-0001
```

### 6. Build database

```bash
python scripts/build_database.py
```

### 7. Launch dashboard

```bash
python scripts/launch_dashboard.py
```

---

## Data Policy

- **Do not commit raw dataset files to GitHub.**
- Raw LEMON data and shared example notebooks live in **Google Drive**.
- Reference data paths through `configs/paths.local.yaml` — never hard-code paths.
- `configs/paths.example.yaml` is the committed template; `paths.local.yaml` is gitignored.

---

## Standard Outputs

| Type | Location |
|------|----------|
| QC summaries | `outputs/qc/` |
| Subject biomarker tables | `outputs/biomarkers/` |
| Cohort summary tables | `outputs/cohort/` |

Example:
```
outputs/qc/sub-0001_ses-rest_run-01_qc.csv
outputs/biomarkers/sub-0001_ses-rest_run-01_biomarkers.parquet
```

---

## Project Rules

- Every pull request must be linked to an issue.
- Notebook logic must be converted to scripts/modules before merging.
- Use standard file and variable naming across modules.
- Every major feature needs at least one test or smoke check.

---

## Milestones

| # | Milestone |
|---|-----------|
| 1 | Onboarding and replication |
| 2 | LEMON ingestion and preprocessing |
| 3 | Biomarker database |
| 4 | Dashboard prototype |
| 5 | Prototype release |

See [docs/milestones.md](docs/milestones.md) for detailed checklists.

---

## Documentation

- [Biomarker Dictionary](docs/biomarker_dictionary.md)
- [Milestones](docs/milestones.md)
- [Contributing](docs/contributing.md)
