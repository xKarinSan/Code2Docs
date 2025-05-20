import time
__t0 = time.perf_counter()

import asyncio
import os
import sys

from dotenv import load_dotenv
from pathlib import Path

from .utils.file_processes import create_archi_diagram,create_readme_file
from .utils.rag import read_all_file_contents
from .utils.scan import detect_repo, read_contents, scan_subfolders
from .utils.tasks import run_all
import typer
from rich.console import Console
from rich.panel import Panel



app = typer.Typer()
console = Console()

VECTOR_DB_DIR = Path.home() / "code2docs" / "vector_db"
ENV_DIR = Path.home() / "code2docs"
ENV_FILE = ENV_DIR / ".env"



def is_valid_openai_key(api_key: str) -> bool:
    from openai import OpenAI
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        return True
    except Exception as e:
        console.print(f"⚠️ [yellow]Unexpected error while validating API key: {e}[/yellow]")
        return False
    
def get_key(key="OPEN_AI_API_KEY"):
    """
    Get the API key from the environment variable.

    Parameters:
        key (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.
    """
    load_dotenv(dotenv_path=ENV_FILE)
    return os.getenv(key)

def under_construction():
    console.print("🚧 [bold yellow]This feature is under construction.[/bold yellow] Stay tuned! 🛠️")

def scanning_in_progress():
    console.print("🔍 [bold cyan]Scanning your codebase...[/bold cyan] Please wait ⏳")

def generating_in_progress():
    """
    Display a message indicating that the documentation generation is in progress.
    """
    console.print("🛠️  [bold green]Generating documentation...[/bold green] Almost there 🚀")

@app.command("code-doc")
def create_inline_doc():
    """
    Generate inline documentation (docstrings and comments) for the codebase. (Beta)
    """
    from langchain_openai import ChatOpenAI
    
    OPEN_AI_API_KEY = get_key()
    if not OPEN_AI_API_KEY:
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if not is_valid_openai_key(OPEN_AI_API_KEY):
        console.print("❌ [bold red]Invalid OpenAI API key![/bold red]")
        return
    repo_start = detect_repo()
    if not repo_start:
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    
    scanning_in_progress()
    resultant_files = scan_subfolders(repo_start)
    read_files = read_contents(resultant_files)
    generating_in_progress()

    model = ChatOpenAI(openai_api_key = OPEN_AI_API_KEY)
    asyncio.run(run_all(read_files,model))
    console.print("✅ [bold green]Code documentation successfully created![/bold green] 🚀")

@app.command("api-doc")
def create_api_doc():
    """
    Generate documentation for API endpoints. (Coming soon)
    """
    OPEN_AI_API_KEY = get_key()
    if not OPEN_AI_API_KEY:
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if not is_valid_openai_key(OPEN_AI_API_KEY):
        console.print("❌ [bold red]Invalid OpenAI API key![/bold red]")
        return
    if not detect_repo():
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]API documentation successfully created![/bold green] 🚀")
    
@app.command("db-doc")
def create_db_doc():
    """
    Generate documentation for the database schema. (Coming soon)
    """
    OPEN_AI_API_KEY = get_key()
    if not OPEN_AI_API_KEY:
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if not is_valid_openai_key(OPEN_AI_API_KEY):
        console.print("❌ [bold red]Invalid OpenAI API key![/bold red]")
        return
    if not detect_repo():
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]Database schema documentation successfully created![/bold green] 🚀")
    
@app.command("readme-doc")
def create_readme_doc():
    """
    Generate a comprehensive README.md for the project. (Beta)
    """
    from langchain_openai import ChatOpenAI
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    
    OPEN_AI_API_KEY = get_key()
    if not OPEN_AI_API_KEY:
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if not is_valid_openai_key(OPEN_AI_API_KEY):
        console.print("❌ [bold red]Invalid OpenAI API key![/bold red]")
        return
    repo_start = detect_repo()
    if not repo_start:
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return
    
    embeddings = OpenAIEmbeddings(api_key=OPEN_AI_API_KEY, model="text-embedding-3-large")
    vector_store = Chroma(
        collection_name="c2d",
        embedding_function=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
    )
    vector_store.reset_collection()
    
    scanning_in_progress()
    resultant_files = scan_subfolders(repo_start)
    read_files = read_contents(resultant_files)
    generating_in_progress()
    
    model = ChatOpenAI(openai_api_key = OPEN_AI_API_KEY)
    documents, _ = read_all_file_contents(read_files)
    vector_store.add_documents(documents)
    
    create_readme_file(vector_store,model,str(repo_start))
    console.print("✅ [bold green]Project README documentation successfully created![/bold green] 🚀")

@app.command("archi-doc")
def create_archi_doc():
    """
    Generate architecture diagrams for the codebase. (Beta)
    """
    from langchain_openai import ChatOpenAI
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    
    OPEN_AI_API_KEY = get_key()
    if not OPEN_AI_API_KEY:
        console.print("🔑 [bold red]Please set your OpenAI API key first![/bold red]")
        return
    if not is_valid_openai_key(OPEN_AI_API_KEY):
        console.print("❌ [bold red]Invalid OpenAI API key![/bold red]")
        return
    repo_start = detect_repo()
    if not repo_start:
        console.print("📁 [bold red]Not inside a Git repository![/bold red]")
        return

    embeddings = OpenAIEmbeddings(api_key=OPEN_AI_API_KEY, model="text-embedding-3-large")
    vector_store = Chroma(
        collection_name="c2d",
        embedding_function=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
    )
    vector_store.reset_collection()

    scanning_in_progress()
    resultant_files = scan_subfolders(repo_start)
    read_files = read_contents(resultant_files)
    generating_in_progress()
    
    model = ChatOpenAI(openai_api_key = OPEN_AI_API_KEY)
    documents, _ = read_all_file_contents(read_files)
    vector_store.add_documents(documents)
          
    create_archi_diagram(vector_store, model, str(repo_start))
    console.print("✅ [bold green]Project architecture documentation successfully created![/bold green] 🚀")

@app.command("save-key")
def save_key(api_key):
    """
    Save the OpenAI API key securely to the local environment file.

    Parameters:
        api_key (str): The OpenAI API key to be saved.
    """
    with open(ENV_FILE, "w") as f:
        f.write(f"OPEN_AI_API_KEY={api_key}\n")
    console.print("🔑 [bold green]API key saved successfully![/bold green] 🚀")

@app.command("load-key")
def load_key():
    """
    Load and display the saved OpenAI API key from the environment file.
    """
    API_KEY = get_key()
    console.print("OPEN AI API key:", API_KEY)

def main():
    if not os.path.exists(ENV_DIR):
        os.makedirs(ENV_DIR)

    if len(sys.argv) == 1:
        console.print(
            Panel.fit(
                "[bold cyan]✨ Welcome to Code2Docs CLI ✨[/bold cyan]\n\n"
                "[white]Your AI-powered documentation assistant 🧠📄[/white]\n\n"
                "[green]Usage:[/green] Run [bold]c2d[command][/bold] to get started\n"
                "[green]Help:[/green] Add [bold]--help[/bold] to view options\n\n"
                "[dim]Happy documenting! 🚀[/dim]",
                title="📘 Code2Docs",
                border_style="bright_blue",
            )
        )
        print(f"⏱️ Total startup time (from import): {time.perf_counter() - __t0}s")
        return
    cli = typer.main.get_command(app)
    cli()

if __name__ == "__main__":
    main()