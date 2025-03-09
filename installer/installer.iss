[Setup]
AppName=L3M
AppVersion=1.0
DefaultDirName={pf}\L3M
DefaultGroupName=L3M
OutputDir=output
OutputBaseFilename=L3M_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "output\L3M.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\L3M"; Filename: "{app}\L3M.exe"
Name: "{group}\L3M"; Filename: "{app}\L3M.exe"

[Run]
Filename: "{app}\L3M.exe"; Description: "Launch L3M Desktop App"; Flags: nowait postinstall

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
