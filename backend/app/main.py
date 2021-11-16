import uvicorn
from datetime import datetime
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.app.routers import login

app = FastAPI()
app.include_router(login.router)

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

if __name__ == '__main__':
    print("UTC Time: ", datetime.utcnow())
    uvicorn.run(app, host="127.0.0.1", port=8000)
