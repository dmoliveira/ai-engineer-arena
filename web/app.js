const listNode = document.getElementById("problemList");
const titleNode = document.getElementById("problemTitle");
const metaNode = document.getElementById("problemMeta");
const promptNode = document.getElementById("problemPrompt");
const codeInput = document.getElementById("codeInput");
const runBtn = document.getElementById("runBtn");
const resultOutput = document.getElementById("resultOutput");
const runtimeStatus = document.getElementById("runtimeStatus");
const progressStats = document.getElementById("progressStats");
const difficultyFilter = document.getElementById("difficultyFilter");
const topicFilter = document.getElementById("topicFilter");
const tagFilter = document.getElementById("tagFilter");
const sortFilter = document.getElementById("sortFilter");
const searchInput = document.getElementById("searchInput");
const prevPageBtn = document.getElementById("prevPageBtn");
const nextPageBtn = document.getElementById("nextPageBtn");
const pageStatus = document.getElementById("pageStatus");
const resultsCount = document.getElementById("resultsCount");
const activeFiltersBar = document.getElementById("activeFiltersBar");
const activeFiltersText = document.getElementById("activeFiltersText");
const clearFiltersBtn = document.getElementById("clearFiltersBtn");
const recommendationCard = document.getElementById("recommendationCard");
const trackAllBtn = document.getElementById("trackAllBtn");
const trackInterviewBtn = document.getElementById("trackInterviewBtn");
const trackMlBtn = document.getElementById("trackMlBtn");
const trackStatus = document.getElementById("trackStatus");

const supportNudge = document.getElementById("supportNudge");
const supportNudgeText = document.getElementById("supportNudgeText");
const supportNudgeDismiss = document.getElementById("supportNudgeDismiss");

let pyodide;
let problems = [];
let activeProblem;
let currentPage = 1;
let activeTrack = "all";

const PAGE_SIZE = 12;
const STORAGE_KEY = "aiea-progress-v1";
const SUPPORT_NUDGE_KEY = "aiea-support-nudge-v1";
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

const TRACKS = {
  all: [],
  interview: [
    "two-sum-hash",
    "valid-anagram",
    "merge-intervals",
    "number-of-islands",
    "binary-tree-level-order",
    "detect-cycle-directed-graph",
    "kth-smallest-sorted-matrix",
  ],
  ml_engineer: [
    "clean-null-sales",
    "normalize-min-max-column",
    "group-mean-by-region",
    "logistic-threshold-classifier",
    "gradient-descent-step",
    "precision-recall-threshold",
    "early-stop-criteria",
  ],
};

function loadProgress() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

function saveProgress(progress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

function loadNudgeState() {
  const raw = localStorage.getItem(SUPPORT_NUDGE_KEY);
  if (!raw) return { dismissedUntil: 0, lastShownAt: 0 };
  try {
    return JSON.parse(raw);
  } catch {
    return { dismissedUntil: 0, lastShownAt: 0 };
  }
}

function saveNudgeState(state) {
  localStorage.setItem(SUPPORT_NUDGE_KEY, JSON.stringify(state));
}

function hideSupportNudge() {
  supportNudge.hidden = true;
}

function showSupportNudge(message) {
  supportNudgeText.textContent = message;
  supportNudge.hidden = false;
}

function maybeShowSupportNudge(solvedCount, solvedProblemTitle) {
  const now = Date.now();
  const nudgeState = loadNudgeState();
  const inCooldown = now - nudgeState.lastShownAt < 3 * ONE_DAY_MS;
  const dismissed = now < (nudgeState.dismissedUntil || 0);

  if (solvedCount < 2 || inCooldown || dismissed) return;

  showSupportNudge(
    `${solvedProblemTitle} completed. You're now at ${solvedCount} solved. If this helps, a small donation keeps new challenges coming.`,
  );
  saveNudgeState({ ...nudgeState, lastShownAt: now });
}

function renderProgress() {
  const progress = loadProgress();
  const solved = Object.values(progress).filter(Boolean).length;
  progressStats.textContent = `${solved} solved of ${problems.length} loaded`;
  renderRecommendation(progress);
}

function renderRecommendation(progress) {
  const solvedIds = new Set(
    Object.entries(progress)
      .filter(([, done]) => Boolean(done))
      .map(([id]) => id),
  );

  const pending = getVisibleProblems().filter((problem) => !solvedIds.has(problem.id));
  if (pending.length === 0) {
    recommendationCard.innerHTML =
      "<strong>All currently visible problems solved.</strong> Switch topic/path filters for a fresh challenge set.";
    return;
  }

  const rank = { easy: 0, medium: 1, hard: 2 };
  const next = [...pending].sort((a, b) => rank[a.difficulty] - rank[b.difficulty])[0];
  recommendationCard.innerHTML = `<strong>Recommended next:</strong> ${next.title} (${next.difficulty}) in ${next.category}.`;
}

function setTrack(track) {
  activeTrack = track;
  trackAllBtn.classList.toggle("active", track === "all");
  trackInterviewBtn.classList.toggle("active", track === "interview");
  trackMlBtn.classList.toggle("active", track === "ml_engineer");

  if (track === "all") {
    trackStatus.textContent = "Showing all available problems.";
  } else if (track === "interview") {
    trackStatus.textContent = "Interview path loaded: algorithm-heavy fundamentals and graph/tree patterns.";
  } else {
    trackStatus.textContent = "ML engineer path loaded: data cleaning, modeling, and optimization essentials.";
  }

  currentPage = 1;
  renderProblemList();
  syncActiveProblemWithFilters();
  renderProgress();
}

function isInActiveTrack(problem) {
  if (activeTrack === "all") return true;
  const trackIds = new Set(TRACKS[activeTrack] || []);
  return trackIds.has(problem.id);
}

function getVisibleProblems() {
  const selectedDifficulty = difficultyFilter.value;
  const selectedTopic = topicFilter.value;
  const selectedTag = tagFilter.value;
  const selectedSort = sortFilter.value;
  const query = searchInput.value.trim().toLowerCase();

  const filtered = problems.filter((problem) => {
    const topicMatch = selectedTopic === "all" || problem.category === selectedTopic;
    const difficultyMatch = selectedDifficulty === "all" || problem.difficulty === selectedDifficulty;
    const tagMatch = selectedTag === "all" || (problem.tags || []).includes(selectedTag);
    const trackMatch = isInActiveTrack(problem);
    const searchSpace = [problem.id, problem.title, ...(problem.tags || [])].join(" ").toLowerCase();
    const queryMatch = !query || searchSpace.includes(query);
    return topicMatch && difficultyMatch && tagMatch && trackMatch && queryMatch;
  });

  const rank = { easy: 0, medium: 1, hard: 2 };
  if (selectedSort === "title_asc") {
    filtered.sort((a, b) => a.title.localeCompare(b.title));
  } else if (selectedSort === "difficulty_asc") {
    filtered.sort((a, b) => rank[a.difficulty] - rank[b.difficulty]);
  } else if (selectedSort === "difficulty_desc") {
    filtered.sort((a, b) => rank[b.difficulty] - rank[a.difficulty]);
  } else {
    filtered.sort((a, b) => {
      if (a.category !== b.category) return a.category.localeCompare(b.category);
      return rank[a.difficulty] - rank[b.difficulty];
    });
  }

  return filtered;
}

function setActive(problem) {
  activeProblem = problem;
  titleNode.textContent = problem.title;
  metaNode.textContent = `${problem.category} | ${problem.difficulty} | ${problem.track}`;
  promptNode.textContent = problem.prompt;
  codeInput.value = problem.starter || "def solve(*args, **kwargs):\n    pass\n";
  resultOutput.textContent = "Ready. Click Run to execute available public tests.";
  hideSupportNudge();

  const runnable = problem.track === "python";
  codeInput.disabled = !runnable;
  runBtn.disabled = !runnable;
  if (!runnable) {
    resultOutput.textContent =
      "Shell-track problem selected. Use the command hints and terminal workflow to solve this challenge.";
  }

  [...listNode.querySelectorAll("button")].forEach((button) => {
    button.classList.toggle("active", button.dataset.problemId === problem.id);
  });
}

function renderTopicFilter() {
  const topics = [...new Set(problems.map((problem) => problem.category))].sort();
  topicFilter.innerHTML = '<option value="all">All</option>';
  for (const topic of topics) {
    const option = document.createElement("option");
    option.value = topic;
    option.textContent = topic;
    topicFilter.appendChild(option);
  }
}

function renderTagFilter() {
  const tags = [...new Set(problems.flatMap((problem) => problem.tags || []))].sort();
  tagFilter.innerHTML = '<option value="all">All</option>';
  for (const tag of tags) {
    const option = document.createElement("option");
    option.value = tag;
    option.textContent = tag;
    tagFilter.appendChild(option);
  }
}

function syncActiveProblemWithFilters() {
  const visible = getVisibleProblems();
  if (visible.length === 0) {
    listNode.innerHTML = "";
    resultOutput.textContent = "No problems match the current filters.";
    return;
  }
  if (!activeProblem || !visible.some((problem) => problem.id === activeProblem.id)) {
    setActive(visible[0]);
  }
}

function renderProblemList() {
  const visible = getVisibleProblems();
  const selectedSort = sortFilter.value;
  const totalPages = Math.max(1, Math.ceil(visible.length / PAGE_SIZE));
  if (currentPage > totalPages) currentPage = totalPages;
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageItems = visible.slice(start, start + PAGE_SIZE);
  resultsCount.textContent = `${visible.length} results`;

  const activeTokens = [];
  if (topicFilter.value !== "all") activeTokens.push(`topic: ${topicFilter.value}`);
  if (difficultyFilter.value !== "all") activeTokens.push(`difficulty: ${difficultyFilter.value}`);
  if (tagFilter.value !== "all") activeTokens.push(`tag: ${tagFilter.value}`);
  if (searchInput.value.trim()) activeTokens.push(`search: ${searchInput.value.trim()}`);
  if (activeTrack !== "all") {
    activeTokens.push(activeTrack === "interview" ? "path: interview" : "path: ml engineer");
  }
  if (selectedSort !== "recommended") activeTokens.push(`sort: ${selectedSort}`);

  if (activeTokens.length > 0) {
    activeFiltersText.textContent = activeTokens.join(" | ");
    activeFiltersBar.hidden = false;
  } else {
    activeFiltersBar.hidden = true;
  }

  listNode.innerHTML = "";
  for (const problem of pageItems) {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.dataset.problemId = problem.id;
    button.innerHTML = `
      <span class="problem-card-title">${problem.title}</span>
      <span class="problem-meta-row">
        <span class="mini-badge ${problem.difficulty}">${problem.difficulty}</span>
        <span class="mini-badge">${problem.category}</span>
        <span class="mini-id">${problem.id}</span>
      </span>
    `;
    button.addEventListener("click", () => setActive(problem));
    item.appendChild(button);
    listNode.appendChild(item);
  }

  pageStatus.textContent = `Page ${currentPage} / ${totalPages}`;
  prevPageBtn.disabled = currentPage <= 1;
  nextPageBtn.disabled = currentPage >= totalPages;
}

async function initPyodideRuntime() {
  runtimeStatus.classList.remove("ok", "bad");
  runtimeStatus.textContent = "Loading Pyodide runtime...";
  pyodide = await loadPyodide();
  runtimeStatus.classList.add("ok");
  runtimeStatus.textContent = "Pyodide ready";
}

async function ensurePublicTests(problem) {
  if (problem.public_tests) return problem.public_tests;
  if (!problem.public_test_path) return [];
  const response = await fetch(`../${problem.public_test_path}`);
  const payload = await response.json();
  problem.public_tests = payload.tests || [];
  problem.function = payload.function || "solve";
  return problem.public_tests;
}

async function runTests() {
  if (!activeProblem) return;
  if (activeProblem.track !== "python") {
    resultOutput.textContent = "Shell-track problems are solved in terminal mode; browser run is disabled.";
    return;
  }
  if (!pyodide) {
    resultOutput.textContent = "Runtime still loading. Try again in a moment.";
    return;
  }

  const tests = await ensurePublicTests(activeProblem);
  if (!tests.length) {
    resultOutput.textContent = "No public tests available for this problem.";
    return;
  }

  try {
    runBtn.disabled = true;
    const start = performance.now();
    const codeLiteral = JSON.stringify(codeInput.value);
    const testsLiteral = JSON.stringify(tests);
    const functionName = activeProblem.function || "solve";

    const pyScript = `
import json

namespace = {}
exec(${codeLiteral}, namespace)
solve = namespace.get(${JSON.stringify(functionName)})
if solve is None:
    raise ValueError('Required function was not found')

tests = json.loads(${JSON.stringify(testsLiteral)})
results = []
for test in tests:
    output = solve(**test['input'])
    ok = output == test['expected']
    results.append({'name': test['name'], 'passed': ok, 'expected': test['expected'], 'output': output})

json.dumps(results)
`;

    const raw = await pyodide.runPythonAsync(pyScript);
    const parsed = JSON.parse(raw);
    const passed = parsed.filter((row) => row.passed).length;
    const elapsed = performance.now() - start;

    resultOutput.textContent = JSON.stringify(
      {
        passed,
        total: parsed.length,
        avg_runtime_ms: Number((elapsed / parsed.length).toFixed(3)),
        total_runtime_ms: Number(elapsed.toFixed(3)),
        benchmark_tier: "advisory",
        metrics: {
          runtime: "advisory (browser-dependent)",
          memory: "not measured in browser runner",
        },
        tests: parsed,
      },
      null,
      2,
    );

    if (passed === parsed.length) {
      const progress = loadProgress();
      progress[activeProblem.id] = true;
      saveProgress(progress);
      renderProgress();
      const solvedCount = Object.values(progress).filter(Boolean).length;
      maybeShowSupportNudge(solvedCount, activeProblem.title);
    } else {
      hideSupportNudge();
    }
  } catch (error) {
    runtimeStatus.classList.remove("ok");
    runtimeStatus.classList.add("bad");
    runtimeStatus.textContent = "Execution error";
    resultOutput.textContent = String(error);
  } finally {
    runBtn.disabled = activeProblem.track !== "python";
  }
}

async function loadCatalog() {
  const fullCatalogResponse = await fetch("full-catalog.json");
  if (fullCatalogResponse.ok) {
    return fullCatalogResponse.json();
  }
  const fallbackResponse = await fetch("problems.json");
  return fallbackResponse.json();
}

async function bootstrap() {
  problems = await loadCatalog();
  renderTopicFilter();
  renderTagFilter();
  setTrack("all");
  renderProblemList();
  renderProgress();
  syncActiveProblemWithFilters();
  initPyodideRuntime();
}

function onFilterChange() {
  currentPage = 1;
  renderProblemList();
  syncActiveProblemWithFilters();
  renderProgress();
}

difficultyFilter.addEventListener("change", onFilterChange);
topicFilter.addEventListener("change", onFilterChange);
tagFilter.addEventListener("change", onFilterChange);
sortFilter.addEventListener("change", onFilterChange);
searchInput.addEventListener("input", onFilterChange);

prevPageBtn.addEventListener("click", () => {
  currentPage = Math.max(1, currentPage - 1);
  renderProblemList();
});
nextPageBtn.addEventListener("click", () => {
  currentPage += 1;
  renderProblemList();
});

trackAllBtn.addEventListener("click", () => setTrack("all"));
trackInterviewBtn.addEventListener("click", () => setTrack("interview"));
trackMlBtn.addEventListener("click", () => setTrack("ml_engineer"));

clearFiltersBtn.addEventListener("click", () => {
  topicFilter.value = "all";
  difficultyFilter.value = "all";
  tagFilter.value = "all";
  sortFilter.value = "recommended";
  searchInput.value = "";
  setTrack("all");
});

supportNudgeDismiss.addEventListener("click", () => {
  const now = Date.now();
  const nudgeState = loadNudgeState();
  saveNudgeState({ ...nudgeState, dismissedUntil: now + 14 * ONE_DAY_MS });
  hideSupportNudge();
});

runBtn.addEventListener("click", runTests);

document.addEventListener("keydown", (event) => {
  const target = event.target;
  const isTypingField =
    target instanceof HTMLInputElement ||
    target instanceof HTMLTextAreaElement ||
    target instanceof HTMLSelectElement;

  if (event.key === "/" && !isTypingField) {
    event.preventDefault();
    searchInput.focus();
    searchInput.select();
    return;
  }

  if (event.key === "Escape" && document.activeElement === searchInput && searchInput.value) {
    searchInput.value = "";
    onFilterChange();
  }
});

bootstrap();
