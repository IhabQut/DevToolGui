import subprocess
from pathlib import Path


def git_init(project_dir) :
    if not is_git_available():
        raise RuntimeError("Git is not installed or not in PATH")
    try : 
        init  = subprocess.run(["git" , "init"], cwd = Path(project_dir) , check = True , capture_output = True , text= True)
        add = git_add(project_dir)
        commit = git_commit(project_dir)
        return "\n".join([
             init.stdout.strip(),
             add.strip(),
             commit.strip()
            ]).strip()
    
    except subprocess.CalledProcessError as e:
        msg = (e.stderr or e.stdout or str(e)).strip()
        raise RuntimeError(f"Git command failed: {msg}") from e


def git_add(project_dir) :
    subprocess.run(["git", "add", "."] , cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    return "Files staged successfully"

def git_commit(project_dir) : 
    commit  = subprocess.run(["git" , "commit" , "-m" , "Initial commit"], cwd = Path(project_dir) , check = True , capture_output = True , text= True)
    return commit.stdout

def is_git_available() -> bool:
    try : 
        subprocess.run(["git" , "--version"] , capture_output = True , check = True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False