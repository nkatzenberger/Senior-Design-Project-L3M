[Setup]
AppName=L3M
AppVersion=1.1.2
DefaultDirName={autopf}\L3M
DefaultGroupName=L3M
UninstallDisplayIcon={app}\L3M.exe
OutputDir=dist\L3M\L3M_Installer
OutputBaseFilename=L3M_Installer

; REQUIREMENTS
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; COMPRESSION
Compression=lzma2
SolidCompression=yes

; UI ENHANCEMENTS
WizardStyle=modern

DiskSpanning=yes



[Files]
; Include your PyInstaller-built EXE
Source: "dist\L3M\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{commondesktop}\L3M"; Filename: "{app}\L3M.exe"
Name: "{group}\L3M"; Filename: "{app}\L3M.exe"

[Run]
Filename: "{app}\L3M.exe"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
Type: filesandordirs; Name: "{localappdata}\L3M"

