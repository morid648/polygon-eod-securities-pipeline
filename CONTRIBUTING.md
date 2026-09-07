# Contributing

This repository is primarily a portfolio project, but suggestions and fixes
are welcome.

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-change`
3. Make your changes, keeping the folder structure intact (`dags/`, `lib/`,
   `sql/`, `docs/`)
4. Commit with a clear message describing what changed and why
5. Open a pull request describing the change and its motivation

## Guidelines

- Keep SQL scripts idempotent — every merge should be safe to re-run
- Preserve the numbered filename convention in `sql/` (e.g. `01_copy_to_raw.sql`)
  since it reflects execution order
- If you add a new Airflow task, document it in `dags/README.md`
- If you change validation logic, update `docs/data_quality.md` to match

## Reporting Issues

Open a GitHub issue with:
- What you expected to happen
- What actually happened
- Relevant logs or error messages (with credentials/API keys redacted)
