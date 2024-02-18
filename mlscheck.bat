@echo off
setlocal
set mls=%1
if "%mls%" EQU "" set /p mls=MlsPath? ^>
if not exist "%mls%" goto NOTFOUND
goto Check
:NOTFOUND
echo file %mls% is not found
pause
goto EOF

:Check
python mlsCheck.py --folder "%CD%" --mls "%mls%"
:EOF
endlocal
