import os
import json

PROBLEM_ID = "longest_consecutive"

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def build():
    base = os.path.join("problems", PROBLEM_ID)
    prompt_md = read(os.path.join(base, "prompt.md"))
    rubric = read("docs/02_grading_prompt.md")

    subs_dir = os.path.join(base, "submissions")
    evidence_dir = os.path.join("results", "raw", PROBLEM_ID)

    out_dir = os.path.join("results", "prompts", PROBLEM_ID)
    os.makedirs(out_dir, exist_ok=True)

    for fname in sorted(os.listdir(subs_dir)):
        if not fname.endswith(".py"):
            continue

        code = read(os.path.join(subs_dir, fname))
        evidence = json.load(open(os.path.join(evidence_dir, fname.replace(".py", ".json"))))

        # -------- C1: code only --------
        c1 = f"""
You are grading a programming submission.

{prompt_md}

RUBRIC:
{rubric}

STUDENT CODE:
{code}

Return the required JSON.
"""
        # -------- C3: code + tests summary --------
        summary = f"""
Execution summary:
passed = {evidence['passed']}
failed = {evidence['failed']}
runtime_ms = {evidence['runtime_ms']}
"""

        c3 = f"""
You are grading a programming submission.

{prompt_md}

RUBRIC:
{rubric}

STUDENT CODE:
{code}

{summary}

Return the required JSON.
"""

        json.dump(c1, open(os.path.join(out_dir, fname.replace(".py", "_C1.txt")), "w"))
        json.dump(c3, open(os.path.join(out_dir, fname.replace(".py", "_C3.txt")), "w"))

        print("built prompts for", fname)

if __name__ == "__main__":
    build()

