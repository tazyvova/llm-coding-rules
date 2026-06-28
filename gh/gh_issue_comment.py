#!/usr/bin/env python3
"""Post a comment on an issue from a file or stdin."""
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
    ap.add_argument("number", type=int)
    ap.add_argument("--repo", default="")
    ap.add_argument("--body-file", default="")
    args = ap.parse_args()

    if args.body_file:
        with open(args.body_file) as f:
            body = f.read()
    else:
        body = sys.stdin.read()

    if not body.strip():
        sys.exit("error: comment body is empty")

    repo_flag = ["--repo", args.repo] if args.repo else []

    url = run_gh(
        "issue", "comment", str(args.number),
        "--body", body,
        *repo_flag,
    )
    print(url)


if __name__ == "__main__":
    main()
