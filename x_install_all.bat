ECHO OFF
TITLE Install all things.


ECHO Welcome. This promt will try to install all needed packages.
echo
echo If you don't wish to continue, press 'CRTL + C'
echo.

PAUSE
:: Check for Python Installation
echo.
python --version 2>NUL
if errorlevel 1 goto errorNoPython

ECHO Python is installed!
echo.
PAUSE

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:afterPython

:errorNoPython
echo Error: Python not installed.
echo Please install python.
start https://www.python.org/downloads/
echo.
PAUSE
goto:terminate

:afterPython

:: Check for Pip Installation
echo.
pip3 --version
if errorlevel 1 goto errorNoPip3
pip install --upgrade pip --user
echo Pip3 is installed!
echo.
PAUSE
goto:afterPip

:errorNoPip3
echo.
echo Error: Pip3 not installed.
echo Please install pip3.
start https://pypi.org/project/pip/
echo.
PAUSE
goto:terminate

:afterPip

echo.
echo Now we are ready to begin the installation and setup an evironment for you. :D
echo.
PAUSE
echo.
echo INSTALLING VIRTUAL ENVIRONMENT
echo.
pip3 install virtualenv 
if errorlevel 1 goto:END
echo.
PAUSE
virtualenv venv
if errorlevel 1 goto:END
echo.
PAUSE
echo.
echo INSTALLING ALL DEPENDENCIES
echo.
pip3 install -r .\backend\app\requirements.txt --user
pip3 install -r .\frontend\requirements.txt --user
echo.
PAUSE

if errorlevel 1 goto otherError
goto:lastPart

:otherError
echo uhh... there seems to be an error :c please contact an administrator.

SET /P AREYOUSURE=Did you get an error saying somthing about 'Microsoft Visual C++ 14.0 is required... etc' ( Y / N )?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo. 2>c++_error_help_file.txt
echo Welcome, it seems you got this error.>> c++_error_help_file.txt
echo -- Downloaded Microsoft Visual C++ Build Tools from this link: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019>> c++_error_help_file.txt
echo -- Run the installer.>> c++_error_help_file.txt
echo -- Select: Desktop development with C++.>> c++_error_help_file.txt
echo -- Press Install on the bottom right.>> c++_error_help_file.txt
echo A file has been created for you called 'c++_error_help_file'.
echo Maybe there you can find a solution.
echo.
PAUSE

:END
echo.
echo Installation failed.
echo.
PAUSE

goto:eof

:lastPart
echo.
echo Finished installing
echo.
PAUSE


:eof
SET /P AREYOUSURE=Did you get a warning saying something about 'file is not on PATH...' ( Y / N )?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO terminate

echo. 2>PATH_help_file.txt
echo A file has been generated to help with adding a folder to PATH.
echo.

echo If you get a warning that goes something like>> PATH_help_file.txt
echo 'file is not on PATH'>> PATH_help_file.txt
echo you should also get a folder path, which looks like>> PATH_help_file.txt
echo 'C:\folder\names\leading\to\probably\a\scripts\folder'>> PATH_help_file.txt
echo.>> PATH_help_file.txt
echo If you see this warning, please add the given path to you PATH.>> PATH_help_file.txt
echo Here is how to do this: https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho>> PATH_help_file.txt
echo.>> PATH_help_file.txt
echo Go to the Windows Start menu.>> PATH_help_file.txt
echo Select Settings.>> PATH_help_file.txt
echo Select System.>> PATH_help_file.txt
echo Select About.>> PATH_help_file.txt
echo Select Advanced System Settings.>> PATH_help_file.txt
echo Select Environment Variables.>> PATH_help_file.txt
echo Double click on the PATH entry.>> PATH_help_file.txt
echo Add a new location.>> PATH_help_file.txt
echo Paste the folder path you got in the warning earlier.>> PATH_help_file.txt
echo You can now close everything and run the file again.>> PATH_help_file.txt
echo.>> PATH_help_file.txt
PAUSE





:terminate