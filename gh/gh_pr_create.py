#!/usr/bin/env python3
"""Create a PR with body from file or stdin. Prints the new PR URL."""
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
    ap.add_argument("--base", default="")
    ap.add_argument("--body-file", default="")
    args = ap.parse_args()

    if args.body_file:
        with open(args.body_file) as f:
            body = f.read()
    else:
        body = sys.stdin.read()

    repo_flag = ["--repo", args.repo] if args.repo else []
    base_flag = ["--base", args.base] if args.base else []

    url = run_gh(
        "pr", "create",
        "--title", args.title,
        "--body", body,
        *repo_flag, *base_flag,
    )
    print(url)


if __name__ == "__main__":
    main()
