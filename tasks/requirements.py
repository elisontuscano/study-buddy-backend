import os
import sys
from typing import Optional

from invoke import task, Context

# Import the singleton context object we built
from tasks.context import context

def _update_requirement(c: Context, name: str, upgrade: bool = False, package_name: str = None):
    project_root = context.project_root_dir

    name = name.strip().lower()

    if name.endswith('.txt'):
        name = name.replace('.txt', '')
    if '.' in name:
        name = name[:name.rfind('.')]

    in_file = f'{name}.in'
    in_file_abs_path = os.path.join(project_root, 'requirements', in_file)

    if not os.path.isfile(in_file_abs_path):
        context.console.error(f"Requirements .in file not found: {in_file_abs_path}")
        sys.exit(1)

    out_file = f'{name}.txt'
    out_file_abs_path = os.path.join(project_root, 'requirements', out_file)

    cmd = 'pip-compile --no-header --no-annotate --no-emit-index-url '
    if upgrade:
        cmd += '--upgrade '
    if package_name:
        cmd += f'--upgrade-package {package_name} '
    cmd += f'--output-file "{out_file_abs_path}" "{in_file_abs_path}"'
    
    # We use pty=True so the output looks colorful and nice in the terminal
    c.run(cmd, pty=True)

    out_file = f'{name}.txt'
    out_file_abs_path = os.path.join(project_root, 'requirements', out_file)
    context.console.success(f"Requirements file updated: {out_file_abs_path}")


@task(optional=['name'])
def update(c, name=None, upgrade=False, package_name=None):
    # type: (Context, Optional[str], bool, str) -> None
    """
    Update python requirements using pip-compile. 
    (e.g., invoke req.update --name=dev)
    """
    if name is not None:
        _update_requirement(c, name, upgrade, package_name)
        return

    for req_name in ['dev']:
        _update_requirement(c, req_name, upgrade, package_name)
    


@task(optional=['name'])
def install(c, name=None):
    # type: (Context, Optional[str]) -> None
    """
    Install python requirements (e.g., inv req.install --name=dev)
    """
    project_root = context.project_root_dir

    if name is None:
        name = 'dev'

    req_txt = os.path.join(project_root, 'requirements', f'{name}.txt')
    if not os.path.isfile(req_txt):
        context.console.error(f'Requirements .txt file not found: {req_txt}')
        sys.exit(1)

    c.run(f'pip install -r {req_txt}', pty=True)
