import os
import json
import re
from grader.llm_judge import grade_prompt

PROBLEM_ID = "longest_consecutive"
RUNS = 5

def strip_code_fences(s: str) -> str:
    s = s.strip()
    # Remove ```json ... ``` or ``` ... ```
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
        s = re.sub(r"\n?```$", "", s)
    return s.strip()

def parse_json(s: str):
    s2 = strip_code_fences(s)

    # try direct parse
    try:
        obj = json.loads(s2)
        return obj
    except Exception:
        pass

    # fallback: greedy {...}
    m = re.search(r"\{.*\}", s2, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None

def main():
    in_dir = os.path.join("results", "prompts", PROBLEM_ID)
    out_dir = os.path.join("results", "grades", PROBLEM_ID)
    os.makedirs(out_dir, exist_ok=True)

    for fname in sorted(os.listdir(in_dir)):
        if not fname.endswith(".txt"):
            continue

        prompt = open(os.path.join(in_dir, fname), encoding="utf-8").read()

        for r in range(RUNS):
            print("Grading", fname, "run", r + 1)

            raw = grade_prompt(prompt)
            parsed = parse_json(raw)

            out_path = os.path.join(out_dir, fname.replace(".txt", f"_run{r+1}.json"))
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump({"raw_output": raw, "parsed": parsed}, f, indent=2)

if __name__ == "__main__":
    main()
