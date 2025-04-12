import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI 
from pathlib import Path
from .utils.scan import detect_repo, read_contents, scan_subfolders
from .utils.tasks import run_all
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

ENV_DIR = Path.home() / "code2docs"
ENV_FILE = ENV_DIR / ".env"

def get_key(key="OPEN_AI_API_KEY"):
    """
    This function gets the API key from the environment variable
    """
    load_dotenv(dotenv_path=ENV_FILE)
    return os.getenv(key)

def under_construction():
    console.print("🚧 [bold yellow]This feature is under construction.[/bold yellow] Stay tuned! 🛠️")

def scanning_in_progress():
    console.print("🔍 [bold cyan]Scanning your codebase...[/bold cyan] Please wait ⏳")

def generating_in_progress():
    console.print("🛠️  [bold green]Generating documentation...[/bold green] Almost there 🚀")

@app.command("code-doc")
def create_inline_doc():
    """
    This is for users to create in-line documentations
    """
    OPEN_AI_API_KEY = get_key()
    if(OPEN_AI_API_KEY is None):
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if(not detect_repo()):
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    
    scanning_in_progress()
    resultant_files = scan_subfolders()
    read_files = read_contents(resultant_files)
    generating_in_progress()

    model = ChatOpenAI(openai_api_key = OPEN_AI_API_KEY)
    asyncio.run(run_all(read_files,model))
    console.print("✅ [bold green]Code documentation successfully created![/bold green] 🚀")

@app.command("api-doc")
def create_api_doc():
    """
    This is for users to create API endpoint documentations
    """
    if(get_key() is None):
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if(not detect_repo()):
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]API documentation successfully created![/bold green] 🚀")
    
@app.command("db-doc")
def create_db_doc():
    """
    This is for users to create database schema documentation
    """
    if(get_key() is None):
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if(not detect_repo()):
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]Database schema documentation successfully created![/bold green] 🚀")
    
@app.command("readme-doc")
def create_readme_doc():
    """
    This is for users to create README documentations
    """
    if(get_key() is None):
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if(not detect_repo()):
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]Project README documentation successfully created![/bold green] 🚀")

@app.command("archi-doc")
def create_archi_doc():
    """
    This is for users to create project architecture diagrams
    """
    if(get_key() is None):
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if(not detect_repo()):
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]Project architecture documentation successfully created![/bold green] 🚀")

@app.command("save-key")
def save_key(api_key):
    """
    This is for users to save their API keys
    """
    with open(ENV_FILE, "w") as f:
        f.write(f"OPEN_AI_API_KEY={api_key}\n")
    console.print("🔑 [bold green]API key saved successfully![/bold green] 🚀")

@app.command("load-key")
def load_key():
    """
    This is for users to load their API keys
    """
    API_KEY = get_key()
    console.print("OPEN AI API key:",API_KEY)
    # Here you would load the API key from a secure location
    # For example, you could load it from a .env file or a secure vault


def main():
    if not os.path.exists(ENV_DIR):
        os.makedirs(ENV_DIR)

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
    app()

    
if __name__ == "__main__":
    main()
