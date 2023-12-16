import typer
import subprocess
from codecraft.commands.Projects import app as ProjectsApp
from codecraft.commands.Apps import app as AppsApp
from codecraft.commands.Build import app as BuildApp


app = typer.Typer()

app.add_typer(ProjectsApp, name="project")
app.add_typer(AppsApp, name="app")

@app.command()
def build(target: str="all", config: str = "Debug"):
    
    if config != "Debug" and config != "Release":
        print(typer.Abort("Invalid configuration type"))
    else:
        subprocess.call(["cmake","-S",".","-B","cmake/"+config,"-DCMAKE_BUILD_TYPE="+config])
        subprocess.call(["cmake","--build","cmake/"+config])
    

def start():
    app()