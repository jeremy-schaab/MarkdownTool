; Inno Setup Script for Markdown Manager
; This creates a professional Windows installer

#define MyAppName "Markdown Manager"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "Jeremy Schaab"
#define MyAppURL "https://github.com/jeremy-schaab/MarkdownTool"
#define MyAppExeName "MarkdownManager.exe"
#define MyAppDescription "A powerful markdown viewer, editor, and AI-powered summarization tool"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{8F2C9B4A-1234-5678-9ABC-DEF012345678}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=installer\LICENSE.txt
InfoBeforeFile=installer\README-INSTALLER.txt
InfoAfterFile=installer\SETUP-COMPLETE.txt
OutputDir=installer\output
OutputBaseFilename=MarkdownManager-Setup-v{#MyAppVersion}
SetupIconFile=assets\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
MinVersion=6.1
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppDescription}
VersionInfoCopyright=Copyright (C) 2024 {#MyAppPublisher}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startmenuicon"; Description: "Create Start Menu shortcut"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "addtopath"; Description: "Add to PATH environment variable (allows 'markdown-manager' command)"; GroupDescription: "System Integration"; Flags: unchecked

[Files]
; Main application
Source: "dist\MarkdownManager.exe"; DestDir: "{app}"; Flags: ignoreversion
; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "README.txt"
Source: "CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "CHANGELOG.txt"
Source: "docs\BUILDING_EXE.md"; DestDir: "{app}\docs"; Flags: ignoreversion; DestName: "BUILDING_EXE.txt"
Source: ".env.example"; DestDir: "{app}"; Flags: ignoreversion
; Test files for demo
Source: "test_files\*"; DestDir: "{app}\test_files"; Flags: ignoreversion recursesubdirs createallsubdirs
; License and installer docs
Source: "installer\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
; Visual C++ Redistributable (if needed)
; Source: "installer\vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall; Check: IsWin64

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppName} (Browser)"; Filename: "http://localhost:8501"; Comment: "Open {#MyAppName} in browser after starting"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\Test Files"; Filename: "{app}\test_files"; Comment: "Sample markdown files for testing"; IconFilename: "{sys}\shell32.dll"; IconIndex: 3
Name: "{group}\Configuration"; Filename: "notepad.exe"; Parameters: "{app}\.env.example"; Comment: "Edit configuration template"; IconFilename: "{sys}\shell32.dll"; IconIndex: 70
Name: "{group}\Documentation"; Filename: "{app}\README.txt"; Comment: "Read the documentation"; IconFilename: "{sys}\shell32.dll"; IconIndex: 23
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; IconFilename: "{sys}\shell32.dll"; IconIndex: 31

; Desktop icon (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Quick Launch (for older Windows versions)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"; Tasks: quicklaunchicon

[Run]
; Option to run the application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
; Open documentation
Filename: "{app}\README.txt"; Description: "Open README file"; Flags: postinstall skipifsilent shellexec unchecked
; Open configuration template
Filename: "notepad.exe"; Parameters: "{app}\.env.example"; Description: "Open configuration template"; Flags: postinstall skipifsilent unchecked

[UninstallRun]
; Clean up any running processes before uninstall
Filename: "taskkill"; Parameters: "/F /IM MarkdownManager.exe"; Flags: runhidden; RunOnceId: "KillMarkdownManager"

[UninstallDelete]
; Clean up user data (optional - ask user first)
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\sessions"
Type: filesandordirs; Name: "{app}\data"
Type: files; Name: "{app}\.env"

[Registry]
; Add to PATH if requested
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath(ExpandConstant('{app}'))
; File associations (optional)
Root: HKCR; Subkey: ".md"; ValueType: string; ValueName: ""; ValueData: "MarkdownManager.Document"; Flags: uninsdeletevalue
Root: HKCR; Subkey: ".markdown"; ValueType: string; ValueName: ""; ValueData: "MarkdownManager.Document"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "MarkdownManager.Document"; ValueType: string; ValueName: ""; ValueData: "Markdown Document"; Flags: uninsdeletekey
Root: HKCR; Subkey: "MarkdownManager.Document\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "MarkdownManager.Document\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Messages]
; Custom messages
WelcomeLabel1=Welcome to the [name/ver] Setup Wizard
WelcomeLabel2=This will install [name/ver] on your computer.%n%nMarkdown Manager is a powerful tool for viewing, editing, and AI-powered summarization of markdown documents.%n%nIt is recommended that you close all other applications before continuing.

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'PATH', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { look for the path with leading and trailing semicolon }
  { Pos() returns 0 if not found }
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function InitializeSetup(): Boolean;
var
  V: Integer;
  iResultCode: Integer;
  sUnInstallString: string;
begin
  Result := True; { in case when no previous version is found }
  if RegValueExists(HKEY_LOCAL_MACHINE,'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1', 'UninstallString') then  {Your App GUID/ID}
  begin
    V := MsgBox(ExpandConstant('An older version of {#emit SetupSetting("AppName")} is already installed. Do you want to uninstall the old version?'), mbInformation, MB_YESNO); {Custom message if app is installed}
    if V = IDYES then
    begin
      sUnInstallString := GetUninstallString();
      sUnInstallString := RemoveQuotes(sUnInstallString);
      if Exec(sUnInstallString, '/SILENT', '', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
        Result := True; {if uninstall was successful, continue with install}
      else
        Result := False; {if uninstall was unsuccessful, abort install}
    end
    else
      Result := False; {if user clicked No, abort install}
  end;
end;