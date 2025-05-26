from fastapi import APIRouter, Request
from ..services.video_editor import merge_clips # Adjusted for relative import

router = APIRouter()

@router.post("/merge_video")
async def merge_video(data: Request):
    body = await data.json()
    recipe = body.get("recipe")
    clips = body.get("files")
    # Assuming merge_clips is not async, if it becomes async, add await here
    output_path = merge_clips(recipe, clips) 
    return {"merged_video": output_path}