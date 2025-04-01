import os
import logging
from logging.handlers import RotatingFileHandler
from utils.path_utils import PathManager

class LogManager:
    logger = None

    @classmethod
    def _initialize_logger(cls):
        if cls.logger is not None:
            return  # Already initialized

        log_file = os.path.join(PathManager.get_logs_path(), "L3M.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
        handler.setFormatter(formatter)

        cls.logger = logging.getLogger("L3MLogger")
        cls.logger.setLevel(logging.DEBUG)
        cls.logger.addHandler(handler)

    @classmethod
    def log(cls, level, message):
        cls._initialize_logger()

        if level == "debug":
            cls.logger.debug(message)
        elif level == "info":
            cls.logger.info(message)
        elif level == "warning":
            cls.logger.warning(message)
        elif level == "error":
            cls.logger.error(message)
        elif level == "critical":
            cls.logger.critical(message)