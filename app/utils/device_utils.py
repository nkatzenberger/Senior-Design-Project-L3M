import torch
from utils.logging_utils import log_message

class DeviceManager:
    @staticmethod
    def supports_float16():
        try:
            if not torch.cuda.is_available():
                return False
            major = torch.cuda.get_device_capability()[0]
            return major >= 6
        except Exception as e:
            log_message("warning", f"Failed to check float16 support: {e}")
            return False

    @staticmethod
    def get_best_dtype():
        try:
            dtype = torch.float16 if DeviceManager.supports_float16() else torch.float32
        except Exception as e:
            dtype = None
            log_message("warning", f"Torch not available — dtype fallback: {e}")
        log_message("info", f"Using dtype: {dtype}")
        return dtype

    @staticmethod
    def get_best_device():
        try:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        except Exception as e:
            device = torch.device("cpu")
            log_message("warning", f"Torch not available — using CPU: {e}")
        log_message("info", f"Using device: {device}")
        return device

