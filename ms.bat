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
set defaultpath="K:\Comic\used"
set secondpath="K:\Comic"

if "%2" EQU "used" set defaultpath="K:\Comic\used"
if "%2" EQU "used" set secondpath=
if "%2" EQU "comic" set defaultpath="K:\Comic"
if "%2" EQU "comic" set secondpath=


py "C:\Path\migemo_search.py" "%Word%" %defaultpath% %secondpath%
goto Finish

:ErrWord
echo.
echo Request Search Word
goto Finish

:Help
echo. %~nx0 ^<searchword^> ^[used comic^]

:Finish
endlocal
