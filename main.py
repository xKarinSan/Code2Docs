from pathlib import Path
import os
from dotenv import load_dotenv
import typer


app = typer.Typer()


@app.command("upload-key")
def upload_key(key: str):
    """
    To upload an API key
    """
    if not key:
        print("Key not found")
    else:
        env_path = Path(".env")
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
    load_dotenv()
    app()
