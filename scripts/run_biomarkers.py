#!/usr/bin/env python3
"""Extract LOCF biomarkers for one subject."""
import argparse
from pathlib import Path
import sys
import mne

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.biomarkers.locf import extract_biomarkers
from src.database.writer import write_biomarkers
from src.utils.config import load_config, load_paths


def main():
    parser = argparse.ArgumentParser(description="Extract LOCF biomarkers for one subject.")
    parser.add_argument("--config", default="configs/biomarkers.yaml")
    parser.add_argument("--paths", default="configs/paths.local.yaml")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--session", default="rest")
    args = parser.parse_args()

    config = load_config(args.config)
    paths = load_paths(args.paths)

    preproc_dir = Path(paths["outputs_root"]) / "preprocessed"
    epo_file = preproc_dir / f"{args.subject}_preprocessed-epo.fif"
    epochs = mne.read_epochs(str(epo_file), preload=True)

    locf_config = config.get("locf", {})
    biomarkers = extract_biomarkers(epochs.get_data(), locf_config)

    bm_dir = Path(paths["outputs_root"]) / "biomarkers"
    for level in config.get("output_level", ["subject", "window"]):
        path = write_biomarkers(args.subject, args.session, biomarkers, str(bm_dir), level=level)
        print(f"Saved {level}: {path}")


if __name__ == "__main__":
    main()
