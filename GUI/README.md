This folder is for the GUI application that the user will install

This only works with python verion 3.12.3 currently. Make sure to be using this verions of python or the code will not work.

make sure to cd into the GUI folder to run and do, also advised to use a pip virtual environment in dev for making sure there are no package conflicts
info can be found here: https://www.activestate.com/blog/how-to-manage-dependencies-in-python/

```bash
$ pip install
```

will install everything in requirements.txt which is needed to run the app.
to update the file if new packages are added, do:

```bash
$ pip freeze > requirements.txt
```

-while CD'd into the GUI folder

to install a model:
```bash
$ cd gui
$ python modelDownload.py
```

to prompt the model you just installed run:
```bash
$ python gpt_prompt.py --prompt "ENTER PROMPT HERE"
```