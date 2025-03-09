This folder is for the installer that the user will download from the web-server that unpackages the GUI application

There are two main files in this folder.
build.py which takes the source files and creates a single exe for the user to installer.

installer.iss which takes the exe and packages it into an Inno installation package so the user can properly install

To run the build script:
1. CD into /app
2. Run pip install -r requirements.txt
3. CD into /installer
4. Run Python build.py

This will create a L3M.exe in the output folder.

To create the installer you must have Inno Setup installed. You can find this at https://jrsoftware.org/isdl.php

1. Open Inno Setup Compiler
2. Open the installer.iss file in the compiler
3. Run the compiler and the L3M_installer.exe will be created in the output folder