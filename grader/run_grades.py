import os
import json
from grader.llm_judge import grade_prompt

PROBLEM_ID = "longest_consecutive"
RUNS = 1  # later we increase for consistency experiments

def main():
    in_dir = os.path.join("results", "prompts", PROBLEM_ID)
    out_dir = os.path.join("results", "grades", PROBLEM_ID)
    os.makedirs(out_dir, exist_ok=True)

    for fname in sorted(os.listdir(in_dir)):
        if not fname.endswith(".txt"):
            continue

        prompt = open(os.path.join(in_dir, fname)).read()

        for r in range(RUNS):
            print("Grading", fname, "run", r + 1)

            output = grade_prompt(prompt)

            out_path = os.path.join(
                out_dir,
                fname.replace(".txt", f"_run{r+1}.json")
            )

            with open(out_path, "w") as f:
                json.dump({"raw_output": output}, f, indent=2)

if __name__ == "__main__":
    main()

