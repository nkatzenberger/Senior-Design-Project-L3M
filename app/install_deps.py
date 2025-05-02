import os
import subprocess
import sys

REQUIREMENTS_FILE = "requirements.txt"
LIB_DIR = os.path.abspath("lib")
TORCH_CPU_DIR = os.path.join(LIB_DIR, "torch_cpu")
TORCH_CUDA_DIR = os.path.join(LIB_DIR, "torch_cuda")

def pip_install(package, target_dir, extra_index=None):
    cmd = [sys.executable, "-m", "pip", "install", package, "--no-deps", f"--target={target_dir}"]
    if extra_index:
        cmd += ["--index-url", extra_index]
    print(f"\nInstalling {package} into {target_dir}...")
    subprocess.check_call(cmd)

def install_requirements():
    print("Installing requirements from requirements.txt...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--no-deps", "-r", REQUIREMENTS_FILE
        ])
        print("requirements.txt dependencies installed.\n")
    except subprocess.CalledProcessError as e:
        print("Failed to install some packages from requirements.txt")
        print("    Error:", str(e))

def install_torch_cpu():
    if os.path.exists(os.path.join(TORCH_CPU_DIR, "torch")):
        print("torch_cpu already exists, skipping...")
    else:
        pip_install("torch", TORCH_CPU_DIR, extra_index="https://download.pytorch.org/whl/cpu")
        pip_install("torchaudio", TORCH_CPU_DIR, extra_index="https://download.pytorch.org/whl/cpu")
        pip_install("torchvision", TORCH_CPU_DIR, extra_index="https://download.pytorch.org/whl/cpu")

def install_torch_cuda():
    if os.path.exists(os.path.join(TORCH_CUDA_DIR, "torch")):
        print("torch_cuda already exists, skipping...")
    else:
        pip_install("torch", TORCH_CUDA_DIR, extra_index="https://download.pytorch.org/whl/cu118")
        pip_install("torchvision", TORCH_CUDA_DIR, extra_index="https://download.pytorch.org/whl/cu118")
        pip_install("torchaudio", TORCH_CUDA_DIR, extra_index="https://download.pytorch.org/whl/cu118")

def main():
    os.makedirs(LIB_DIR, exist_ok=True)
    os.makedirs(TORCH_CPU_DIR, exist_ok=True)
    os.makedirs(TORCH_CUDA_DIR, exist_ok=True)

    install_requirements()
    install_torch_cpu()
    install_torch_cuda()
    print("\n✅ All dependencies installed.")

if __name__ == "__main__":
    main()
