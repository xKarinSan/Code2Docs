import typer

app = typer.Typer()


@app.command()
def hello(name: str, iq: int, display_iq:bool = True):
    print(f"Hello {name}")
    if display_iq:
        print(f"This is your IQ: {iq}")


@app.command()
def goodbye():
    print("Goodbye")


if __name__ == "__main__":
    app()
