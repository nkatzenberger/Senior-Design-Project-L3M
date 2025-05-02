This folder is for the GUI application that the user will install

This only works with python verion 3.12.3 currently. Make sure to be using this verions of python or the code will not work.

Make sure to cd into the GUI folder to run, also its strongly advised to use a pip virtual environment in dev for making sure there are no package conflicts
info can be found here: https://www.activestate.com/blog/how-to-manage-dependencies-in-python/

To create a virtual environmnt do:
```bash
$ python3.12 -m venv venv
```

To activate the venv do:
```bash
$ venv/Scripts/activate
```

To install all dependencies run our install script:
```bash
$ python install_deps.py
```
will install everything in requirements.txt as well as create a lib folder with two versions of torch which is needed to run the app. The app auto selects the correct version of torch depending on your system.

To start the app run:
```bash
$ python main.py
```
this is our entry script

To update the file if new packages are added:
1. Add the package manually to requirements.in
2. If pip-tools is not installed install it
```bash
$ pip install pip-tools
```
3. Create new requirements txt by running:
```bash
$ pip-compile --upgrade requirements.in
```
4. Important! - Delete Torch, TorchVision, TorchAudio from requirements.txt