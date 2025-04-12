from pathlib import Path
import os

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
    current_path = Path.cwd()
    for path in [current_path] + list(current_path.parents):
        if (path / ".git").exists():
            return path
    return ""

def scan_subfolders(path):
    """
    Scans all subfolders for source code files and returns their paths,
    skipping dependency/config/lock files like package.json, yarn.lock, etc.
    """

    # Supported programming-related file extensions
    programming_extensions = {
        ".py", ".js", ".ts", ".java", ".cs", ".cpp", ".c", ".go", ".rb",
        ".php", ".rs", ".kt", ".swift", ".scala", ".sh", ".pl", ".dart",
        ".html", ".css", ".json", ".xml", ".yml", ".yaml", ".sql", ".jsx",
        ".tsx", ".vue", ".svelte"
    }

    # Filenames to skip (dependency/config/lock/build)
    skip_filenames = {
        "package.json", "package-lock.json", "yarn.lock", "requirements.txt",
        "Pipfile", "Pipfile.lock", "poetry.lock", "go.mod", "go.sum",
        "build.gradle", "settings.gradle", "pom.xml",
        ".env", "Makefile", "Dockerfile", "Cargo.toml", "Cargo.lock",
        "tsconfig.json", "vite.config.js", "babel.config.js",
        "next.config.js", "jest.config.js", "webpack.config.js","manifest.json",
        "index.html", "index.css", "index.js", "index.ts","__init__.py"
    }

    res_files = []

    for root, _, files in os.walk(path, topdown=True):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in programming_extensions and file not in skip_filenames:
                res_files.append(os.path.join(root, file))

    return res_files



def read_contents(files_to_read):
    res = []
    for file in files_to_read:
        try:
            extension = os.path.splitext(file)[1].lstrip(".")
            with open(file, "r", encoding="utf-8") as f:
                res.append({
                    "filePath": file,
                    "extension": extension,
                    "contents":f.read()
                })
        except Exception as e:
            print(f"Could not read {file}: {e}")
            return []
    return res

if __name__ == "__main__":
    resultant_files = scan_subfolders()
    read_files = read_contents(resultant_files)
    for file in read_files:
        print(file)
