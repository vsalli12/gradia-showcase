from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
from getJson import generateInfo

app = FastAPI()
DATA = None

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/api/data")
def get_data():
    global DATA

    if DATA is None:
        DATA = generateInfo()

    return DATA