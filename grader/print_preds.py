import os, json, re

PROBLEM_ID = "longest_consecutive"
FNAME_RE = re.compile(r"^(?P<sub>.+)_(?P<cond>C[1-4])_run(?P<run>\d+)\.json$")

def main():
    labels = json.load(open(f"problems/{PROBLEM_ID}/submissions/labels.json", "r", encoding="utf-8"))
    grade_dir = f"results/grades/{PROBLEM_ID}"

    preds = {}  # (sub_py, cond) -> verdict
    reasons = {}  # (sub_py, cond) -> reasons/score for quick inspection

    for fname in sorted(os.listdir(grade_dir)):
        m = FNAME_RE.match(fname)
        if not m:
            continue
        sub_py = m.group("sub") + ".py"
        cond = m.group("cond")

        data = json.load(open(os.path.join(grade_dir, fname), "r", encoding="utf-8"))
        parsed = data.get("parsed")
        if not parsed:
            continue
        verdict = str(parsed.get("verdict", "")).strip().lower()
        if not verdict:
            continue
        preds[(sub_py, cond)] = verdict
        reasons[(sub_py, cond)] = {
            "score": parsed.get("score"),
            "confidence": parsed.get("confidence"),
            "reasons": parsed.get("reasons"),
        }

    for cond in ["C1", "C3", "C4"]:
        print("\n===", cond, "===")
        for sub_py, gt in labels.items():
            pred = preds.get((sub_py, cond))
            info = reasons.get((sub_py, cond))
            print(f"{sub_py:35} gt={gt:9} pred={str(pred):9} score={info.get('score') if info else None} conf={info.get('confidence') if info else None}")
            if info and info.get("reasons"):
                print("  reasons:", info["reasons"])

if __name__ == "__main__":
    main()
