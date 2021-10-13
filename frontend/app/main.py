#--------------------------------------------------------------------------------------------IMPORTS
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#--------------------------------------------------------------------------------------------DEPENDENCIES
app = FastAPI()
templates = Jinja2Templates(directory="../templates")

app.mount("/static", StaticFiles(directory="../static"), name="static")
#--------------------------------------------------------------------------------------------ROUTES

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
