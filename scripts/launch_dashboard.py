#!/usr/bin/env python3
"""Launch the EEG Biomarker dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import pages to register them with Dash
import src.dashboard.pages.cohort  # noqa
import src.dashboard.pages.subject  # noqa
import src.dashboard.pages.qc  # noqa

from src.dashboard.app import create_app
from src.utils.config import load_paths


def main():
    paths = load_paths()
    app = create_app(paths)
    print("Dashboard running at http://127.0.0.1:8050")
    app.run(debug=True, host="127.0.0.1", port=8050)


if __name__ == "__main__":
    main()
