@ECHO OFF
TITLE Backend Console
COLOR A
echo.

echo If you wish to exit, it would be nice of you to press 'CTRL + C'
echo You can also use 'CTRL + C' to reboot the server and entering 'N'.
echo.

virtualenv venv

cd .\backend\app
:run
python main.py
goto:run