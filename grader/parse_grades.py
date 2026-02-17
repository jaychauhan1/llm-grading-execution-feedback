import os, json, re

PROBLEM_ID = "longest_consecutive"

def extract_json(s: str):
    # grab the first {...} block (best-effort)
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None

def main():
    in_dir = os.path.join("results", "grades", PROBLEM_ID)
    out_path = os.path.join("results", "tables", f"{PROBLEM_ID}_grades_run1.json")

    rows = []
    for fname in sorted(os.listdir(in_dir)):
        if not fname.endswith("_run1.json"):
            continue
        raw = json.load(open(os.path.join(in_dir, fname), "r"))["raw_output"]
        parsed = extract_json(raw)

        rows.append({
            "file": fname,
            "parsed_ok": parsed is not None,
            "parsed": parsed
        })

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(rows, open(out_path, "w"), indent=2)
    ok = sum(1 for r in rows if r["parsed_ok"])
    print(f"Parsed {ok}/{len(rows)} successfully")
    print("Wrote", out_path)

if __name__ == "__main__":
    main()
