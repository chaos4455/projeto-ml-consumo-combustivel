import shutil
import os

def translate_project(source_dir, target_dir):
    """Copies the project files to a new directory."""
    try:
        shutil.copytree(source_dir, target_dir)
        print(f"Project copied successfully to {target_dir}")
    except Exception as e:
        print(f"Error copying project: {e}")

if __name__ == "__main__":
    source_dir = "."
    target_dir = "projeto-en"
    translate_project(source_dir, target_dir)
