ECHO OFF
ECHO Welcome. This promt will try to install all needed packages.
echo
echo If you don't wish to continue, press 'CRTL + C'
PAUSE
:: Check for Python Installation
python --version 2>NUL
if errorlevel 1 goto errorNoPython

ECHO Python is installed!
PAUSE

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:afterPython

:errorNoPython
echo Error: Python not installed.
echo Please install python3.9.0
PAUSE
goto:eof

:afterPython

:: Check for Pip Installation
pip3 --version
if errorlevel 1 goto errorNoPip3

echo Pip3 is installed!
PAUSE
goto:afterPip

:errorNoPip3
echo Error: Pip3 not installed.
echo Please install pip3.
PAUSE
goto:eof

:afterPip

echo Now we are ready to begin the installation and setup an evironment for you. :D
PAUSE
echo INSTALLING VIRTUAL ENVIRONMENT
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
echo INSTALLING ALL DEPENDENCIES
pip3 install -r backend\app\requirements.txt

if errorlevel 1 goto otherError
goto:lastPart

:otherError
echo uhh... there seems to be an error :c please contact an administrator.
PAUSE

goto:eof
:lastPart
echo Finished installing

PAUSE