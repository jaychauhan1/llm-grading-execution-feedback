import os
import json
import re

PROBLEM_ID = "longest_consecutive"

# Matches: s01_correct_C1_run1.json
FNAME_RE = re.compile(r"^(?P<sub>.+)_(?P<cond>C[1-4])_run(?P<run>\d+)\.json$")


def main():
    labels_path = f"problems/{PROBLEM_ID}/submissions/labels.json"
    labels = json.load(open(labels_path, "r", encoding="utf-8"))

    grade_dir = f"results/grades/{PROBLEM_ID}"
    if not os.path.isdir(grade_dir):
        raise SystemExit(f"Missing directory: {grade_dir}")

    preds = {}  # (submission_py, condition) -> verdict

    total_files = 0
    parsed_files = 0

    for fname in os.listdir(grade_dir):
        m = FNAME_RE.match(fname)
        if not m:
            continue

        total_files += 1

        sub = m.group("sub")        # s01_correct
        cond = m.group("cond")      # C1 or C3
        sub_py = sub + ".py"

        path = os.path.join(grade_dir, fname)
        data = json.load(open(path, "r", encoding="utf-8"))

        parsed = data.get("parsed")

        if not parsed or "verdict" not in parsed:
            continue

        verdict = str(parsed["verdict"]).strip().lower()

        preds[(sub_py, cond)] = verdict
        parsed_files += 1

    print(f"Found {total_files} grade files, parsed {parsed_files} verdicts.\n")

    def acc_for(cond):
        total = 0
        correct = 0
        missing = 0

        for sub_py, gt in labels.items():
            pred = preds.get((sub_py, cond))

            if pred is None:
                missing += 1
                continue

            total += 1

            if pred == gt:
                correct += 1

        return correct, total, missing

    for cond in ["C1", "C3", "C4"]:
        c, t, miss = acc_for(cond)
        print(f"{cond}: {c}/{t} (missing {miss} of {len(labels)})")


if __name__ == "__main__":
    main()
