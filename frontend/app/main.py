#--------------------------------------------------------------------------------------------IMPORTS
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

#--------------------------------------------------------------------------------------------DEPENDENCIES
app = FastAPI()
templates = Jinja2Templates(directory="templates")
#--------------------------------------------------------------------------------------------ROUTES

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})