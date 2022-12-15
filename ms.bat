@echo off 
setlocal
set Word=%1

if "%1" EQU "/help" goto :Help
if "%1" EQU "-help" goto :Help
if "%1" EQU "/?" goto :Help
if "%1" EQU "-h" goto :Help
if "%1" EQU "--help" goto :Help

if "%1" EQU "" set /p Word=Search? ^>
if "%Word%" EQU "" goto :ErrWord
set default_yaml=default.yaml
set yaml_path=%default_yaml%

if "%2" EQU "used" set yaml_path=used.yaml
if "%2" EQU "comic" set yaml_path=comic.yaml
if "%2" NEQ "" set yaml_path=%2


py "C:\Path\migemo_search.py" "%Word%" %~dp0%yaml_path%
goto Finish

:ErrWord
echo.
echo Request Search Word
goto Finish

:Help
echo. %~nx0 ^<searchword^> ^[used comic^]

:Finish
endlocal
