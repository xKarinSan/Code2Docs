import typer

app = typer.Typer()


@app.command("wave")
def hello(name: str, iq: int, display_iq: bool = True):
    """
    To say hello
    name (string): name of person
    iq (int): iq of person
    """
    print(f"Hello {name}")
    if display_iq:
        print(f"This is your IQ: {iq}")


@app.command("bye")
def goodbye():
    """
    To say goodbye
    """
    print("Goodbye")


if __name__ == "__main__":
    app()
