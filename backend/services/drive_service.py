import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_drive_service():
    creds = Credentials.from_authorized_user_info(
        info={
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
            "token_uri": "https://oauth2.googleapis.com/token"
        },
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=creds)

def list_recipe_folders():
    folder_id = os.getenv("GOOGLE_FOLDER_ID")
    service = get_drive_service()

    # Get subfolders (recipes)
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    folders = service.files().list(q=query, fields="files(id, name)").execute().get("files", [])

    results = {}
    for folder in folders:
        subquery = f"'{folder['id']}' in parents and mimeType contains 'video'"
        clips = service.files().list(q=subquery, fields="files(name)").execute().get("files", [])
        sorted_clips = sorted([f["name"] for f in clips])
        results[folder["name"]] = sorted_clips

    return results