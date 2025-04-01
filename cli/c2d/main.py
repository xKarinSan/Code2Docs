from pathlib import Path
import sys
import os
from dotenv import load_dotenv
from c2d.utils.scan import detect_repo, get_gitignore_contents, scan_subfolders
import typer
from rich import print
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()


@app.command("upload-key")
def upload_key(key: str):
    """
    \b
    To upload an API key.
    \nParameters:
      - key (string): the value of the API key
    \nExample:
      c2d upload-key test_key
    """
    if not key:
        print("Key not found")
    else:
        env_path = Path(".env")
        env_path.parent.mkdir(parents=True, exist_ok=True)
        with env_path.open("w") as f:
            f.write(f"api_key={key}")
        print("key saved")


@app.command("show-key")
def show_key(masked: bool = True):
    """
    To show if the key is present or not. NOTE: This should at least be masked during production.
    """
    curr_key = os.environ.get("api_key", None)
    if not curr_key:
        print("Key not found")
    else:
        if masked:
            masked = curr_key[:2] + "*" * (len(curr_key) - 4) + curr_key[-2:]
            print(f"Masked key is: {masked}")
        else:
            print(f"Unmasked key is:{curr_key}")


@app.command("scan")
def scan_directory():
    """
    \b
    This scans the current directory which the c2d cli is used at.

    """
    print("Scanning ...")
    path = os.curdir

    scan_subfolders()
    return


@app.command("repo-scan")
def scan_for_repo():
    """
    \b
    This scans for an existing github repository in the current path.

    \nReturns:
      - repository name if a repository is found
      - "Not found" if there is no repository found.
    """
    repo_found = detect_repo()
    if not repo_found:
        print("Not found!")
        return
    gitignore_contents = get_gitignore_contents()
    print(gitignore_contents)
    # print("Repo found!")


def main():
    if len(sys.argv) == 1:
        console.print(
            Panel.fit(
                "[bold cyan]Welcome to Code2Docs CLI 🚀[/bold cyan]\n\n"
                "Use [green]--help[/green] after any command to see usage.",
                title="📘 Code2Docs",
                border_style="bright_blue",
            )
        )
        return
    load_dotenv()
    app()


if __name__ == "__main__":
    main()
