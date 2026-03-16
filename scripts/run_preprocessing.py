#!/usr/bin/env python3
"""Run the preprocessing pipeline for one subject."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion import load_subject
from src.preprocessing.pipeline import run_preprocessing
from src.preprocessing.qc import save_qc
from src.utils.config import load_config, load_paths


def main():
    parser = argparse.ArgumentParser(description="Preprocess one EEG subject.")
    parser.add_argument("--config", default="configs/preprocessing.yaml")
    parser.add_argument("--paths", default="configs/paths.local.yaml")
    parser.add_argument("--subject", required=True, help="e.g. sub-0001")
    parser.add_argument("--session", default="rest")
    args = parser.parse_args()

    config = load_config(args.config)
    paths = load_paths(args.paths)

    raw = load_subject(args.subject, lemon_root=paths["lemon_root"], session=args.session)

    qc_dir = Path(paths["outputs_root"]) / "qc"
    preproc_dir = Path(paths["outputs_root"]) / "preprocessed"

    result = run_preprocessing(raw, config, output_dir=str(preproc_dir), subject_id=args.subject)
    save_qc(result["qc"], output_dir=str(qc_dir), subject_id=args.subject)

    print(f"Done: {args.subject} — {result['qc']['n_windows']} windows")


if __name__ == "__main__":
    main()
