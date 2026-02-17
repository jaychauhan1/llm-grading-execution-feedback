import os
import importlib.util
from grader.sandbox import load_func, safe_call

def load_tests(problem_dir: str):
    tests_path = os.path.join(problem_dir, "tests.py")
    spec = importlib.util.spec_from_file_location("tests", tests_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.gen_tests()

def main():
    problem_dir = "problems/longest_consecutive"
    submission = os.path.join(problem_dir, "submissions", "s01_correct.py")

    testcases = load_tests(problem_dir)
    f = load_func(submission, "longestConsecutive")

    passed = 0
    failed = 0

    for inp, expected in testcases:
        res = safe_call(f, (inp,))
        if (not res["ok"]) or res["output"] != expected:
            failed += 1
        else:
            passed += 1

    print(f"submission={os.path.basename(submission)} passed={passed} failed={failed}")

if __name__ == "__main__":
    main()

