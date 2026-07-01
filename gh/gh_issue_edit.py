#!/usr/bin/env python3
"""Update an issue body from a file — avoids glob/newline permission prompts."""
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
    ap.add_argument("--title", default="")
    ap.add_argument("--add-label", action="append", default=[])
    ap.add_argument("--remove-label", action="append", default=[])
    args = ap.parse_args()

    repo_flag = ["--repo", args.repo] if args.repo else []

    extra = []
    if args.body_file:
        with open(args.body_file) as f:
            body = f.read()
        extra += ["--body", body]
    elif not sys.stdin.isatty():
        # A non-interactive caller (e.g. an agent's shell tool) also reports
        # isatty() == False even when nothing was piped in, so sys.stdin.read()
        # silently returns "" and would wipe the issue body. Only pass --body
        # when a piped body was actually provided.
        stdin_body = sys.stdin.read()
        if stdin_body:
            extra += ["--body", stdin_body]

    if args.title:
        extra += ["--title", args.title]
    for lbl in args.add_label:
        extra += ["--add-label", lbl]
    for lbl in args.remove_label:
        extra += ["--remove-label", lbl]

    run_gh("issue", "edit", str(args.number), *repo_flag, *extra)
    print(f"Issue #{args.number} updated.")


if __name__ == "__main__":
    main()
