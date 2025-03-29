[Setup]
AppName=L3M
AppVersion=1.1.0
DefaultDirName={pf}\L3M
DefaultGroupName=L3M
OutputDir=output
OutputBaseFilename=L3M_Installer
Compression=lzma
SolidCompression=yes

[Files]
; Include your PyInstaller-built EXE
Source: "output\L3M.exe"; DestDir: "{app}"; Flags: ignoreversion

; Include post-install script and cleaned requirements
Source: "post_install.py"; DestDir: "{app}"; Flags: ignoreversion

; Include embedded Python with pip support
Source: "python-embed\*"; DestDir: "{app}\python"; Flags: recursesubdirs ignoreversion



[Icons]
Name: "{commondesktop}\L3M"; Filename: "{app}\L3M.exe"
Name: "{group}\L3M"; Filename: "{app}\L3M.exe"



[Run]
; Install pip into embedded Python
Filename: "{app}\python\python.exe"; Parameters: """{app}\python\get-pip.py"""; Flags: runhidden

; Run post-install script to install deps + correct torch version
Filename: "{app}\python\python.exe"; Parameters: """{app}\post_install.py"""; Flags: runhidden

; Launch the app
Filename: "{app}\python\python.exe"; Parameters: """{app}\L3M.exe"""; Flags: nowait postinstall skipifsilent



[UninstallDelete]
Type: filesandordirs; Name: "{app}"
Type: filesandordirs; Name: "{localappdata}\L3M"

