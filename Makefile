PROJECT_NAME := ai-engineer-arena
VERSION := 0.4.x

.PHONY: help validate quality build-catalog smoke shell-smoke new-problem

help:
	@printf "$(PROJECT_NAME) $(VERSION)\n"
	@printf "Commands:\n"
	@printf "  make validate        - Run content contract validation\n"
	@printf "  make quality         - Score quality and enforce gate\n"
	@printf "  make build-catalog   - Rebuild web/full-catalog.json\n"
	@printf "  make smoke           - Run Python runner smoke checks\n"
	@printf "  make shell-smoke     - Run shell runner smoke checks\n"
	@printf "  make new-problem     - Create new problem scaffold (requires ARGS)\n"

validate:
	python3 scripts/validate_content.py

quality:
	python3 scripts/score_problem_quality.py

build-catalog:
	python3 scripts/build_web_catalog.py

smoke:
	python3 runner/run_problem.py --problem-dir problems/algorithms/two-sum-hash --solution examples/solutions/two_sum_hash.py
	python3 runner/run_problem.py --problem-dir problems/algorithms/merge-intervals --solution examples/solutions/merge_intervals.py

shell-smoke:
	python3 runner/run_shell_problem.py --problem-dir problems/shell_lab/log-level-counter --command "cut -d' ' -f2 {input_file} | sort | uniq -c | awk '{print $$2, $$1}'"

new-problem:
	python3 scripts/new_problem.py $(ARGS)
