[Setup]
AppId={{32CDB05E-87D3-44D4-B01C-6175A7878A1F}
AppName=Marco Vídeo
AppVersion=1.1.0
AppPublisher=Marco Pescador
AppPublisherURL=https://github.com/Peskysa/marco-video
DefaultDirName={localappdata}\Programs\Marco Video
DefaultGroupName=Marco Vídeo
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=Marco-Video-Windows-Instalador
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
LicenseFile=..\LICENSE
UninstallDisplayIcon={app}\Marco Video.exe
[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
[Files]
Source: "..\dist\Marco Video\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\Marco Vídeo"; Filename: "{app}\Marco Video.exe"
Name: "{userdesktop}\Marco Vídeo"; Filename: "{app}\Marco Video.exe"
[Run]
Filename: "{app}\Marco Video.exe"; Description: "Marco Vídeo"; Flags: nowait postinstall skipifsilent
