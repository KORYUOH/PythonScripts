@echo off
setlocal
set DIRECTORY_PATH=%~dp0
for %%i in ("%DIRECTORY_PATH:~0,-1%") do set THIS_DIRECTORY=%%~ni
title Convert to %THIS_DIRECTORY%
python conv.py
endlocal
exit
