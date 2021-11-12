# --------------------------------------------------------------------------------------------IMPORTS
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# --------------------------------------------------------------------------------------------DEPENDENCIES
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

app.mount("/static", StaticFiles(directory="../static"), name="static")

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------------------------ROUTES

class bovenbalk:
    def __init__(self, href, caption):
        self.href = href
        self.caption = caption


bovenbalk = [bovenbalk('http://localhost:8080/item/', 'Inloggen'), bovenbalk('base.html', 'Logo')]


@app.get("/", response_class=HTMLResponse)
async def inlogcontent(request: Request):
    return templates.TemplateResponse("include/inlogcontent.html", {"request": request, "bovenBalk": bovenbalk})


@app.get("/item/", response_class=HTMLResponse)
async def item(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "bovenbalk": bovenbalk})


@app.get("/test/", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("include/bovenbalk.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("fhome.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("flogin.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8080)
