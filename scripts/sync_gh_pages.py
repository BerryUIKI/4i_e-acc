#!/usr/bin/env python3
"""
Sync script: syncs index.html, .nojekyll, tools/, and assets/ to origin/gh-pages.
Can be run manually by agents or developers to publish updates to GitHub Pages.
"""

import os
import shutil
import subprocess
import tempfile

def run_cmd(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"Command failed with code {res.returncode}:\n{res.stderr}")
        raise RuntimeError(res.stderr)
    return res.stdout.strip()

def sync_to_gh_pages():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"Repo root: {repo_root}")

    # Fetch latest gh-pages
    run_cmd(["git", "fetch", "origin", "gh-pages"], cwd=repo_root)

    with tempfile.TemporaryDirectory() as tmpdir:
        worktree_dir = os.path.join(tmpdir, "gh-pages-wt")
        print(f"Creating git worktree in {worktree_dir}...")
        run_cmd(["git", "worktree", "add", worktree_dir, "origin/gh-pages"], cwd=repo_root)

        try:
            # Copy files: index.html, .nojekyll, tools/, assets/
            shutil.copy2(os.path.join(repo_root, "index.html"), os.path.join(worktree_dir, "index.html"))
            shutil.copy2(os.path.join(repo_root, ".nojekyll"), os.path.join(worktree_dir, ".nojekyll"))

            # Sync tools/
            dst_tools = os.path.join(worktree_dir, "tools")
            if os.path.exists(dst_tools):
                shutil.rmtree(dst_tools)
            shutil.copytree(os.path.join(repo_root, "tools"), dst_tools)

            # Sync assets/
            dst_assets = os.path.join(worktree_dir, "assets")
            if os.path.exists(dst_assets):
                shutil.rmtree(dst_assets)
            shutil.copytree(os.path.join(repo_root, "assets"), dst_assets)

            # Git add and commit in worktree
            run_cmd(["git", "add", "-A"], cwd=worktree_dir)
            status = run_cmd(["git", "status", "--porcelain"], cwd=worktree_dir)
            if not status:
                print("No changes to sync to gh-pages; working tree clean.")
            else:
                print(f"Changes detected:\n{status}")
                commit_msg = "[f78f1d3e] chore: sync web site, tools, and assets to gh-pages"
                run_cmd(["git", "-c", "commit.gpgsign=false", "commit", "-m", commit_msg], cwd=worktree_dir)
                print("Pushing to origin/gh-pages...")
                run_cmd(["git", "push", "origin", "HEAD:gh-pages"], cwd=worktree_dir)
                print("Successfully synced and pushed to gh-pages!")
        finally:
            print("Cleaning up git worktree...")
            run_cmd(["git", "worktree", "remove", "--force", worktree_dir], cwd=repo_root)

if __name__ == "__main__":
    sync_to_gh_pages()
