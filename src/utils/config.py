import yaml
from pathlib import Path


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_paths(paths_path: str = "configs/paths.local.yaml") -> dict:
    p = Path(paths_path)
    if not p.exists():
        raise FileNotFoundError(
            f"{paths_path} not found. "
            "Copy configs/paths.example.yaml to configs/paths.local.yaml and fill in your paths."
        )
    with open(p) as f:
        return yaml.safe_load(f)
