from pathlib import Path
import configparser

config_dir = Path.home() / ".devtoolgui"
config_path = config_dir / "config.ini"
config = configparser.ConfigParser()

Section = "Configuration"
Key = "Project_Dir"

def config_setup() -> Path:
    config_dir.mkdir(parents = True , exist_ok = True)
    if not config_path.exists() :
        config_path.touch()
    return config_path



def load_project_dir(default : str | None = None) -> str | None : 
    config_setup()
    config = configparser.ConfigParser()
    config.read(config_path)
    if config.has_option(Section , Key) :
        v = config.get(Section , Key).strip()
        return v if v else default
    return default
    
def update_project_dir(project_dir : str) :
    config_setup()
    config = configparser.ConfigParser()
    config.read(config_path)
    if not config.has_section(Section) : 
        config.add_section(Section)
    config.set(Section , Key , str(project_dir))
    with config_path.open("w" , encoding = "utf-8") as f :
        config.write(f)

