#!/usr/bin/env python3
"""Print an issue's title, body, and comments in plain text — no JSON parsing needed."""
import argparse, json, subprocess, sys


def run_gh(*args):
    try:
        r = subprocess.run(["gh", *args], capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("error: gh not found on PATH")
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    return r.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("number", type=int)
    ap.add_argument("--repo", default="")
    args = ap.parse_args()

    repo_flag = ["--repo", args.repo] if args.repo else []

    data = json.loads(run_gh(
        "issue", "view", str(args.number),
        *repo_flag,
        "--json", "title,state,labels,milestone,body,comments",
    ))

    labels = ", ".join(l["name"] for l in data.get("labels") or [])
    milestone = (data.get("milestone") or {}).get("title", "")

    print(f"TITLE: {data['title']}")
    print(f"STATE: {data['state']}")
    print(f"LABELS: {labels}")
    print(f"MILESTONE: {milestone}")
    print()
    print("BODY:")
    print(data.get("body", "").strip())

    for i, c in enumerate(data.get("comments") or [], 1):
        author = c.get("author", {}).get("login", "?")
        created = c.get("createdAt", "")[:10]
        print(f"\n--- COMMENT {i} ({author}, {created}) ---")
        print(c.get("body", "").strip())


if __name__ == "__main__":
    main()
