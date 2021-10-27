@ECHO OFF
TITLE Frontend Console
COLOR 9
echo.

echo If you wish to exit, it would be nice of you to press 'CTRL + C'
echo You can also use 'CTRL + C' to reboot the server and entering 'N'.
echo.

virtualenv venv
cd .\frontend
uvicorn main:app --reload --port 8080
goto:run
