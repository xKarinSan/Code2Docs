from pathlib import Path
import pathspec

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
        "index.html", "index.css", "index.js", "index.ts","__init__.py",
        "tsconfig.node.json", "vite.config.ts", "vite-env.d.ts", "vercel.json",
        "typings.d.ts", "index.spec.ts", "swagger.json", ".github/workflows/node.js.yml"
    }
    
    ignored_paths = set(get_gitignored_contents(path)) if path else set()
    
    res_files = []

    for root, _, files in os.walk(path, topdown=True):
        
        # ensure to skip gitignore
        for file in files:
            full_path = Path(root) / file
            ext = os.path.splitext(file)[1]
            if str(full_path.resolve()) in ignored_paths:
                continue
            if ext in programming_extensions and file not in skip_filenames:
                res_files.append(os.path.join(root, file))

    for i in res_files:
        print("file: ",i)

    return res_files

def get_gitignored_contents(base_path="."):
    """
    Recursively collects ignored file/folder paths across all `.gitignore` files
    in the project directory, including contents of ignored folders.
    """
    base_path = Path(base_path).resolve()
    ignored = set()
    cumulative_spec = pathspec.PathSpec([])

    for root, dirs, files in os.walk(base_path, topdown=True):
        current_path = Path(root)
        gitignore_file = current_path / ".gitignore"

        # Parse .gitignore in current folder
        if gitignore_file.exists():
            try:
                lines = gitignore_file.read_text().splitlines()
                patterns = [line for line in lines if line.strip() and not line.strip().startswith("#")]
                spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
                cumulative_spec = cumulative_spec + spec
            except Exception as e:
                print(f"⚠️ Could not parse {gitignore_file}: {e}")

        # Skip ignored directories and collect full subtree
        for d in list(dirs):
            rel_path = (current_path / d).relative_to(base_path)
            abs_path = (current_path / d).resolve()
            if cumulative_spec.match_file(str(rel_path)):
                for sub_root, sub_dirs, sub_files in os.walk(abs_path):
                    for f in sub_files:
                        ignored.add(str(Path(sub_root) / f))
                    for sd in sub_dirs:
                        ignored.add(str(Path(sub_root) / sd))
                ignored.add(str(abs_path)) 
                dirs.remove(d)

        # Check ignored files
        for f in files:
            rel_path = (current_path / f).relative_to(base_path)
            abs_path = (current_path / f).resolve()
            if cumulative_spec.match_file(str(rel_path)):
                ignored.add(str(abs_path))

    return ignored




def read_contents(files_to_read):
    res = []
    for file in files_to_read:
        try:
            extension = os.path.splitext(file)[1].lstrip(".")
            with open(file, "r", encoding="utf-8") as f:
                print(file)
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
