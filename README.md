# LLM Grading with Execution Feedback

Execution-grounded code evaluation pipeline using **Qwen**.  
The system runs student programs in a sandbox, captures runtime behavior, and uses the model to generate **structured JSON grading feedback**.

---

## Overview

This project evaluates student solutions by combining:

1. Code
2. Program execution
3. Runtime evidence (outputs, errors, exit status)

The LLM grades based on **what the code actually does**, not just static inspection.

---

## Features

- Sandboxed execution of student code
- Runtime signal collection:
  - stdout  
  - stderr  
  - exit code  
  - timeout detection
- Structured JSON grading with Qwen
- Consistency analysis across multiple runs
- Three evaluation conditions:
  1. **Code only**
  2. **Code + test results**
  3. **Code + failure traces**

---

## Repository Structure

```
grader/
  sandbox.py            # safe code execution
  llm_judge.py          # Qwen grading interface
  build_prompts.py      # prompt construction
  parse_grades.py       # JSON grade parsing
  consistency.py        # multi-run stability analysis

run_one.py              # grade a single submission
run_problem.py          # grade all submissions for one problem
run_batch.py            # run full experiment pipeline
run_grades.py           # generate grades from raw outputs

problems/
  longest_consecutive/  # dataset + test cases

results/
  raw/                  # raw model outputs
  grades/               # parsed grades
  tables/               # aggregated metrics
```

---

## Environment Setup

### 1. Create conda environment

```bash
conda create -n qwen-grade python=3.10
conda activate qwen-grade
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify GPU (recommended)

```bash
nvidia-smi
```

---

## Usage

### Run grading for one problem

```bash
python run_problem.py problems/longest_consecutive
```

### Run the full experiment pipeline

```bash
python run_batch.py
```

### Parse grades from raw outputs

```bash
python run_grades.py
```

---

## Outputs

Results are written to:

```
results/
  raw/        # model responses
  grades/     # structured JSON grades
  tables/     # consistency & accuracy metrics
```

---

## Research Goal

Move from **prompt-only grading → execution-grounded evaluation**, enabling:

- Evidence-based code assessment
- Grading consistency measurement
- Controlled comparison of runtime feedback conditions
- Integration with agent memory for longitudinal student modeling

---

## Future Work

- Rubric-based grading
- Automatic test generation & coverage
- Larger model evaluation
- Qwen-Agent memory integration
