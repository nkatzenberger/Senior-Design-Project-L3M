#Automatically corrects path for developement enviorment and users enviorment.
import os
import sys

class PathManager:
    APP_NAME = "L3M"

    @classmethod
    def get_models_path(cls):
        #Path for models folder in installed application 
        if getattr(sys, 'frozen', False):
            models_dir = os.path.join(os.getenv("LOCALAPPDATA"), cls.APP_NAME, "models") 

        #Path for models folder in developement
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Go to "Senior-Design-Project-L3M/app"
            models_dir = os.path.join(base_dir, "models")
        
        os.makedirs(models_dir, exist_ok=True)
        return models_dir
    
    @classmethod
    def get_logs_path(cls):
        #Path for logs folder in installed application
        if getattr(sys, 'frozen', False):  # Running as an installed .exe
            logs_dir = os.path.join(os.getenv("LOCALAPPDATA"), cls.APP_NAME, "logs")

        #Path for models folder in developement
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            logs_dir = os.path.join(base_dir, "logs")

        os.makedirs(logs_dir, exist_ok=True)
        return logs_dir