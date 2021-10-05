@ECHO OFF
TITLE Backend Console
COLOR A
echo.

echo If you wish to exit, it would be nice of you to press 'CRTL + C'
echo.

virtualenv venv
cd .\backend\app
uvicorn main:app --reload --port 8000
