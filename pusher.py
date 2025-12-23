#!/usr/bin/env python3
"""
Auto-commit script for GitHub Pages leaderboard updates.
Run: python auto_commit.py
"""

import subprocess
import time
import os
import sys
from datetime import datetime

def run_git(cmd, check=True):
    """Run git command and handle errors."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        print(f"✓ {cmd}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {cmd}: {e.stderr}")
        return None

def has_changes():
    """Check if repo has uncommitted changes."""
    status = run_git("git status --porcelain")
    return status and len(status.strip()) > 0

def commit_and_push(commit_msg):
    """Commit changes if any exist."""
    if not has_changes():
        print("No changes to commit.")
        return False
    
    run_git("git add .")
    run_git(f'git commit -m "{commit_msg}"')
    run_git("git push origin main")
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        commit_and_push("Update leaderboard data")
        return
    
    print("Auto-commit watcher started (Ctrl+C to stop)")
    print("Updates data.csv every 5 minutes...")
    
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"Update leaderboard [{timestamp}]"
            
            if commit_and_push(commit_msg):
                print("✅ Pushed to GitHub Pages")
            
            time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            print("\n👋 Stopped.")
            break

if __name__ == "__main__":
    main()
