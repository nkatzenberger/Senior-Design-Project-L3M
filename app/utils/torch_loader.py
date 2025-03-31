import os
import sys

class TorchLoader:
    @classmethod
    def _get_path(cls, folder):
        base_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
        return os.path.abspath(os.path.join(base_dir, "..", "lib", folder))

    @classmethod
    def load(cls):
        use_cuda = os.environ.get("FORCE_CPU_TORCH") != "1" #For CircleCI
        cuda_path = cls._get_path("torch_cuda")
        cpu_path = cls._get_path("torch_cpu")

        try:
            if use_cuda:
                sys.path.insert(0, cuda_path)
                import torch
                if torch.cuda.is_available():
                    cls._torch = torch
                    cls._device = torch.device("cuda")
                    print("Using GPU torch")
                    return
                raise RuntimeError("CUDA not available or not detected")
            raise RuntimeError("FORCE_CPU_TORCH is set")
        except Exception as e:
            print(f"Falling back to CPU torch: {e}")
            # Remove the possibly-bad torch import
            if "torch" in sys.modules:
                del sys.modules["torch"]
            if cuda_path in sys.path:
                sys.path.remove(cuda_path)

            sys.path.insert(0, cpu_path)
            import torch  # fresh import after sys.path change
            cls._torch = torch
            cls._device = torch.device("cpu")
            print("Using CPU torch from:", cpu_path)

        # Ensure consistency
        sys.modules["torch"] = cls._torch

# Automatically run on import
TorchLoader.load()