#!/usr/bin/env python3
"""Zero-dependency GitHub pusher for /home/achinagrawal/wcb-manitoba (works without local `git` installed).

Usage:
  # Interactive prompt for repo & GitHub Personal Access Token (PAT):
  python3 push_to_github.py

  # Or pass arguments directly:
  GITHUB_TOKEN=ghp_xxx python3 push_to_github.py --repo <owner>/<repo> --create-private

  # Preview which files will be uploaded without making network calls:
  python3 push_to_github.py --dry-run
"""

import argparse
import base64
import fnmatch
import getpass
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

EXCLUDED_DIRS = {".git", ".venv", "venv", "ENV", "__pycache__"}
EXCLUDED_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.so",
    ".env",
    ".env.*",
    "secrets.toml",
    "*.json.key",
    "service-account*.json",
    "*.zip",
    ".DS_Store",
    "Thumbs.db",
]


def should_include(rel_path: Path, include_videos: bool = True) -> bool:
    for part in rel_path.parts[:-1]:
        if part in EXCLUDED_DIRS:
            return False
    name = rel_path.name
    for pat in EXCLUDED_PATTERNS:
        if fnmatch.fnmatch(name, pat):
            return False
    if not include_videos and name.lower().endswith(".mp4"):
        return False
    return True


def collect_files(root: Path, include_videos: bool = True) -> list[Path]:
    files = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root)
            if should_include(rel, include_videos=include_videos):
                files.append(rel)
    return files


def gh_request(method: str, path: str, token: str, payload: dict | None = None) -> tuple[int, dict]:
    url = f"https://api.github.com{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "wcb-claims-assistant-github-uploader",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
        except Exception:
            err_json = {"message": err_body}
        return e.code, err_json


def normalize_repo(repo_arg: str) -> str:
    s = repo_arg.strip()
    for prefix in ("https://github.com/", "http://github.com/", "git@github.com:"):
        if s.startswith(prefix):
            s = s[len(prefix):]
    if s.endswith(".git"):
        s = s[:-4]
    s = s.strip("/")
    if "/" not in s or len(s.split("/")) != 2:
        raise ValueError(f"Expected '<owner>/<repo>' or GitHub URL, got: {repo_arg}")
    return s


def main():
    parser = argparse.ArgumentParser(description="Push AI Claims Assistant directly to GitHub via REST API.")
    parser.add_argument("--repo", help="Target GitHub repo as 'owner/repo' or 'https://github.com/owner/repo'")
    parser.add_argument("--branch", default="main", help="Target branch name (default: main)")
    parser.add_argument("--subdir", default="", help="Optional subfolder inside the target repo (e.g. 'wcb-manitoba')")
    parser.add_argument("--create-private", action="store_true", help="Create a private repo if it does not exist yet")
    parser.add_argument("--create-public", action="store_true", help="Create a public repo if it does not exist yet")
    parser.add_argument("--skip-videos", action="store_true", help="Exclude .mp4 demo recordings for a smaller upload")
    parser.add_argument("--message", default="Initial commit: Google Cloud AI Claims Assistant", help="Commit message")
    parser.add_argument("--dry-run", action="store_true", help="List files and sizes that would be pushed and exit")
    args = parser.parse_args()

    rel_files = collect_files(ROOT_DIR, include_videos=not args.skip_videos)
    total_bytes = sum((ROOT_DIR / f).stat().st_size for f in rel_files)

    if args.dry_run:
        print(f"Dry run — {len(rel_files)} files ({total_bytes / (1024 * 1024):.2f} MB) ready to push:")
        for f in rel_files:
            sz_kb = (ROOT_DIR / f).stat().st_size / 1024
            print(f"  {str(f):68s} {sz_kb:8.1f} KB")
        return

    repo_input = args.repo or input("Enter target GitHub repository (e.g. username/wcb-claims-assistant): ").strip()
    owner_repo = normalize_repo(repo_input)
    owner, repo_name = owner_repo.split("/")

    token = os.environ.get("GITHUB_TOKEN") or getpass.getpass("Enter GitHub Personal Access Token (PAT): ").strip()
    if not token:
        sys.exit("Error: GitHub Personal Access Token is required.")

    # 1. Check if repository exists (or create it)
    status, repo_info = gh_request("GET", f"/repos/{owner_repo}", token)
    if status == 404:
        if args.create_private or args.create_public:
            is_private = not args.create_public
        else:
            ans = input(f"Repository '{owner_repo}' not found. Create it now as a Private repo? [Y/n]: ").strip().lower()
            if ans in ("n", "no"):
                sys.exit("Aborted.")
            is_private = True
        print(f"Creating {'private' if is_private else 'public'} repository '{repo_name}'...")
        c_status, repo_info = gh_request(
            "POST",
            "/user/repos",
            token,
            {
                "name": repo_name,
                "description": "AI-Powered Claims Intake & Adjudication Assistant on Google Cloud Run & Vertex AI Gemini",
                "private": is_private,
                "auto_init": True,
            },
        )
        if c_status not in (200, 201):
            sys.exit(f"Failed to create repository ({c_status}): {repo_info}")
        owner_repo = repo_info["full_name"]
    elif status != 200:
        sys.exit(f"GitHub API error ({status}): {repo_info}")

    branch = args.branch
    ref_status, ref_info = gh_request("GET", f"/repos/{owner_repo}/git/ref/heads/{branch}", token)

    # Bootstrap completely empty repo so Git Blobs API is enabled
    if ref_status in (404, 409):
        print(f"Initializing branch '{branch}' on empty repository...")
        readme_b64 = base64.b64encode((ROOT_DIR / "README.md").read_bytes()).decode("ascii")
        init_path = f"{args.subdir.strip('/')}/README.md" if args.subdir.strip("/") else "README.md"
        b_status, b_info = gh_request(
            "PUT",
            f"/repos/{owner_repo}/contents/{init_path}",
            token,
            {"message": "Initialize repository", "content": readme_b64, "branch": branch},
        )
        if b_status not in (200, 201):
            sys.exit(f"Failed to bootstrap empty repository ({b_status}): {b_info}")
        ref_status, ref_info = gh_request("GET", f"/repos/{owner_repo}/git/ref/heads/{branch}", token)

    if ref_status != 200:
        sys.exit(f"Could not resolve branch '{branch}' ({ref_status}): {ref_info}")

    head_sha = ref_info["object"]["sha"]
    _, commit_info = gh_request("GET", f"/repos/{owner_repo}/git/commits/{head_sha}", token)
    base_tree_sha = commit_info["tree"]["sha"]

    # 2. Upload blobs
    prefix = f"{args.subdir.strip('/')}/" if args.subdir.strip("/") else ""
    tree_entries = []
    print(f"Uploading {len(rel_files)} files ({total_bytes / (1024 * 1024):.2f} MB) to {owner_repo} ({branch})...")
    for idx, rel in enumerate(rel_files, start=1):
        raw = (ROOT_DIR / rel).read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        b_status, blob = gh_request("POST", f"/repos/{owner_repo}/git/blobs", token, {"content": b64, "encoding": "base64"})
        if b_status not in (200, 201):
            sys.exit(f"Failed uploading {rel} ({b_status}): {blob}")
        mode = "100755" if rel.name.endswith(".py") and os.access(ROOT_DIR / rel, os.X_OK) else "100644"
        tree_entries.append({"path": f"{prefix}{rel.as_posix()}", "mode": mode, "type": "blob", "sha": blob["sha"]})
        print(f"  [{idx}/{len(rel_files)}] {prefix}{rel.as_posix()}")

    # 3. Create tree, commit & update branch ref
    t_status, new_tree = gh_request(
        "POST",
        f"/repos/{owner_repo}/git/trees",
        token,
        {"base_tree": base_tree_sha, "tree": tree_entries},
    )
    if t_status not in (200, 201):
        sys.exit(f"Failed creating Git tree ({t_status}): {new_tree}")

    cm_status, new_commit = gh_request(
        "POST",
        f"/repos/{owner_repo}/git/commits",
        token,
        {"message": args.message, "tree": new_tree["sha"], "parents": [head_sha]},
    )
    if cm_status not in (200, 201):
        sys.exit(f"Failed creating commit ({cm_status}): {new_commit}")

    u_status, _ = gh_request(
        "PATCH",
        f"/repos/{owner_repo}/git/refs/heads/{branch}",
        token,
        {"sha": new_commit["sha"], "force": False},
    )
    if u_status != 200:
        sys.exit(f"Failed updating branch '{branch}' ({u_status})")

    print(f"\nSuccess! Pushed commit {new_commit['sha'][:7]} to https://github.com/{owner_repo}/tree/{branch}")


if __name__ == "__main__":
    main()
