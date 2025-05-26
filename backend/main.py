\
from fastapi import FastAPI

app = FastAPI(title=\"AutoChef AI Backend\")

# Placeholder for importing routers
# from routes import drive, process, youtube, gemini

# app.include_router(drive.router, prefix=\"/drive\", tags=[\"Google Drive\"])
# app.include_router(process.router, prefix=\"/process\", tags=[\"Video Processing\"])
# app.include_router(youtube.router, prefix=\"/youtube\", tags=[\"YouTube\"])
# app.include_router(gemini.router, prefix=\"/gemini\", tags=[\"Gemini AI\"])

@app.get(\"/\", tags=[\"Root\"])
async def read_root():
    return {\"message\": \"Welcome to AutoChef AI Backend!\"}

# To run this app (from the 'backend' directory):
# uvicorn main:app --reload
