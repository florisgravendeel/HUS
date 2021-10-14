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

class customer:
    def __init__(self, href, caption):
        self.href = href
        self.caption = caption

boi = [customer('http://localhost:8080/item/', 'the best website'), customer('base.html', 'pagina')]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("include/bovenBalk.html", {"request": request, "customer":boi})


@app.get("/item/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.tml", {"request": request})


@app.get("/test/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("bovenBalk.html", {"request": request})