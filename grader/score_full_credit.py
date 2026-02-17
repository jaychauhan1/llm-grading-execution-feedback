import os, json, re

PROBLEM_ID = "longest_consecutive"
FNAME_RE = re.compile(r"^(?P<sub>.+)_(?P<cond>C[1-4])_run(?P<run>\d+)\.json$")

def main():
    labels = json.load(open(f"problems/{PROBLEM_ID}/submissions/labels.json", "r", encoding="utf-8"))
    grade_dir = f"results/grades/{PROBLEM_ID}"

    preds = {}  # (sub_py, cond) -> verdict (run1)
    for fname in os.listdir(grade_dir):
        m = FNAME_RE.match(fname)
        if not m or m.group("run") != "1":
            continue
        sub_py = m.group("sub") + ".py"
        cond = m.group("cond")
        data = json.load(open(os.path.join(grade_dir, fname), "r", encoding="utf-8"))
        parsed = data.get("parsed") or {}
        v = str(parsed.get("verdict", "")).strip().lower()
        if v:
            preds[(sub_py, cond)] = v

    def gt_is_correct(gt: str) -> bool:
        return gt.strip().lower() == "correct"

    def pred_is_correct(v: str) -> bool:
        return v.strip().lower() == "correct"

    for cond in ["C1", "C3", "C4"]:
        tp = fp = fn = 0
        for sub_py, gt in labels.items():
            v = preds.get((sub_py, cond))
            if v is None:
                continue
            gt_c = gt_is_correct(gt)
            pr_c = pred_is_correct(v)
            if pr_c and gt_c:
                tp += 1
            elif pr_c and (not gt_c):
                fp += 1
            elif (not pr_c) and gt_c:
                fn += 1

        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        print(f"{cond} correct-precision={prec:.3f} correct-recall={rec:.3f} (tp={tp} fp={fp} fn={fn})")

if __name__ == "__main__":
    main()
