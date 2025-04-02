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
