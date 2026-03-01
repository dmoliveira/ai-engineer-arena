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

let pyodide;
let problems = [];
let activeProblem;

const STORAGE_KEY = "aiea-progress-v1";

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
