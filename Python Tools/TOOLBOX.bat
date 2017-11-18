ECHO OFF
:MENU
CLS
ECHO.
ECHO ...............................................
ECHO          PYTHON PEN TOOLBOX v1.0
ECHO PRESS 1, 2 OR 3 to select your task, or 4 to EXIT.
ECHO ...............................................
ECHO.
ECHO 1 - Open PSCAN
ECHO 2 - TOOL 2
ECHO 3 - TOOL 3
ECHO 4 - EXIT
ECHO
SET /P M=Type 1, 2, 3, or 4 then press ENTER:
IF %M%==1 GOTO PSCAN
IF %M%==2 GOTO TOOL2
IF %M%==3 GOTO TOOL3
IF %M%==4 GOTO EOF
:PSCAN
cd %cd%\TOOLS\
start python PSCAN.py
GOTO MENU
:CALC
cd %windir%\system32\calc.exe
start calc.exe
GOTO MENU
:BOTH
cd %windir%\system32\notepad.exe
start notepad.exe
cd %windir%\system32\calc.exe
start calc.exe
GOTO MENU