This is the web server that will provide static html web pages and the file for the installer

make sure to cd into the web server backend to run and do, also advised to use a pip virtual environment in dev for making sure there are no package conflicts
info can be found here: https://www.activestate.com/blog/how-to-manage-dependencies-in-python/

```bash
$ pip install
```

will install everything in requirements.txt which is needed to run the app.
to update the file if new packages are added, do:

```bash
$ pip freeze > requirements.txt
```

-while CD'd into the web server backend folder

to run:
```bash
$ cd webServer/backend
$ python app.py
```