@ECHO OFF
TITLE Backend Console
COLOR A
echo.

echo If you wish to exit, it would be nice of you to press 'CTRL + C'
echo You can also use 'CTRL + C' to reboot the server and entering 'N'.
echo.
pause
venv\scripts\activate.bat
pause
cd .\backend\app
:run
python main.py
goto:run