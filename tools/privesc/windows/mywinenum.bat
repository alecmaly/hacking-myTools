@ECHO OFF & SETLOCAL EnableDelayedExpansion
TITLE WinPEAS - Windows local Privilege Escalation Awesome Script
COLOR 0F
CALL :SetOnce

REM :: WinPEAS - Windows local Privilege Escalation Awesome Script
REM :: Code by carlospolop; Re-Write by ThisLimn0

REM Registry scan of other drives besides 
REM /////true or false
SET long=false

:Splash
ECHO.
CALL :ColorLine "   %E%32m((,.,/((((((((((((((((((((/,  */%E%97m"
CALL :ColorLine "   %E%32m,/*,..*(((((((((((((((((((((((((((((((((,%E%97m"              

ECHO.


@REM  print colors
for %%a in (31 32 33 34 35 36) do (
    CALL :ColorLine "%E%%%am%%a%%%E%97m" 
    echo %%a
)
echo.
echo.
echo.
echo.



@REM environment
CALL :ColorLine "%E%33m[+] ENVIRONMENT%E%97m"
CALL :ColorLine "   %E%33m[+] os version%E%97m"
systeminfo | findstr /C:"OS Name" /C:"OS Version" /C:"System Type"
echo.

CALL :ColorLine "   %E%33m[+] architecture%E%97m"
wmic os get osarchitecture || echo %PROCESSOR_ARCHITECTURE%
echo.


CALL :ColorLine "   %E%33m[+] environment variables%E%97m"
set
echo.

CALL :ColorLine "   %E%33m[+] drives%E%97m"
powershell -c "get-psdrive"
echo.



@REM user
CALL :ColorLine "%E%33m[+] USER%E%97m"
CALL :ColorLine "   %E%33m[+] user info (groups)%E%97m"
net user %username%
echo.

CALL :ColorLine "   %E%33m[+] whoami /all%E%97m"
whoami /all
echo.

CALL :ColorLine "   %E%33m[+] other users%E%97m"
net user
echo.

CALL :ColorLine "   %E%33m[+] other doamin users%E%97m"
net user /domain
echo.

CALL :ColorLine "   %E%33m[+] dir C:\users%E%97m"
dir C:\Users
echo.




@REM filesystem
CALL :ColorLine "%E%33m[+] FILESYSTEM%E%97m"
CALL :ColorLine "   %E%33m[+] C:\ (any unusual directories? e.g. 'backup')%E%97m"
dir C:\
echo.

CALL :ColorLine "   %E%33m[+] desktop%E%97m"
dir %userprofile%\desktop
echo.

CALL :ColorLine "   %E%33m[+] documents%E%97m"
dir %userprofile%\documents
echo.


CALL :ColorLine "   %E%33m[+] Check recycle bin%E%97m"
for /f "tokens=*" %%f in ('wmic useraccount where "name='%%username%%'" get sid /value ^| findstr "SID"') do set "%%f"
CALL :ColorLine "%E%33mc:\$recycle.bin\%SID%%E%97m"
dir c:\$recycle.bin\%SID%
echo.



CALL :ColorLine "   %E%33m[+] Alternative Data Streams in homepath: %userprofile%%E%97m"
dir /S /r %userprofile% | find ":$DATA"
echo.


CALL :ColorLine "   %E%33m[+] PowerShell History%E%97m"
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
echo.


CALL :ColorLine "   %E%33m[+] doskey /history%E%97m"
doskey /history
echo.



echo.
CALL :ColorLine "   %E%33m[+] Network%E%97m"
netstat -ano | findstr LISTENING
echo.





@REM credentials

CALL :ColorLine "%E%33m[+] CREDENTIALS%E%97m"
CALL :ColorLine "   %E%33m[+] winlogon credentials %E%97m"
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr /i "DefaultDomainName DefaultUserName DefaultPassword AltDefaultDomainName AltDefaultUserName AltDefaultPassword LastUsedUsername"
echo.

CALL :ColorLine "   %E%33m[+] cmdkey /list%E%97m"
cmdkey /list
echo.


CALL :ColorLine "   %E%33m[+] clipboard %E%97m"
powershell.exe -c "get-clipboard"
echo.

CALL :ColorLine "   %E%33m[+] wifi passwords %E%97m"
for /f "tokens=4 delims=: " %%a in ('netsh wlan show profiles ^| find "Profile "') do (netsh wlan show profiles name=%%a key=clear | findstr "SSID Cipher Content" | find /v "Number" & echo.) 
echo.


IF "%SYSTEMROOT%"=="" (set vSystemRoot=C:\windows) ELSE (set vSystemRoot=%SYSTEMROOT%)
echo %vSystemRoot%

CALL :ColorLine "   %E%33m[+] unattended files %E%97m"
if exist %vSystemRoot%\sysprep\sysprep.xml (CALL :ColorLine "%E%31m%vSystemRoot%\sysprep\sysprep.xml%E%97m")
if exist %vSystemRoot%\sysprep\sysprep.inf (CALL :ColorLine "%E%31m%vSystemRoot%\sysprep\sysprep.inf%E%97m")
if exist %vSystemRoot%\sysprep.inf (CALL :ColorLine "%E%31m%vSystemRoot%\sysprep.inf%E%97m")
if exist %vSystemRoot%\Panther\Unattended.xml (CALL :ColorLine "%E%31m%vSystemRoot%\Panther\Unattended.xml%E%97m")
if exist %vSystemRoot%\Panther\Unattend.xml (CALL :ColorLine "%E%31m%vSystemRoot%\Panther\Unattend.xml%E%97m")
if exist %vSystemRoot%\Panther\Unattend\Unattend.xml (CALL :ColorLine "%E%31m%vSystemRoot%\Panther\Unattend\Unattend.xml%E%97m")
if exist %vSystemRoot%\Panther\Unattend\Unattended.xml (CALL :ColorLine "%E%31m%vSystemRoot%\Panther\Unattend\Unattended.xml%E%97m")
if exist %vSystemRoot%\System32\Sysprep\unattend.xml (CALL :ColorLine "%E%31m%vSystemRoot%\System32\Sysprep\unattend.xml%E%97m")
if exist %vSystemRoot%\System32\Sysprep\unattended.xml (CALL :ColorLine "%E%31m%vSystemRoot%\System32\Sysprep\unattended.xml%E%97m")
if exist C:\unattend.txt (CALL :ColorLine "%E%31mC:\unattend.txt%E%97m")
if exist C:\unattend.inf (CALL :ColorLine "%E%31mC:\unattend.inf%E%97m")
echo.


CALL :ColorLine "   %E%33m[+] SAM/SYSTEM files%E%97m"
if exist %vSystemRoot%\repair\SAM (CALL :ColorLine "%E%31m%vSystemRoot%\repair\SAM%E%97m")
if exist %vSystemRoot%\System32\config\RegBack\SAM (CALL :ColorLine "%E%31m%vSystemRoot%\System32\config\RegBack\SAM%E%97m")
if exist %vSystemRoot%\System32\config\SAM (CALL :ColorLine "%E%31m%vSystemRoot%\System32\config\SAM%E%97m")
if exist %vSystemRoot%\repair\system (CALL :ColorLine "%E%31m%vSystemRoot%\repair\system%E%97m")
if exist %vSystemRoot%\System32\config\SYSTEM (CALL :ColorLine "%E%31m%vSystemRoot%\System32\config\SYSTEM%E%97m")
if exist %vSystemRoot%\System32\config\RegBack\system (CALL :ColorLine "%E%31m%vSystemRoot%\System32\config\RegBack\system%E%97m")
echo.


CALL :ColorLine "   %E%33m[+] Cloud Credentials%E%97m"
if exist %userprofile%\.aws\credentials (CALL :ColorLine "%E%31m%userprofile%\.aws\credentials%E%97m")
if exist %userprofile%\AppData\Roaming\gcloud\credentials.db (CALL :ColorLine "%E%31m%userprofile%\AppData\Roaming\gcloud\credentials.db%E%97m")
if exist %userprofile%\AppData\Roaming\gcloud\legacy_credentials (CALL :ColorLine "%E%31m%userprofile%\AppData\Roaming\gcloud\legacy_credentials%E%97m")
if exist %userprofile%\AppData\Roaming\gcloud\access_tokens.db (CALL :ColorLine "%E%31m%userprofile%\AppData\Roaming\gcloud\access_tokens.db%E%97m")
if exist %userprofile%\.azure\accessTokens.json (CALL :ColorLine "%E%31m%userprofile%\.azure\accessTokens.json%E%97m")
if exist %userprofile%\.azure\azureProfile.json (CALL :ColorLine "%E%31m%userprofile%\.azure\azureProfile.json%E%97m")
echo.

CALL :ColorLine "   %E%33m[+] possible files containing credentials%E%97m"
dir /s/b /A:-D RDCMan.settings == *.rdg == *_history* == httpd.conf == .htpasswd == .gitconfig == .git-credentials == Dockerfile == docker-compose.yml == access_tokens.db == accessTokens.json == azureProfile.json == appcmd.exe == scclient.exe == *.gpg$ == *.pgp$ == *config*.php == elasticsearch.y*ml == kibana.y*ml == *.p12$ == *.cer$ == known_hosts == *id_rsa* == *id_dsa* == *.ovpn == tomcat-users.xml == web.config == *.kdbx == KeePass.config == Ntds.dit == SAM == SYSTEM == security == software == FreeSSHDservice.ini == sysprep.inf == sysprep.xml == *vnc*.ini == *vnc*.c*nf* == *vnc*.txt == *vnc*.xml == php.ini == https.conf == https-xampp.conf == my.ini == my.cnf == access.log == error.log == server.xml == ConsoleHost_history.txt == pagefile.sys == NetSetup.log == iis6.log == AppEvent.Evt == SecEvent.Evt == default.sav == security.sav == software.sav == system.sav == ntuser.dat == index.dat == bash.exe == wsl.exe 2>nul | findstr /v ".dll"
echo.



@REM registy
echo.
CALL :ColorLine "%E%33m[+] REGISTRY%E%97m"
@REM @REM # 2****1 Try to write every service with its current content (to check if you have write permissions)
CALL :ColorLine "   %E%33m[+] Try to write every service with its current content (to check if you have write permissions%E%97m"
(for /f %%a in ('reg query hklm\system\currentcontrolset\services') do (del %%temp%%\reg.hiv 2>nul & reg save %%a %%temp%%\reg.hiv 2>nul && reg restore %%a %%temp%%\reg.hiv 2>nul && echo You can modify %%a)) 
echo.


@REM # **** try to write a registry key to each service
CALL :ColorLine "   %E%33m[+] try to write a registry key to each service%E%97m"
for /f %%a in ('reg query hklm\system\currentcontrolset\services') do (reg add %%a /v testing99393 /t REG_EXPAND_SZ /d c:\temp\x.exe /f 2>nul 1>nul && reg delete %%a /v testing99393 /f 2>nul 1>nul && echo You can modify %%a)
echo.




echo.
CALL :ColorLine "%E%33m[+] STARTUP%E%97m"
CALL :ColorLine "   %E%33m[+] Auto Starts%E%97m"
for /f "tokens=2" %%n in ('sc query state^= all^| findstr SERVICE_NAME') do (
    for /f "delims=: tokens=1*" %%r in ('sc qc "%%~n" ^| findstr BINARY_PATH_NAME ^| findstr /i /v /l /c:"c:\windows\system32" ^| findstr /v /c:""""') do (
        echo %%~s | findstr /r /c:"[a-Z][ ][a-Z]" >nul 2>&1 && (echo %%n && echo %%~s && icacls %%s | findstr /i "(F) (M) (W) :\" | findstr /i ":\\ everyone authenticated users todos %username%") && echo.
    )
)
echo.

CALL :ColorLine "   %E%33m[+] Programs run on startup%E%97m"
wmic startup get caption,command 2>nul 
echo.


CALL :ColorLine "   %E%33m[+] Scheduled Tasks (run as SYSTEM)%E%97m"
@REM powershell -c "Get-ScheduledTask |% { $t = $_; Get-ScheduledTaskInfo -TaskName $_.TaskName -ErrorAction SilentlyContinue| select @{Name='State'; Expression={$t.State}},TaskName,TaskPath,LastRunTime,NextRunTime,@{Name='Actions'; Expression={$t.Actions.execute}},@{Name='Arguments'; Expression={$t.Actions.Arguments}} }"
powershell.exe -exec bypass -enc RwBlAHQALQBTAGMAaABlAGQAdQBsAGUAZABUAGEAcwBrACAAfAAlACAAewAgACQAdAAgAD0AIAAkAF8AOwAgAEcAZQB0AC0AUwBjAGgAZQBkAHUAbABlAGQAVABhAHMAawBJAG4AZgBvACAALQBUAGEAcwBrAE4AYQBtAGUAIAAkAF8ALgBUAGEAcwBrAE4AYQBtAGUAIAAtAEUAcgByAG8AcgBBAGMAdABpAG8AbgAgAFMAaQBsAGUAbgB0AGwAeQBDAG8AbgB0AGkAbgB1AGUAfAAgAHMAZQBsAGUAYwB0ACAAQAB7AE4AYQBtAGUAPQAnAFMAdABhAHQAZQAnADsAIABFAHgAcAByAGUAcwBzAGkAbwBuAD0AewAkAHQALgBTAHQAYQB0AGUAfQB9ACwAVABhAHMAawBOAGEAbQBlACwAVABhAHMAawBQAGEAdABoACwATABhAHMAdABSAHUAbgBUAGkAbQBlACwATgBlAHgAdABSAHUAbgBUAGkAbQBlACwAQAB7AE4AYQBtAGUAPQAnAEEAYwB0AGkAbwBuAHMAJwA7ACAARQB4AHAAcgBlAHMAcwBpAG8AbgA9AHsAJAB0AC4AQQBjAHQAaQBvAG4AcwAuAGUAeABlAGMAdQB0AGUAfQB9ACwAQAB7AE4AYQBtAGUAPQAnAEEAcgBnAHUAbQBlAG4AdABzACcAOwAgAEUAeABwAHIAZQBzAHMAaQBvAG4APQB7ACQAdAAuAEEAYwB0AGkAbwBuAHMALgBBAHIAZwB1AG0AZQBuAHQAcwB9AH0AIAB9AA==
echo.


CALL :ColorLine "   %E%33m[+] can write to PATH%E%97m"
for %%A in ("%%path:;=";"%%") do ( cmd.exe /c icacls "%%~A" 2>nul | findstr /i "(F) (M) (W) :\" | findstr /i ":\\ everyone authenticated users todos %%username%%" && echo. )
echo.



echo.
CALL :ColorLine "%E%33m[+] OTHER%E%97m"
CALL :ColorLine "   %E%33m[+] Always install elevated (no error = vulnerable)%E%97m"
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated && reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated |findstr ERROR
echo.









echo.
CALL :ColorLine "%E%33m[+] NOTES%E%97m"
echo - Don't forget to run systeminfo through Windows Exploit Suggester







:::-Subroutines

:SetOnce
REM :: ANSI escape character is set once below - for ColorLine Subroutine
SET "E=0x1B["
SET "PercentageTrack=0"
EXIT /B

:T_Progress
SET "Percentage=%~1"
SET /A "PercentageTrack=PercentageTrack+Percentage"
TITLE WinPEAS - Windows local Privilege Escalation Awesome Script - Scanning... !PercentageTrack!%%
EXIT /B

:ColorLine
SET "CurrentLine=%~1"
FOR /F "delims=" %%A IN ('FORFILES.EXE /P %~dp0 /M %~nx0 /C "CMD /C ECHO.!CurrentLine!"') DO ECHO.%%A
EXIT /B


@REM CALL :Trim return_val %val%
:Trim
SetLocal EnableDelayedExpansion
set Params=%*
for /f "tokens=1*" %%a in ("!Params!") do EndLocal & set %1=%%b
exit /b
