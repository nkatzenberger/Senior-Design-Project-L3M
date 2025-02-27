#Automatically corrects path for developement enviorment and users enviorment.
import os
import sys

APP_NAME = "L3M"

def get_models_path():
    #Path for models folder in installed application 
    if getattr(sys, 'frozen', False):
        models_dir = os.path.join(os.getenv("LOCALAPPDATA"), APP_NAME, "models") 

    #Path for models folder in developement
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Go to "Senior-Design-Project-L3M/app"
        models_dir = os.path.join(base_dir, "models")
    
    os.makedirs(models_dir, exist_ok=True)
    return models_dir