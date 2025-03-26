# installs the right version of torch depending on the system

import subprocess
import sys
import os

def has_gpu():
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def upgrade_pip():
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_torch():
    if has_gpu():
        print("💻 GPU detected — installing torch with CUDA...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "torch==2.6.0+cu118",
            "--extra-index-url", "https://download.pytorch.org/whl/cu118"
        ])
    else:
        print("🖥️ No GPU detected — installing CPU-only torch...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "torch==2.6.0"
        ])

def install_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

def main():
    upgrade_pip()
    install_requirements()
    install_torch()

if __name__ == "__main__":
    main()
