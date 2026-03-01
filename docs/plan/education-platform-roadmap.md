# AI Engineer Arena - Product and Delivery Plan

## Vision

Create a professional, educational platform where users grow from foundational coding skills to advanced software engineering and machine learning practice through structured challenges, deep editorials, and measurable progress.

## Product goals

- Deliver a LeetCode/HackerRank/Codeforces-inspired experience focused on AI/ML engineers.
- Cover computer science fundamentals plus data science and ML implementation workflows.
- Provide practical shell challenge tracks for Linux command fluency.
- Support local-first progress and submissions in early phases (no database requirement).
- Launch as a public MIT-licensed repository and GitHub Pages educational product.

## Users and learning outcomes

### Target users

- AI/ML engineers improving software engineering depth.
- Software engineers expanding into data science/ML workflows.
- Students and interview candidates preparing with practical progression.

### Learning outcomes

- Apply core algorithms and data structures under performance constraints.
- Build correct, efficient, and readable solutions.
- Analyze runtime, memory, and trade-offs across solution strategies.
- Execute shell-based workflows for data processing and automation.
- Develop practical ML/data analysis intuition through coding-focused exercises.

## Scope and non-goals

### In scope (phase 1)

- Python 3 challenge support
- problem taxonomy and difficulty progression
- local test execution and hidden stress tests
- editorial solution pages with multi-approach analysis
- static site delivery via GitHub Pages
- browser Python execution (Pyodide)
- local solved-history storage

### Out of scope (phase 1)

- user accounts and cloud persistence
- paid content or subscription logic
- multi-language execution engines beyond Python

## Content taxonomy

### Algorithm and data-structure tracks

- strings
- arrays
- sorting and searching
- hash maps and sets
- recursion and backtracking
- dynamic programming
- trees (binary trees, BST, decision trees where algorithmic)
- graphs (traversal, shortest path, union-find)
- advanced structures (heaps, tries, segment trees)

### Data and ML tracks

- data cleaning and preprocessing
- feature engineering
- exploratory data analysis
- classification and prediction tasks
- model evaluation and selection
- optimization basics and trade-offs

### Shell tracks

- single-command basics (`grep`, `awk`, `sort`, `uniq`, `cut`)
- two-command pipelines
- multi-step workflow challenges with hints only

## Exercise model

Each problem includes:

- statement and constraints
- input/output specification
- simple public sample tests
- hidden advanced tests for correctness/performance/memory
- tags (topic, difficulty, interview relevance)
- editorial with at least two approaches where suitable
- complexity analysis and recommendations

## Editorial framework

For each problem solution page:

- `Approach A (Foundational)`: clear baseline logic
- `Approach B (Optimized)`: preferred interview approach
- `Approach C (Advanced)`: optional deeper technique for selected problems
- complexity table (time, space)
- trade-off explanation (clarity vs speed vs memory)
- recommendation labels: `Interview Recommended`, `Production Practical`, `Advanced/Research`

## Technical architecture (phase 1)

### Repository domains

- `problems/`: problem statements, metadata, and tests
- `runner/`: local execution harness and metrics collection
- `web/`: static GitHub Pages app for browsing/running problems
- `docs/`: planning, specs, contribution guidance

### Data contracts

- `problem.yaml`: id, title, category, difficulty, tags, constraints
- `tests/public.json`: sample tests
- `tests/hidden.json`: stress and edge tests (local only, not exposed in pages output)
- `editorial.md`: approaches and analysis

### Execution and metrics

- run against public + hidden tests
- collect pass rate and aggregate runtime
- estimate memory usage locally where possible
- output machine-readable result payloads for web rendering

## GitHub Pages compatibility plan

- use static assets only (HTML/CSS/JS)
- integrate Pyodide for browser Python runtime
- avoid server dependencies
- store progress in `localStorage`
- provide deterministic, client-side result rendering with charts

## Gamification design

- progression ladder: Easy -> Medium -> Hard
- category streaks and completion percentages
- badges for milestones (first solve, 10 solves, all Easy in category)
- challenge score weighting by difficulty and efficiency
- visible recommendation for next problem based on solved history

## Quality strategy

### Validation levels

1. logic correctness
2. performance checks (runtime thresholds)
3. memory sanity checks for designated problems

### Anti-bruteforce design

- hidden tests include high-input constraints
- edge-case heavy scenarios
- multiple randomized seeds for selected categories

## Epics, tasks, and subtasks

## Epic 1 - Foundation and standards

### Task 1.1 Repository scaffolding

- define folder structure
- configure MIT license and base docs
- add contribution and coding conventions

#### Subtasks

- create directory skeleton
- create templates for problem package
- add issue/PR templates

### Task 1.2 Metadata contracts

- define `problem.yaml` schema
- define tests payload format
- define result payload format

#### Subtasks

- author schema examples
- validate sample assets with lightweight checker

## Epic 2 - Problem authoring system

### Task 2.1 Problem specification template

- standard markdown template for statements
- constraint and examples sections
- acceptance checklist for editorial quality

#### Subtasks

- create reusable template files
- create first 10 seed problems across categories

### Task 2.2 Hidden/public test strategy

- separate public and hidden tests
- support stress patterns by category

#### Subtasks

- add stress generator for arrays/graphs
- define memory-test markers

## Epic 3 - Runner and evaluation engine (Python)

### Task 3.1 Local runner MVP

- execute candidate solution against tests
- produce pass/fail and runtime summary

#### Subtasks

- sandboxed imports policy
- timeout handling per test
- deterministic reporting format

### Task 3.2 Metrics and ranking model

- calculate average runtime and total runtime
- capture coarse memory usage

#### Subtasks

- integrate timing utility
- integrate memory snapshot utility
- create scoring formula with thresholds

## Epic 4 - Educational editorials

### Task 4.1 Editorial standard

- require at least baseline + optimized methods
- enforce complexity table and trade-off notes

#### Subtasks

- create editorial lint checklist
- create sample editorials for 5 problems

## Epic 5 - Web experience on GitHub Pages

### Task 5.1 Static app MVP

- list and filter problems
- problem detail page
- code editor and run button

#### Subtasks

- implement index and category pages
- implement detail route strategy
- render result panel and basic charts

### Task 5.2 Browser Python runtime

- integrate Pyodide runtime
- run sample tests in browser safely

#### Subtasks

- load runtime with caching strategy
- show execution progress and errors cleanly
- persist recent submissions locally

## Epic 6 - Shell challenge track

### Task 6.1 Shell content framework

- define challenge format with command hints
- include single-tool, two-tool, and pipeline levels

#### Subtasks

- author 15 seed shell challenges
- define expected output validator format

## Epic 7 - Release and project operations

### Task 7.1 CI and docs pipeline

- lint and validate metadata
- run sample tests in CI
- publish GitHub Pages

#### Subtasks

- create CI workflow
- configure pages deployment action
- add release checklist

## Definition of Done (global)

- feature implemented and documented
- tests for new behavior included and passing
- docs reflect current behavior (no stale references)
- validation command outputs recorded in PR
- no high-severity review findings unresolved

## Acceptance criteria by release stage

### Milestone M1 - Planning and skeleton

- planning docs approved
- repository scaffold committed
- initial templates available

### Milestone M2 - Python runner alpha

- local runner executes at least 20 problems
- supports hidden/public tests and timing

### Milestone M3 - GitHub Pages beta

- users can browse and run Python sample tests in browser
- results and progression tracked locally

### Milestone M4 - Educational maturity

- at least 100 high-quality problems across categories
- editorial standards consistently applied

## Assumptions

- GitHub Pages remains static-hosting only.
- Browser runtime limits require bounded test sizes in-client.
- Hidden tests for strict anti-cheat remain local/developer-side in phase 1.
- Users accept local-only solved history before account system exists.

## Conventions

- naming: kebab-case paths, snake_case Python modules
- one problem per folder with metadata/tests/editorial bundle
- deterministic test seeds when randomization is used
- all public docs in clear, education-first language

## Risks and mitigations

- **Risk:** browser runtime performance inconsistency
  - **Mitigation:** compare against local runner and label browser metrics as advisory
- **Risk:** brute-force bypass on simple tests
  - **Mitigation:** hidden stress tests and stricter constraints
- **Risk:** content quality drift at scale
  - **Mitigation:** editorial checklist and reviewer gate before publish

## Immediate next iteration plan

1. finalize templates for problem packs and metadata contracts
2. create 10 seed problems (mixed categories and difficulties)
3. implement Python local runner MVP with timing + pass/fail output
4. scaffold static pages for listing and viewing problems
