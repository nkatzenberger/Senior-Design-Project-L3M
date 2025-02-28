import os
import shutil
import PyInstaller.__main__

# Define base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up to Senior-Design/
APP_DIR = os.path.join(BASE_DIR, "app")
L3M_DIR = os.path.join(APP_DIR, "l3m")
UTILS_DIR = os.path.join(BASE_DIR, "app", "utils")
ENTRY_SCRIPT = os.path.join(APP_DIR, "main.py")
REQUIREMENTS_FILE = os.path.join(APP_DIR, "requirements.txt")

# Build output locations
BUILD_DIR = os.path.join(os.path.dirname(__file__), "build")
SPEC_FILE = os.path.join(BUILD_DIR, "L3M.spec")
COPIED_REQUIREMENTS_FILE = os.path.join(BUILD_DIR, "requirements_copy.txt") #Will be recoded so it can be parsed

# Application details
APP_NAME = "L3M"
ICON_PATH = None  # Set this when we have an icon, e.g., os.path.join(APP_DIR, "resources", "icon.ico")

# Ensure clean build
def clean_build():
    print("Cleaning old build files...")
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
        print(f"Deleted {BUILD_DIR}")

    if os.path.exists(SPEC_FILE):
        os.remove(SPEC_FILE)
        print(f"Deleted {SPEC_FILE}")

# Creates a copy of requirements.txt in the build folder.
def copy_requirements():
    if not os.path.exists(BUILD_DIR): # Ensure build directory exists
        os.makedirs(BUILD_DIR)

    if os.path.exists(REQUIREMENTS_FILE):
        shutil.copy(REQUIREMENTS_FILE, COPIED_REQUIREMENTS_FILE)

# Fixes encoding issues in requirements.txt
def fix_requirements_encoding():
    if os.path.exists(COPIED_REQUIREMENTS_FILE):
        with open(COPIED_REQUIREMENTS_FILE, "rb") as file:  # Read raw bytes
            raw_content = file.read()

        # Remove null bytes and decode as UTF-8
        fixed_content = raw_content.replace(b'\x00', b'').decode("utf-8", "ignore")

        # Overwrite the file with fixed content
        with open(COPIED_REQUIREMENTS_FILE, "w", encoding="utf-8") as file:
            file.write(fixed_content)

# Read dependencies from requirements.txt
def get_hidden_imports():
    hidden_imports = []

    if os.path.exists(COPIED_REQUIREMENTS_FILE):
        with open(COPIED_REQUIREMENTS_FILE, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                package = line.strip().split("==")[0]  # Extract package name only
                if package and not package.startswith("#"):  # Ignore comments
                    clean_name = package.replace("-", "_")  # Convert `transformers-4.2.0` -> `transformers`
                    hidden_imports.append("--hidden-import")
                    hidden_imports.append(clean_name)

    return hidden_imports

# Build the executable
def build_exe():
    print("Building the executable...")

    pyinstaller_args = [
        ENTRY_SCRIPT,  # Main script
        "--name", APP_NAME,  # Output file name
        "--onefile",  # Bundle into a single .exe
        "--windowed",  # No console window
        "--distpath", BUILD_DIR,  # Save final output in installer/build/
        "--workpath", BUILD_DIR,  # Temporary build files in installer/build/
        "--specpath", BUILD_DIR,  # Store .spec file in installer/build/
        "--add-data", f"{L3M_DIR};l3m/",  # Ensure `l3m/` folder is included
        "--add-data", f"{UTILS_DIR};utils/",  # Ensure `utils/` folder is included
    ]

    # Add hidden imports for all dependencies
    pyinstaller_args.extend(get_hidden_imports())

    # Add icon path once we have that
    if ICON_PATH:
        pyinstaller_args.extend(["--icon", ICON_PATH])
    
    PyInstaller.__main__.run(pyinstaller_args)

# Execute build process
def main():
    clean_build()
    copy_requirements()
    fix_requirements_encoding()
    print(get_hidden_imports())
    build_exe()
    print(f"Build complete! .exe is located in '{BUILD_DIR}/'")

if __name__ == "__main__":
    main()
