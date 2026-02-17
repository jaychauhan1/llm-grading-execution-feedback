import os, json, re
from collections import defaultdict, Counter

PROBLEM_ID = "longest_consecutive"
FNAME_RE = re.compile(r"^(?P<sub>.+)_(?P<cond>C[1-4])_run(?P<run>\d+)\.json$")

def main():
    grade_dir = f"results/grades/{PROBLEM_ID}"

    # group verdicts by (submission, condition)
    groups = defaultdict(list)

    for fname in os.listdir(grade_dir):
        m = FNAME_RE.match(fname)
        if not m:
            continue
        sub = m.group("sub") + ".py"
        cond = m.group("cond")

        data = json.load(open(os.path.join(grade_dir, fname), "r", encoding="utf-8"))
        parsed = data.get("parsed")
        if not parsed or "verdict" not in parsed:
            continue
        verdict = str(parsed["verdict"]).strip().lower()
        groups[(sub, cond)].append(verdict)

    for cond in ["C1", "C3", "C4"]:
        agreements = []
        for (sub, c), verdicts in groups.items():
            if c != cond:
                continue
            if not verdicts:
                continue
            cnt = Counter(verdicts)
            majority = cnt.most_common(1)[0][1]
            agreements.append(majority / len(verdicts))
        avg_agree = sum(agreements) / len(agreements) if agreements else 0.0
        print(f"{cond} average majority agreement over runs: {avg_agree:.3f}")

if __name__ == "__main__":
    main()
