import typer

from codecraft.projects.Projects import Projects

app = typer.Typer()


@app.command()
def create(project_name: str):
    Projects.createProject(project_name)


@app.command()
def delete(project_name: str):
    Projects.deleteProject()


if __name__ == "__main__":
    app()
