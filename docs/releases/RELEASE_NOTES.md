# Release Notes

## Unreleased

### Added

- CI workflow in `.github/workflows/ci.yml` with compile checks, content validation, and runner smoke tests.
- Lightweight content validator script at `scripts/validate_content.py`.
- Prominent donation/support CTA in web hero and README badges.
- New web "Support Progress" panel with transparent funding goals and donate link.

## v0.3.0-catalog-pages (2026-03-01)

### Added

- GitHub Pages deployment workflow in `.github/workflows/pages.yml`.
- Six additional seed problem packs (catalog now at 10 total).
- Extra runnable examples for new Python-track seed problems.

### Changed

- Expanded `web/problems.json` to include more browser-runnable practice problems.
- Updated `README.md` with seed catalog counts and deployment notes.

### Planned

- Add CI checks for metadata schema and runner smoke tests.
- Add more medium/hard shell and graph challenges.

## v0.2.0-mvp (2026-03-01)

### Added

- Python local runner MVP in `runner/run_problem.py` with runtime and memory summaries.
- Initial browser MVP in `web/` with Pyodide execution and local progress tracking.
- First seed problem packs across algorithms, data science, and shell tracks.
- Runner usage docs in `runner/README.md`.

### Changed

- Extended top-level docs and README usage examples for runner and web app.

### Planned

- Grow seed catalog to 10+ problems.
- Add GitHub Pages auto-deploy workflow.

## v0.1.1-templates (2026-03-01)

### Added

- Problem pack templates under `problems/_templates/`.
- Problem pack contract spec in `docs/specs/problem-pack-contract.md`.

### Changed

- Documentation index in `README.md` updated to include schema references.

## v0.1.0-planning (2026-03-01)

### Added

- Public MIT-licensed repository foundation.
- Polished README with hero banner, badges, and project direction.
- Product roadmap with epics, tasks, subtasks, assumptions, and risks.
- Architecture and contribution documentation.

### Scope

- Documentation and repository scaffolding only.
