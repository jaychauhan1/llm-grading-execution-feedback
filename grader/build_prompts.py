import os
import json

PROBLEM_ID = "longest_consecutive"


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    base = f"problems/{PROBLEM_ID}"
    subs_dir = os.path.join(base, "submissions")
    prompt_md = read(os.path.join(base, "prompt.md"))
    rubric = read("docs/02_grading_prompt.md")

    evidence_dir = f"results/raw/{PROBLEM_ID}"
    out_dir = f"results/prompts/{PROBLEM_ID}"
    os.makedirs(out_dir, exist_ok=True)

    for fname in sorted(os.listdir(subs_dir)):
        if not fname.endswith(".py"):
            continue

        code = read(os.path.join(subs_dir, fname))

        evidence_path = os.path.join(
            evidence_dir, fname.replace(".py", ".json")
        )
        evidence = json.load(open(evidence_path, "r", encoding="utf-8"))

        # ---------------- C1: code only ----------------
        c1 = f"""
You are grading a programming submission.

{prompt_md}

RUBRIC:
{rubric}

STUDENT CODE:
{code}

Return the required JSON.
"""

        with open(
            os.path.join(out_dir, fname.replace(".py", "_C1.txt")),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(c1)

        # ---------------- C3: code + test summary ----------------
        c3 = f"""
You are grading a programming submission.

{prompt_md}

RUBRIC:
{rubric}

STUDENT CODE:
{code}

Execution summary:
passed = {evidence['passed']}
failed = {evidence['failed']}
runtime_ms = {evidence['runtime_ms']}

Return the required JSON.
"""

        with open(
            os.path.join(out_dir, fname.replace(".py", "_C3.txt")),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(c3)

        # -------- C4: code + tests summary + failure traces --------
        if evidence.get("failed", 0) > 0:
            traces = "Failure traces (first few):\n" + json.dumps(
                evidence.get("failures", []), indent=2
            )
        else:
            traces = "Failure traces: none (all tests passed)"

        c4 = f"""
You are grading a programming submission.

{prompt_md}

RUBRIC:
{rubric}

STUDENT CODE:
{code}

Execution summary:
passed = {evidence['passed']}
failed = {evidence['failed']}
runtime_ms = {evidence['runtime_ms']}

{traces}

Return the required JSON.
"""

        with open(
            os.path.join(out_dir, fname.replace(".py", "_C4.txt")),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(c4)

        print("built prompts for", fname)


if __name__ == "__main__":
    main()
