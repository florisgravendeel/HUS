@ECHO OFF
TITLE Frontend Console
COLOR 9
echo.

echo If you wish to exit, it would be nice of you to press 'CRTL + C'
echo.

virtualenv venv
cd .\frontend
:run
python main.py
pause
goto:run