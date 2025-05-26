from fastapi import APIRouter
from ..services.drive_service import list_recipe_folders

router = APIRouter()

@router.get("/fetch_clips")
def fetch_clips():
    return {"recipes": list_recipe_folders()}