import os
import shutil
from invoke import task

BUILD_DIR = "build/lambda/resume_reviewer"
SRC_DIR = "src/infrastructure/lambda/resume_reviewer"

@task
def clean(c):
    """Cleans all compiled/packaged artifacts."""
    print("Cleaning build directories...")
    if os.path.exists("build"):
        shutil.rmtree("build")

@task(pre=[clean])
def package(c):
    """Packages the lambda code and requirements into a clean build folder."""
    print(f"Packaging Lambda from '{SRC_DIR}'...")
    
    # Ensure fresh directory
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    # 1. Install dependencies natively into build target
    print("Installing dependencies into package...")
    req_file = os.path.join(SRC_DIR, "requirements.txt")
    
    # Force pip to download AWS Lambda compatible specific Linux binaries (avoiding Mac C-extensions!) 
    cmd = (
        f"pip install -r {req_file} "
        f"-t {BUILD_DIR} "
        "--platform manylinux2014_x86_64 "
        "--implementation cp "
        "--python-version 3.12 "
        "--only-binary=:all: "
        "--upgrade"
    )
    c.run(cmd, hide="err")
    
    # 2. Copy the actual Python source scripts into the same folder
    print("Copying Python handlers...")
    for item in os.listdir(SRC_DIR):
        if item.endswith(".py"):
            src_file = os.path.join(SRC_DIR, item)
            dst_file = os.path.join(BUILD_DIR, item)
            shutil.copy2(src_file, dst_file)
            
    print("Packaging phase complete! Artifacts are ready in 'build/'.")
