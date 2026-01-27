# core file (defining the logic)
from pathlib import Path
import subprocess

def create_project(project_dir , project_name , mainfile_name) :
    project_path = Path(project_dir) / project_name
    counter = 1
    while project_path.exists():
        project_path = Path(project_dir) / f"{project_name}_{counter}"
        counter += 1
    project_path.mkdir(parents=True , exist_ok= False)
    mainfile = create_mainfile(project_path , mainfile_name)
    return project_path , mainfile

def create_mainfile(project_path , filename) :
    if not filename.lower().endswith('.py') :
        filename += ".py"
    file_path = project_path / filename
    file_path.touch()
    return file_path

# git section

def git_init(project_dir) :
    init  = subprocess.run(["git" , "init"], cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    return init.stdout
    
def git_add(project_dir) :
    subprocess.run(["git", "add", "."] , cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    return "Files staged successfully"

def git_commit(project_dir) : 
    commit  = subprocess.run(["git" , "commit" , "-m" , "Initial commit"], cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    return commit.stdout