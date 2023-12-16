import typer
from typing import Optional
from typing_extensions import Annotated
from codecraft.apps.Apps import Apps

app = typer.Typer()

@app.command()
def create(app_name: str, app_type: Annotated[Optional[str], typer.Argument()] = "exe", lib_type: Annotated[Optional[str], typer.Argument()] = ""):
    if app_type != "exe" and app_type != "lib":
        print(typer.Abort("Invalid app type! (must be 'exe' or 'lib')"))
    Apps.createApp(app_name, app_type, lib_type)

@app.command()
def delete(app_name: str):
    Apps.deleteApp(app_name)
    
@app.command()
def link(app_name: str, library_name: str, access: Annotated[Optional[str], typer.Argument()] = "PRIVATE", modules: Annotated[Optional[str], typer.Argument(..., help= "List of modules separated by comma")] = ""):
    modules_splited = [modules.strip() for element in modules.split(",")]
    Apps.linkLibrary(app_name, library_name, access, modules_splited)

@app.command()
def unlink(app_name: str, library_name: str):
    Apps.unlinkLibrary(app_name, library_name)

if __name__ == "__main__":
    app()
