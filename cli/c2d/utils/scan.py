from pathlib import Path
import os
import pathspec
import subprocess


programming_extensions = [
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cs",
    ".cpp",
    ".c",
    ".go",
    ".rb",
    ".php",
    ".rs",
    ".kt",
    ".swift",
    ".scala",
    ".sh",
    ".pl",
    ".dart",
    ".html",
    ".css",
    ".json",
    ".xml",
    ".yml",
    ".yaml",
    ".sql",
    ".jsx",
    ".tsx",
]


def detect_repo():
    """
    This detects if there is a github repo present in the current path
    """
    git_dir = Path(".git")
    if not git_dir.exists():
        return False

    try:
        return True
    except subprocess.CalledProcessError:
        return False


def get_gitignore_contents(gitignore_path=Path(".gitignore")):
    """
    This extracts the contents of gitignore files in the current path
    """
    if not gitignore_path.exists():
        return []

    try:
        with gitignore_path.open("r") as file:
            contents = file.read().splitlines()
        return contents
    except Exception as e:
        print(f"Error reading .gitignore: {e}")
        return []


def scan_subfolders():
    """
    Scans all the contents in the subfolder(s)
    """
    path = os.curdir
    # path = "/Users/demonicaoi/Documents/GitHub/sensei-gigs/backend"
    path = "/Users/demonicaoi/Documents/Experiments/mern-app/"

    programming_extensions = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cs",
        ".cpp",
        ".c",
        ".go",
        ".rb",
        ".php",
        ".rs",
        ".kt",
        ".swift",
        ".scala",
        ".sh",
        ".pl",
        ".dart",
        ".html",
        ".css",
        ".json",
        ".xml",
        ".yml",
        ".yaml",
        ".sql",
        ".jsx",
        ".tsx",
    }
    res_files = []
    for root, _, files in os.walk(path, topdown=True):
        # Filter files to only include programming language files
        code_files = [
            f for f in files if os.path.splitext(f)[1] in programming_extensions
        ]

        for file in code_files:
            res_files.append(root + "/" + file)
    for file in res_files:
        print(file)
    return res_files


def read_contents(files_to_read):
    for file in files_to_read:
        print(f"\n--- {file} ---")
        try:
            with open(file, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print(f"Could not read {file}: {e}")


if __name__ == "__main__":
    resultant_files = scan_subfolders()
    read_contents(resultant_files)
