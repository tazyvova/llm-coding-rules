#!/usr/bin/env python3
"""Print PR number, title, state, and URL. Defaults to current branch's PR."""
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
    ap.add_argument("number", nargs="?", default="")
    ap.add_argument("--repo", default="")
    args = ap.parse_args()

    repo_flag = ["--repo", args.repo] if args.repo else []
    num_flag = [str(args.number)] if args.number else []

    data = json.loads(run_gh(
        "pr", "view", *num_flag,
        *repo_flag,
        "--json", "number,title,state,url,baseRefName,headRefName",
    ))

    print(f"PR:     #{data['number']}")
    print(f"TITLE:  {data['title']}")
    print(f"STATE:  {data['state']}")
    print(f"URL:    {data['url']}")
    print(f"BASE:   {data['baseRefName']}")
    print(f"HEAD:   {data['headRefName']}")


if __name__ == "__main__":
    main()
