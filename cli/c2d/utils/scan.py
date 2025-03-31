from pathlib import Path
import subprocess

def scan_repo():
    git_dir = Path(".git")
    if not git_dir.exists():
        return False

    try:
        return True
    except subprocess.CalledProcessError:
        False
