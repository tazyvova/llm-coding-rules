#!/usr/bin/env python3
"""Print a compact table of issues: #N  [labels]  title."""
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
    ap.add_argument("--repo", default="")
    ap.add_argument("--milestone", default="")
    ap.add_argument("--label", default="")
    ap.add_argument("--state", default="open", choices=["open", "closed", "all"])
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    repo_flag = ["--repo", args.repo] if args.repo else []
    milestone_flag = ["--milestone", args.milestone] if args.milestone else []
    label_flag = ["--label", args.label] if args.label else []

    data = json.loads(run_gh(
        "issue", "list",
        "--state", args.state,
        "--limit", str(args.limit),
        *repo_flag, *milestone_flag, *label_flag,
        "--json", "number,title,labels,milestone,state",
    ))

    for issue in data:
        num = issue["number"]
        title = issue["title"]
        labels = " ".join(f"[{l['name']}]" for l in issue.get("labels") or [])
        ms = (issue.get("milestone") or {}).get("title", "")
        ms_str = f"  ({ms})" if ms else ""
        label_str = f"  {labels}" if labels else ""
        print(f"#{num:<5} {title}{label_str}{ms_str}")


if __name__ == "__main__":
    main()
