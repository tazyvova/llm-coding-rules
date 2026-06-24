#!/usr/bin/env python3
"""Create a GitHub issue. Body read from --body-file or stdin. Prints the new issue URL."""
import argparse, subprocess, sys


def run_gh(*args):
    try:
        r = subprocess.run(["gh", *args], capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("error: gh not found on PATH")
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--title", required=True)
    ap.add_argument("--repo", default="")
    ap.add_argument("--milestone", default="")
    ap.add_argument("--label", action="append", default=[])
    ap.add_argument("--body-file", default="")
    args = ap.parse_args()

    body = ""
    if args.body_file:
        with open(args.body_file) as f:
            body = f.read()
    else:
        body = sys.stdin.read()

    repo_flag = ["--repo", args.repo] if args.repo else []
    milestone_flag = ["--milestone", args.milestone] if args.milestone else []
    label_flags = []
    for lbl in args.label:
        label_flags += ["--label", lbl]

    url = run_gh(
        "issue", "create",
        "--title", args.title,
        "--body", body,
        *repo_flag, *milestone_flag, *label_flags,
    )
    print(url)


if __name__ == "__main__":
    main()
