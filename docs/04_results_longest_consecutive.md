# Results: Longest Consecutive Sequence

Model: Qwen2.5-Coder-7B-Instruct  
Runs per condition: 5

## Rubric Accuracy (3-class)

| Condition | Accuracy |
|-----------|----------|
C1 (code only) | 2 / 4 |
C3 (code + test summary) | 2 / 4 |
C4 (code + traces) | 2 / 4 |

## Full-Credit Detection

| Condition | Precision | Recall |
|-----------|-----------|--------|
C1 | 1.00 | 1.00 |
C3 | 1.00 | 1.00 |
C4 | 0.50 | 1.00 |

## Consistency (majority agreement across 5 runs)

| Condition | Agreement |
|-----------|-----------|
C1 | 1.00 |
C3 | 1.00 |
C4 | 1.00 |

## Key Observation

Failure traces corrected a hallucinated complexity critique for one submission,
causing the model to mark it as fully correct based on observed execution behavior.
This improves behavioral grading but reduces strict rubric precision.
