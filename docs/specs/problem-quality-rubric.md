# Problem Quality Rubric v1

This rubric defines baseline quality scoring for all problem packs.

## Scoring dimensions (100 max)

- Metadata completeness: 20
- Statement depth: 15
- Editorial depth: 15
- Public tests presence: 25
- Hidden tests presence: 15 (10 minimum if hidden array exists but empty)

## Tiers

- Gold: 90+
- Silver: 70-89
- Bronze: below 70

## CI gates

- No problem can be below minimum score (`--min-score`, default 70).
- Gold-count target must be met (`--target-gold`, baseline 10 in CI, planned ramp to 30).
- The report is generated at `docs/specs/problem-quality-report.json`.

## Usage

```bash
python3 scripts/score_problem_quality.py
```
