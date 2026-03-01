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
const recommendationCard = document.getElementById("recommendationCard");
const supportNudge = document.getElementById("supportNudge");
const supportNudgeText = document.getElementById("supportNudgeText");
const supportNudgeDismiss = document.getElementById("supportNudgeDismiss");

let pyodide;
let problems = [];
let activeProblem;

const STORAGE_KEY = "aiea-progress-v1";
const SUPPORT_NUDGE_KEY = "aiea-support-nudge-v1";
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

function loadNudgeState() {
  const raw = localStorage.getItem(SUPPORT_NUDGE_KEY);
  if (!raw) {
    return { dismissedUntil: 0, lastShownAt: 0 };
  }
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

  if (solvedCount < 2 || inCooldown || dismissed) {
    return;
  }

  showSupportNudge(
    `${solvedProblemTitle} completed. You're now at ${solvedCount} solved. If this helps, a small donation keeps new challenges coming.`,
  );
  saveNudgeState({
    ...nudgeState,
    lastShownAt: now,
  });
}

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

  const pending = problems.filter((problem) => !solvedIds.has(problem.id));
  if (pending.length === 0) {
    recommendationCard.innerHTML =
      "<strong>All loaded problems solved.</strong> Great momentum. Next step: add more packs and keep the streak.";
    return;
  }

  const categorySolvedCount = {};
  for (const problem of problems) {
    if (!solvedIds.has(problem.id)) continue;
    categorySolvedCount[problem.category] = (categorySolvedCount[problem.category] || 0) + 1;
  }

  const next = pending.sort((a, b) => {
    const solvedA = categorySolvedCount[a.category] || 0;
    const solvedB = categorySolvedCount[b.category] || 0;
    if (solvedA !== solvedB) return solvedA - solvedB;
    const rank = { easy: 0, medium: 1, hard: 2 };
    return rank[a.difficulty] - rank[b.difficulty];
  })[0];

  recommendationCard.innerHTML = `<strong>Recommended next:</strong> ${next.title} (${next.difficulty}) in ${next.category}.`;
}

function setActive(problem) {
  activeProblem = problem;
  titleNode.textContent = problem.title;
  metaNode.textContent = `${problem.category} | ${problem.difficulty}`;
  promptNode.textContent = problem.prompt;
  codeInput.value = problem.starter;
  resultOutput.textContent = "Ready. Click Run to execute public tests.";
  hideSupportNudge();

  [...listNode.querySelectorAll("button")].forEach((button) => {
    button.classList.toggle("active", button.dataset.problemId === problem.id);
  });
}

function filterProblems() {
  const selectedDifficulty = difficultyFilter.value;
  const selectedTopic = topicFilter.value;
  return problems.filter((problem) => {
    const topicMatch = selectedTopic === "all" || problem.category === selectedTopic;
    const difficultyMatch = selectedDifficulty === "all" || problem.difficulty === selectedDifficulty;
    return topicMatch && difficultyMatch;
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

function renderProblemList() {
  listNode.innerHTML = "";
  for (const problem of filterProblems()) {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.dataset.problemId = problem.id;
    button.textContent = `${problem.title} (${problem.difficulty})`;
    button.addEventListener("click", () => setActive(problem));
    item.appendChild(button);
    listNode.appendChild(item);
  }
}

async function initPyodideRuntime() {
  runtimeStatus.classList.remove("ok", "bad");
  runtimeStatus.textContent = "Loading Pyodide runtime...";
  pyodide = await loadPyodide();
  runtimeStatus.classList.add("ok");
  runtimeStatus.textContent = "Pyodide ready";
}

async function runTests() {
  if (!activeProblem) return;
  if (!pyodide) {
    resultOutput.textContent = "Runtime still loading. Try again in a moment.";
    return;
  }

  try {
    runBtn.disabled = true;
    const start = performance.now();

    const codeLiteral = JSON.stringify(codeInput.value);
    const testsLiteral = JSON.stringify(activeProblem.public_tests);
    const pyScript = `
import json

namespace = {}
exec(${codeLiteral}, namespace)
solve = namespace.get('solve')
if solve is None:
    raise ValueError('Function solve was not found')

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
    runBtn.disabled = false;
  }
}

async function bootstrap() {
  const response = await fetch("problems.json");
  problems = await response.json();
  renderTopicFilter();
  renderProblemList();
  renderProgress();
  setActive(problems[0]);
  initPyodideRuntime();
}

difficultyFilter.addEventListener("change", () => {
  renderProblemList();
  if (!filterProblems().includes(activeProblem)) {
    const available = filterProblems();
    if (available.length > 0) {
      setActive(available[0]);
    }
  }
});

topicFilter.addEventListener("change", () => {
  renderProblemList();
  if (!filterProblems().includes(activeProblem)) {
    const available = filterProblems();
    if (available.length > 0) {
      setActive(available[0]);
    }
  }
});

runBtn.addEventListener("click", runTests);
bootstrap();

supportNudgeDismiss.addEventListener("click", () => {
  const now = Date.now();
  const nudgeState = loadNudgeState();
  saveNudgeState({
    ...nudgeState,
    dismissedUntil: now + 14 * ONE_DAY_MS,
  });
  hideSupportNudge();
});
