# LLMGeneratedCodePowerConsumption

This repository investigates the energy consumption and performance of coding solutions generated/refactored by large language models (LLMs). The original study measured baseline (human-written) solutions against LLM-generated ones (ChatGPT 4o, OpenAI o1-mini, GitHub Copilot) using `perf`/`powermetrics`.

This fork (`replication-study` branch) runs a **replication**: Claude Code is asked to refactor a subset of the same human-written solutions for energy efficiency, measured with [`codecarbon`](https://docs.codecarbon.io/) instead of `perf`/`powermetrics`. The Codex refactoring now has 51 variants and correctness checks; Codex energy measurements remain pending. See [Codex_Experiment_Procedure.md](Codex_Experiment_Procedure.md) for results and usage-metric limitations.

---

## Repository Structure

### **Top-level files**

- **`AI-Powered_But_Power-Hungry_Energy_Efficiency_of_LLM-Generated_Code-4.pdf`**: The paper behind the original study.
- **`PROMPT.md`**: The exact prompts used to ask Claude Code and Codex to refactor the human-written solutions, and how each one's own usage metrics (tokens, tool calls, turns, wall-clock time) are derived from its session transcript.
- **`Claude_Experiment_Procedure.md`**: A transparency log of what was actually done to produce `Results/code/claude/`, including a token-counting mistake that was found and corrected, the validation tooling built, and pre-existing bugs found in the human-written baseline.
- **`requirements.txt`**: Python dependencies (notably `codecarbon`, `pandas`, `scipy`, `seaborn`) for running the scripts and notebook below.

### **Folders**

#### **Sheets**

- **`LeetCodeBenchmark.xlsx`**: Contains the benchmark problems used in the study.
- **`Tasks_and_Tags.xlsx`**: Lists all problems and their associated tags.
- **`Prompt_Structure.png`**: A visual representation of the prompt setup used in the original study.
- **`Grouping_of_Tags.xlsx`**: Groups tags into broader categories of programming tasks.

#### **src**

- **`data/human/`**: Baseline coding solutions written by humans and taken from LeetCode, one subfolder per problem, with separate files for Python, C++, and Java implementations.
- **`config/constants.py`**: Single source of truth for the replication — the 17 selected problems (name, LeetCode number, tags, per-language filename), language/source constants, and path helpers. Both `src/data/human/` and `Results/code/claude/` use the same per-language filename for a given problem.
- **`utils.py`**: Shared helpers to compile (C++/Java) and run a program for any language/source.
- **`validate_program_execution.py`**: Compiles and runs every problem for `human` and `claude`, reporting finished/failed with timing. Run with `python3 src/validate_program_execution.py` (optionally followed by `human` or `claude` to check just one side).
- **`codecarbon_metrics_from_code.py`**: Runs every problem `CODECARBON_RUNS` times per source/language, measuring energy/CO2 with `codecarbon`, and writes each run's results to `Analysis/data/code/<source>/<Problem>/<language>/emissions.csv`. Run with `.venv/bin/python3 src/codecarbon_metrics_from_code.py`.

#### **Results**

- **`code/claude/<Problem>/`**: Claude Code's energy-refactored solution for each of the 17 selected problems, in Python, Java, and C++, using the same filenames as `src/data/human/`. Each solution is accompanied by a `<filename>.txt` file recording that variant's LLM usage metrics (total tokens, tool-call count, model-turn count, wall-clock time) — see `PROMPT.md`/`Claude_Experiment_Procedure.md`.
- **`code/codex/`**: 51 refactored variants, snapshot-metric sidecars, per-variant verification records, and `validation.json`. Run `python3 -B src/verify_codex_replication.py` for isolated correctness checks: 48 embedded suites pass and 3 retain documented baseline runtime failures. Metrics are snapshot-derived and do not reliably isolate per-variant LLM effort; see [Codex_Experiment_Procedure.md](Codex_Experiment_Procedure.md).

#### **Analysis**

- **`data/code/<source>/<Problem>/<language>/emissions.csv`**: Raw, per-run `codecarbon` measurements (energy, CO2, duration, CPU/GPU/RAM power and energy breakdown) produced by `src/codecarbon_metrics_from_code.py`, for `source` in `human`/`claude`.
- **`LLM_Refactoring_Energy_Analysis.ipynb`**: The analysis notebook — loads every `emissions.csv` cell via `src/config/constants.py`, and answers:
  - **General RQ**: To what extent is it possible to obtain energy-efficient code through LLM refactoring?
  - **RQ1**: How does the energy efficiency of LLM-refactored code vary across languages (Python, C++, Java)?
  - **RQ2**: What is the impact of data structure/algorithmic technique choice on the energy efficiency of refactored code?
  - **RQ3**: Is the energy efficiency of code refactored by different LLMs (Claude Code, Codex) significantly different? (no data yet — see above)

  Uses a two-level non-parametric design (Mann-Whitney U per problem, Wilcoxon signed-rank pooling `delta_percent` across problems per language/category, Cliff's delta effect size, Holm-Bonferroni correction) — see the notebook's methodology section for the full rationale and current caveats (`CODECARBON_RUNS=2` in this run, so only pooled/Level-2 comparisons have real statistical power).

---

## Usage

### 1. Setup

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 2. Validate the baseline and refactored solutions compile/run

```
.venv/bin/python3 src/validate_program_execution.py
```

### 3. Measure energy consumption

```
.venv/bin/python3 src/codecarbon_metrics_from_code.py
```

This populates `Analysis/data/code/<source>/<Problem>/<language>/emissions.csv` for every problem in `src/config/constants.py`, for both `human` and `claude`.

### 4. Analyze

Open `Analysis/LLM_Refactoring_Energy_Analysis.ipynb` to reproduce the statistical comparisons and plots for the General RQ, RQ1, and RQ2.

---

## Key findings (current run)

Pooling across all 46 measured `(problem, language)` cells (17 problems x 3 languages, minus 5 pre-existing `human`/Java compile failures), Claude Code's refactor produced a statistically significant reduction in both **energy** (median -4.02%, Wilcoxon p=0.0138) and **duration** (median -2.07%, p=0.0003) relative to the human baseline. The effect is uneven across languages (C++'s duration gain is the only one to survive multiple-comparison correction on its own) and no algorithmic category clears correction at this sample size. See the notebook's Synthesis section for the full breakdown, and `Claude_Experiment_Procedure.md` for data-quality caveats (pre-existing bugs preserved by design, small `CODECARBON_RUNS=2` sample).

---

## License

This project is licensed under the [MIT License](LICENSE).
