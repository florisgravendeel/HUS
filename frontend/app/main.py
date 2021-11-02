#--------------------------------------------------------------------------------------------IMPORTS
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

#--------------------------------------------------------------------------------------------DEPENDENCIES
app = FastAPI()
templates = Jinja2Templates(directory="../templates")

app.mount("/static", StaticFiles(directory="../static"), name="static")
#--------------------------------------------------------------------------------------------ROUTES

class bovenBalk:
    def __init__(self, href, caption):
        self.href = href
        self.caption = caption

bovenBalk = [bovenBalk('http://localhost:8080/item/', 'Inloggen'), bovenBalk('base.html', 'Logo')]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("include/inlogContent.html", {"request": request, "bovenBalk":bovenBalk})


@app.get("/item/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "bovenBalk":bovenBalk})


@app.get("/test/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("bovenBalk.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)