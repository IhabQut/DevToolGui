import subprocess
from pathlib import Path


def git_init(project_dir) :
    init  = subprocess.run(["git" , "init"], cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    add = git_add(project_dir)
    commit = git_commit(project_dir)
    return init.stdout , add , commit
    
def git_add(project_dir) :
    subprocess.run(["git", "add", "."] , cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    return "Files staged successfully"

def git_commit(project_dir) : 
    commit  = subprocess.run(["git" , "commit" , "-m" , "Initial commit"], cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    return commit.stdout