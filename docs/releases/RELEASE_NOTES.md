# Release Notes

## Unreleased

### Added

- CI workflow in `.github/workflows/ci.yml` with compile checks, content validation, and runner smoke tests.
- Lightweight content validator script at `scripts/validate_content.py`.
- Prominent donation/support CTA in web hero and README badges.
- New web "Support Progress" panel with transparent funding goals and donate link.
- Smart post-success donation ribbon in the web app with cooldown and dismiss behavior to avoid user fatigue.
- Shell challenge evaluator in `runner/run_shell_problem.py` with strict timeout-based checks.
- New problem scaffolder `scripts/new_problem.py` for faster content authoring.
- Batch seed generator `scripts/generate_seed_batch.py` and 20 additional seed packs (30 total catalog).
- Community issue templates for problem proposals, editorial improvements, and test bugs.
- Recommendation card in web progress panel for next suggested challenge.
- Topic-based filtering in the web problem list (`topic` + `difficulty`).
- Catalog scaled to 100 problem packs (10x from initial 10).
- Search + pagination in web problem browser.
- Curated learning paths in web UI (`Interview Path`, `ML Engineer Path`).
- Generated full web catalog at `web/full-catalog.json`.
- Quality scoring gate and report generation (`scripts/score_problem_quality.py`, `docs/specs/problem-quality-report.json`).
- Makefile developer workflow commands and pre-commit configuration.
- Future backend API contract draft in `docs/specs/backend-api-contracts.md`.
- Gold-tier baseline raised to 30 with promoted hidden-test coverage.
- Decluttered web filters UI with progressive disclosure and visible result count.
- Added top-level contribution CTA in web hero and README for higher visibility.
- Added sticky active-filter summary bar with one-click clear action.
- Converted problem list rows into compact metadata cards for a cleaner scan path.
- Reduced panel visual weight and tightened typography for denser minimalist browsing.
- Added keyboard shortcuts for discovery flow (`/` focus search, `Esc` clear search).
- Added Focus Mode toggle to hide secondary panels while solving.
- Collapsed non-essential panels (Learning Paths and Support Progress) by default.
- Bundled all public tests into `web/public-tests/` to make browser execution reliable on GitHub Pages.
- Added sticky top navigation with section anchors for faster movement across Problems/Runner/Progress/Paths.
- Added favorites workflow, solved-first ordering, and density toggle for list ergonomics.
- Improved empty/error states with actionable recovery guidance for filtering and test loading.
- Added first-visit onboarding coachmark with quick start steps.
- Seeded wiki-ready documentation pages (Home, Learning Paths, Authoring, Runner, FAQ).
- Published docs hub directly on GitHub Pages under `web/wiki/`.
- Added privacy-safe local insights card (strongest topic and suggested focus).

### Changed

- Hardened Python runner with AST safety validation, blocked dangerous calls, and per-test process timeouts.
- Added explicit benchmark tier labeling (`strict` vs `advisory`) in runner and browser outputs.
- Upgraded content validator with typed schema checks, enums, and web catalog integrity checks.
- Added generation tooling to scale content (`scripts/generate_scale_batch.py`) and maintain author velocity.
- Added `scripts/build_web_catalog.py` and CI check to keep catalog generation in sync.
- Added CI enforcement for quality scoring gates and generated report freshness.

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
