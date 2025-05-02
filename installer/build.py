import os
import shutil
import PyInstaller.__main__

# Define base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up to Senior-Design/
APP_DIR = os.path.join(BASE_DIR, "app")
L3M_DIR = os.path.join(APP_DIR, "l3m")
UTILS_DIR = os.path.join(APP_DIR, "utils")
LIB_DIR = os.path.join(APP_DIR, "lib")
ENTRY_SCRIPT = os.path.join(APP_DIR, "main.py")

# Build output locations
BUILD_DIR = os.path.dirname(__file__)
DIST_DIR = os.path.join(BUILD_DIR, "dist")
WORK_DIR = os.path.join(BUILD_DIR, "build")
SPEC_DIR = os.path.join(BUILD_DIR, "spec")

# Application details
APP_NAME = "L3M"
ICON_PATH = os.path.join(APP_DIR, "resources", "L3M-icon.ico")

# Ensure clean build
def clean_build():
    print("Removing old build files...")

    for folder_name in ["dist", "build", "spec"]:
        full_path = os.path.join(BUILD_DIR, folder_name)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
            print(f"Deleted {full_path}")

# Build the executable
def build_exe():
    print("Building Executable...")

    pyinstaller_args = [
        ENTRY_SCRIPT,
        "--name", APP_NAME,
        "--icon", ICON_PATH,
        "--onedir",
        "--windowed",
        "--distpath", DIST_DIR,
        "--workpath", WORK_DIR,
        "--specpath", SPEC_DIR,
        "--clean",

        # Include required application directories
        "--add-data", f"{L3M_DIR};l3m/",
        "--add-data", f"{UTILS_DIR};utils/",
        "--add-data", f"{LIB_DIR}/torch_cpu;lib/torch_cpu",
        "--add-data", f"{LIB_DIR}/torch_cuda;lib/torch_cuda",

        # Hidden imports required at runtime
        "--hidden-import", "pickletools",
        "--hidden-import", "lzma",
        "--hidden-import", "multiprocessing.spawn",
        "--hidden-import", "importlib.machinery",
        "--hidden-import", "queue",
        "--hidden-import", "typing_extensions",
        "--hidden-import", "sympy",
        "--hidden-import", "modulefinder",
        "--hidden-import", "PIL.ImageEnhance",
        "--hidden-import", "PIL.ImageFilter",
        "--hidden-import", "PIL.ImageOps",
        "--hidden-import", "PIL.ImageChops",
        "--hidden-import", "html.parser",

        # Exclude heavy or unused modules
        "--exclude-module", "torch",
        "--exclude-module", "torchaudio",
        "--exclude-module", "torchvision",
        "--exclude-module", "pytest",
        "--exclude-module", "_pytest",
        "--exclude-module", "test",
        "--exclude-module", "venv",
        "--exclude-module", "ensurepip",
    ]

    PyInstaller.__main__.run(pyinstaller_args)

# Remove unnecessary build files after compilation
def clean_temp_files():
    print("Cleaning temp files")

    for folder_name in ["build", "spec"]:
        full_path = os.path.join(BUILD_DIR, folder_name)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
            print(f"Deleted {full_path}")

# Execute build process
def main():
    clean_build()
    build_exe()
    clean_temp_files()
    print(f"Build complete! .exe is located in '{DIST_DIR}/'")

if __name__ == "__main__":
    main()
