# core file (defining the logic)
from pathlib import Path
from .utilities import git as g

def create_project(project_dir , project_name , mainfile_name , use_git : bool) :
    project_path = Path(project_dir) / project_name
    counter = 1
    while project_path.exists():
        project_path = Path(project_dir) / f"{project_name}_{counter}"
        counter += 1
    project_path.mkdir(parents=True , exist_ok= False)
    mainfile = create_mainfile(project_path , mainfile_name)
    git_o = g.git_init(project_path , use_git) if use_git else None
    return project_path , mainfile , git_o

def create_mainfile(project_path , filename) :
    if not filename.lower().endswith('.py') :
        filename += ".py"
    file_path = project_path / filename
    file_path.touch()
    return file_path
