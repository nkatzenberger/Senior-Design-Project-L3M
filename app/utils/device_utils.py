
import torch
from utils.logging_utils import log_message

class DeviceManager:
    @staticmethod
    def supports_float16():
        if not torch.cuda.is_available():
            return False
        major = torch.cuda.get_device_capability()[0]
        return major >= 6

    @staticmethod
    def get_best_dtype():
        dtype = torch.float16 if DeviceManager.supports_float16() else torch.float32
        log_message("info", f"Using dtype: {dtype}")
        return dtype

    @staticmethod
    def get_best_device():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        log_message("info", f"Using device: {device}")
        return device
