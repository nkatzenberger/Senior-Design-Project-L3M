#Run this to install dependencies

import os
import subprocess
import sys

LIB_DIR = os.path.abspath("lib")
TORCH_CPU_DIR = os.path.join(LIB_DIR, "torch_cpu")
TORCH_CUDA_DIR = os.path.join(LIB_DIR, "torch_cuda")
REQUIREMENTS_FILE = "requirements.txt"

def install_requirements():
    print("Installing regular requirements from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install","--no-deps", "-r", REQUIREMENTS_FILE])
        print("requirements.txt dependencies installed.\n")
    except subprocess.CalledProcessError as e:
        print("Failed to install some packages from requirements.txt")
        print("    Error:", str(e))

def install_torch_cpu():
    if os.path.exists(os.path.join(TORCH_CPU_DIR, "torch")):
        print("torch_cpu already exists, skipping...")
        return
    print("Installing torch==2.6.0 (CPU) into lib/torch_cpu...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--no-deps", "torch==2.6.0",
            f"--target={TORCH_CPU_DIR}"
        ])
        print("torch_cpu installed.\n")
    except subprocess.CalledProcessError as e:
        print("Failed to install torch_cpu.")
        print("    Error:", str(e))

def install_torch_cuda():
    if os.path.exists(os.path.join(TORCH_CUDA_DIR, "torch")):
        print("torch_cuda already exists, skipping...")
        return
    print("Installing torch==2.6.0+cu118 (CUDA) into lib/torch_cuda...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "torch==2.6.0+cu118",
            "--index-url", "https://download.pytorch.org/whl/cu118",
            "--no-deps",
            "-f", "https://download.pytorch.org/whl/cu118",
            f"--target={TORCH_CUDA_DIR}",
        ])
        print("torch_cuda installed.\n")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install torch_cuda. This system may not support CUDA.")
        print("    Error:", str(e))

def main():
    os.makedirs(LIB_DIR, exist_ok=True)
    os.makedirs(TORCH_CPU_DIR, exist_ok=True)
    os.makedirs(TORCH_CUDA_DIR, exist_ok=True)

    install_requirements()
    install_torch_cpu()
    install_torch_cuda()
    print("All dependencies installed.")

if __name__ == "__main__":
    main()