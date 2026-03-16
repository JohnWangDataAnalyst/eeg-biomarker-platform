# Contributing Guide

## Workflow

1. Pick up a GitHub issue or create one.
2. Create a branch: `git checkout -b feature/short-description` or `bugfix/short-description`.
3. Make changes, following the project rules below.
4. Open a pull request — link it to the issue with `Closes #<issue-number>`.
5. Request review from at least one teammate.
6. Supervisor reviews before merge.

## Project Rules

- **No raw data on GitHub.** Use Google Drive for data, large outputs, and reports.
- **Notebooks → scripts.** Final logic must live in `src/` or `scripts/`, not only in notebooks.
- **Standard naming.** Use snake_case for files and variables. Subject IDs follow BIDS: `sub-XXXX`.
- **Every PR linked to an issue.**
- **Every major feature needs a test or smoke check in `tests/`.**
- **Do not hard-code paths.** Use `configs/paths.local.yaml` via `load_paths()`.

## Branch Naming

| Type | Example |
|------|---------|
| Feature | `feature/lemon-metadata-parser` |
| Bug fix | `bugfix/qc-nan-handling` |
| Docs | `docs/biomarker-dictionary` |
| Refactor | `refactor/preprocessing-pipeline` |

## Labels

`task` · `bug` · `enhancement` · `documentation` · `pipeline` · `biomarkers` · `database` · `dashboard` · `good first task` · `blocked` · `high priority`
