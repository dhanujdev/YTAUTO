import os
import subprocess
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload # Added this import

def download_clip(file_id, filename, service):
    request = service.files().get_media(fileId=file_id)
    # Ensure the directory for the filename exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
    print(f"Downloaded {filename}") # Added print statement for feedback

def merge_clips(recipe: str, clips: list[str]):
    tmp_recipe_dir = os.path.join("tmp", recipe)
    os.makedirs(tmp_recipe_dir, exist_ok=True)
    
    print(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID')[:5]}...") # Debug print
    creds = Credentials.from_authorized_user_info({
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
        "token_uri": "https://oauth2.googleapis.com/token"
    }, scopes=["https://www.googleapis.com/auth/drive.readonly"])
    
    service = build("drive", "v3", credentials=creds)

    file_list_for_ffmpeg = []
    # Ensure GOOGLE_FOLDER_ID is available for searching within the correct recipe folder if needed
    # For now, assuming clip names are unique enough or are searched globally if not found in a specific recipe subfolder.
    # If clips are inside the recipe folder on Drive, the query would need to be more specific.

    for clip_name in clips:
        print(f"Searching for clip: {clip_name}")
        # Query might need to be more specific, e.g., search within the parent recipe folder ID
        # For simplicity, assuming clip names are globally unique for now as per current query
        query = f"name='{clip_name}' and mimeType contains 'video'"
        # If you have a parent folder ID for the recipe on Drive:
        # parent_folder_id = get_folder_id_for_recipe(recipe, service) # You'd need this helper
        # query = f"name='{clip_name}' and '{parent_folder_id}' in parents and mimeType contains 'video'"
        
        results = service.files().list(q=query, fields="files(id, name)", pageSize=1).execute()
        files_found = results.get("files", [])
        
        if not files_found:
            print(f"Error: Clip '{clip_name}' not found on Google Drive.")
            # Decide how to handle: raise error, skip clip, etc.
            # For now, let's raise an exception if a clip isn't found.
            raise FileNotFoundError(f"Clip '{clip_name}' not found on Google Drive.")
            
        file_id = files_found[0]["id"]
        # Use absolute paths or ensure correct relative paths for ffmpeg
        local_path = os.path.join(tmp_recipe_dir, clip_name)
        
        print(f"Downloading {clip_name} (ID: {file_id}) to {local_path}")
        download_clip(file_id, local_path, service)
        # FFmpeg requires paths to be escaped or handled carefully if they contain special characters.
        # Using 'file' keyword for concat demuxer expects paths relative to the input.txt file, or absolute paths.
        # For simplicity, we are making local_path relative to the cwd where ffmpeg runs, or absolute.
        # The `input.txt` will be in `tmp_recipe_dir`, so paths in it should be just the filenames.
        file_list_for_ffmpeg.append(f"file '{os.path.basename(local_path)}'")

    input_txt_path = os.path.join(tmp_recipe_dir, "input.txt")
    with open(input_txt_path, "w") as f:
        f.write("\n".join(file_list_for_ffmpeg))
    print(f"Created ffmpeg input file: {input_txt_path}")

    # Output file will also be in the tmp_recipe_dir
    output_file = os.path.join(tmp_recipe_dir, f"{recipe}_merged.mp4")
    # Ensure output_file is cleaned up if it exists to prevent ffmpeg error
    if os.path.exists(output_file):
        os.remove(output_file)

    cmd = [
        "ffmpeg", 
        "-f", "concat", 
        "-safe", "0", # Be cautious with -safe 0 if paths are not controlled
        "-i", input_txt_path, 
        "-c", "copy", 
        output_file
    ]
    print(f"Running FFmpeg command: {' '.join(cmd)}")
    
    # Run FFmpeg from the tmp_recipe_dir so that file paths in input.txt are resolved correctly
    process_result = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=tmp_recipe_dir)
    
    if process_result.returncode != 0:
        print("FFmpeg Error:")
        print("STDOUT:", process_result.stdout)
        print("STDERR:", process_result.stderr)
        raise Exception(f"FFmpeg failed to merge videos. Error: {process_result.stderr}")
    
    print(f"FFmpeg successful. Merged video: {output_file}")
    # The path returned should ideally be accessible by the user, 
    # e.g. a URL if serving statically, or just the path for now.
    return output_file # This path is relative to the server's file system
