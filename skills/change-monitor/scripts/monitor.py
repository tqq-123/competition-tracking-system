import argparse
import json
import os
import requests
from datetime import datetime

API_URL = "https://www.lanqiao.cn/api/v2/problems/"

def fetch_current(search, page=1, page_size=30):
    params = {"page": page, "page_size": page_size, "search": search}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(API_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()

def load_snapshot(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare(old_data, new_data):
    old_problems = {p["id"]: p for p in old_data.get("data", {}).get("results", [])}
    new_problems = {p["id"]: p for p in new_data.get("results", [])}

    added = []
    removed = []
    changed = []

    for pid, new_p in new_problems.items():
        if pid not in old_problems:
            added.append({"id": pid, "name": new_p.get("name")})
        else:
            old_p = old_problems[pid]
            if old_p.get("pass_rate") != new_p.get("pass_rate"):
                changed.append({
                    "id": pid,
                    "name": new_p.get("name"),
                    "old_pass_rate": old_p.get("pass_rate"),
                    "new_pass_rate": new_p.get("pass_rate")
                })

    for pid, old_p in old_problems.items():
        if pid not in new_problems:
            removed.append({"id": pid, "name": old_p.get("name")})

    return {"added": added, "removed": removed, "changed": changed}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--search", required=True)
    args = parser.parse_args()

    old_data = load_snapshot(args.snapshot)
    new_data = fetch_current(args.search)
    diff = compare(old_data, new_data)

    result = {
        "status": "success",
        "search": args.search,
        "check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "added_count": len(diff["added"]),
            "removed_count": len(diff["removed"]),
            "changed_count": len(diff["changed"])
        },
        "details": diff
    }

    output_file = f"change_report_{args.search}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n[已保存到 {output_file}]")

if __name__ == "__main__":
    main()