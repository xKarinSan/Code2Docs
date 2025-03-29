from pathlib import Path
import os
from dotenv import load_dotenv
import typer


app = typer.Typer(no_args_is_help=True)


@app.command("upload-key")
def upload_key(key: str):
    """
    \b
    To upload an API key.
    \nParameters:
      - key (string): the value of the API key
    \nExample:
      code2docs-cli upload-key test_key
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
    \b
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
    \b
    To say hello. here are the following parameters
    \nParameters:
      - name (string): Name of the person
      - iq (int): IQ of the person
      - display_iq (bool, optional): Whether to display the IQ (default: True)
    \nExample:
      code2docs-cli wave John 130 --display-iq
    """
    print(f"Hello {name}")
    if display_iq:
        print(f"This is your IQ: {iq}")

if __name__ == "__main__":
    load_dotenv()
    app()
