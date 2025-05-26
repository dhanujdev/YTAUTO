from fastapi import FastAPI
from drive_utils import get_recipe_folders

app = FastAPI()

@app.get("/")
def root():
    return {"status": "AutoChef API is running."}

@app.get("/fetch_clips")
def fetch_clips():
    return {"recipes": get_recipe_folders()}
