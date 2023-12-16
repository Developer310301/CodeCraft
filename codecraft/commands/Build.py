import typer
from typing import Optional
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def all():
    return

if __name__ == "__main__":
    app()