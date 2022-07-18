@echo off
setlocal

set COPYFILE=conv.bat
set COPYFILE2=conv.py
set SELF=%0
set SELFCOPY=1

for /d  %%A In (*) do call :COPYEXEC "%%A"

exit /b
:COPYEXEC
Copy to %1
copy /Y %COPYFILE% %1
copy /Y %COPYFILE2% %1
if %SELFCOPY% EQU 1 copy /Y %SELF% %1
pushd %1
echo %CD%
start %COPYFILE%
popd
exit /b

endlocal
