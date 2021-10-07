#--------------------------------------------------------------------------------------------IMPORTS
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

#--------------------------------------------------------------------------------------------DEPENDENCIES
app = FastAPI()
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")
#--------------------------------------------------------------------------------------------ROUTES

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        1: {
            "link": "google.com",
            "text": "Link to Google"
        },
        2: {
            "link": "bing.com",
            "text": "Link to Bing"
        }
    }
    return templates.TemplateResponse("homepage.html", {"request": request, "data": data})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


