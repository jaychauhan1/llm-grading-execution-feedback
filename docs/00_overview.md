# Overview

This repo documents a research project: whether execution-derived evidence
(unit tests, stderr, timeouts) makes LLM code grading more accurate and more
consistent than code-only judging.

We evaluate 5 problems:
- Group Anagrams
- Top K Frequent Elements
- Encode and Decode Strings
- Product of Array Except Self
- Longest Consecutive Sequence

For each submission, we grade under 4 conditions:
- C1: Code-only
- C2: Code + stdout/stderr
- C3: Code + structured unit test results
- C4: Code + failing-test traces (inputs/expected/got)

We measure:
- Accuracy vs ground-truth labels
- Consistency (variance across repeated grading runs)
- Hallucination rate

