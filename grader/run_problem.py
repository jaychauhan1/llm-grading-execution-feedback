import os
import json
import time
import importlib.util
from grader.sandbox import load_func, safe_call


def load_tests(problem_dir: str):
    tests_path = os.path.join(problem_dir, "tests.py")
    spec = importlib.util.spec_from_file_location("tests_mod", tests_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.gen_tests()


def load_labels(problem_dir: str):
    labels_path = os.path.join(problem_dir, "submissions", "labels.json")
    with open(labels_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_submission(problem_id: str, submission_file: str, testcases):
    func = load_func(submission_file, "longestConsecutive")

    passed = 0
    failed = 0
    failures = []

    t0 = time.time()
    for idx, (inp, expected) in enumerate(testcases):
        res = safe_call(func, (inp,))
        if (not res["ok"]) or res["output"] != expected:
            failed += 1
            failures.append({
                "test_id": idx,
                "input": inp,
                "expected": expected,
                "got": res["output"],
                "error": res["error"],
            })
        else:
            passed += 1
    dt_ms = int((time.time() - t0) * 1000)

    return {
        "problem_id": problem_id,
        "submission_file": os.path.basename(submission_file),
        "passed": passed,
        "failed": failed,
        "runtime_ms": dt_ms,
        "failures": failures[:5],  # keep small for now
    }


def main():
    problem_id = "longest_consecutive"
    problem_dir = os.path.join("problems", problem_id)

    labels = load_labels(problem_dir)
    testcases = load_tests(problem_dir)

    out_dir = os.path.join("results", "raw", problem_id)
    os.makedirs(out_dir, exist_ok=True)

    for sub_file in sorted(labels.keys()):
        sub_path = os.path.join(problem_dir, "submissions", sub_file)
        evidence = run_submission(problem_id, sub_path, testcases)
        evidence["ground_truth_label"] = labels[sub_file]

        out_path = os.path.join(out_dir, sub_file.replace(".py", ".json"))
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

        print(f"Wrote {out_path} (passed={evidence['passed']} failed={evidence['failed']})")


if __name__ == "__main__":
    main()

