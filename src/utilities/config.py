from pathlib import Path
import configparser

config_dir = Path.home() / ".devtoolgui"
config_path = config_dir / "config.ini"
config = configparser.ConfigParser()

Section = "Configuration"
Dir = "Project_Dir"
Git = "Use_Git"

def config_setup() -> Path:
    config_dir.mkdir(parents = True , exist_ok = True)
    if not config_path.exists() :
        config_path.touch()
    return config_path



def load_project_dir(default : str | None = None) -> str | None : 
    config_setup()
    config = configparser.ConfigParser()
    config.read(config_path)
    if config.has_option(Section , Dir) :
        v = config.get(Section , Dir).strip()
        return v if v else default
    return default

def load_project_options(defualt: bool = False) -> bool :
    config_setup()
    config = configparser.ConfigParser()
    config.read(config_path)
    if config.has_option(Section , Git) :
        try :
            return config.getboolean(Section , Git)
        except ValueError :
            return defualt
    return defualt
    
def update_project_dir(project_dir : str) :
    config_setup()
    config = configparser.ConfigParser()
    config.read(config_path)
    if not config.has_section(Section) : 
        config.add_section(Section)
    config.set(Section , Dir , str(project_dir))
    with config_path.open("w" , encoding = "utf-8") as f :
        config.write(f)

def update_project_options(git: bool) -> None:
    config_setup()
    config = configparser.ConfigParser()
    config.read(config_path)
    if not config.has_section(Section):
        config.add_section(Section)
    config.set(Section, Git, "true" if git else "false")
    with config_path.open("w", encoding="utf-8") as f:
        config.write(f)

