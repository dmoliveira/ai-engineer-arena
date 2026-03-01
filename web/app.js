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
  const selected = difficultyFilter.value;
  return problems.filter((problem) => selected === "all" || problem.difficulty === selected);
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
