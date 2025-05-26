from fastapi import FastAPI
from routes import drive

app = FastAPI()

app.include_router(drive.router)