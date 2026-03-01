import os
import yaml
from pathlib import Path
from rich.console import Console

class ProjectConsole:
    def __init__(self):
        self._console = Console()

    def error(self, msg: str):
        self._console.print(msg, style='bold red')

    def success(self, msg: str):
        self._console.print(msg, style='bold green')

    def info(self, msg: str):
        self._console.print(msg, style='cyan')

class ProjectContext:
    def __init__(self):
        self._config = None
        self._load_config()
        self.console = ProjectConsole()

    @property
    def project_root_dir(self) -> str:
        # Resolve the root directory dynamically relative to this file
        path = Path(os.path.dirname(os.path.realpath(__file__)))
        return str(path.parent.absolute())

    @property
    def config_file_path(self) -> str:
        return os.path.join(self.project_root_dir, 'config', 'config.yaml')

    def _load_config(self):
        with open(self.config_file_path, 'r') as f:
            self._config = yaml.safe_load(f.read())

    @property
    def project_name(self) -> str:
        return self._config.get('project_name', 'studbuddy')

    @property
    def version(self) -> str:
        return str(self._config.get('version', '0.0.1'))

    @property
    def aws_region(self) -> str:
        return self._config.get('aws_region', 'us-east-1')

    @property
    def source_dir(self) -> str:
        return os.path.join(self.project_root_dir, 'source')
        

# Singleton instance for tasks to import
context = ProjectContext()
