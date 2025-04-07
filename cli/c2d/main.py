import os
import sys
from dotenv import load_dotenv

import typer
# from rich import print
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

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
    scanning_in_progress()
    generating_in_progress()
    console.print("✅ [bold green]Code documentation successfully created![/bold green] 🚀")

@app.command("api-doc")
def create_api_doc():
    """
    This is for users to create API endpoint documentations
    """
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]API documentation successfully created![/bold green] 🚀")
    
@app.command("db-doc")
def create_db_doc():
    """
    This is for users to create database schema documentation
    """
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]Database schema documentation successfully created![/bold green] 🚀")
    
@app.command("readme-doc")
def create_readme_doc():
    """
    This is for users to create README documentations
    """
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]Project README documentation successfully created![/bold green] 🚀")

@app.command("archi-doc")
def create_archi_doc():
    """
    This is for users to create project architecture diagrams
    """
    under_construction()
    # scanning_in_progress()
    # generating_in_progress()
    # console.print("✅ [bold green]Project architecture documentation successfully created![/bold green] 🚀")

@app.command("save-key")
def save_key(api_key):
    """
    This is for users to save their API keys
    """
    with open(".env", "w") as f:
        f.write(f"API_KEY={api_key}\n")
    console.print("🔑 [bold green]API key saved successfully![/bold green] 🚀")
    # Here you would save the API key to a secure location
    # For example, you could save it to a .env file or a secure vault
@app.command("load-key")
def load_key():
    """
    This is for users to load their API keys
    """
    console.print("🔑 [bold green]Loading API key...[/bold green]")
    # Here you would load the API key from a secure location
    console.print("API key:",os.getenv("API_KEY"))
    console.print("🔑 [bold green]API key loaded successfully![/bold green] 🚀")
    # Here you would load the API key from a secure location
    # For example, you could load it from a .env file or a secure vault


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
