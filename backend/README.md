# AutoChef AI Backend

This directory contains the FastAPI backend for AutoChef AI.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    *   Copy `.env.example` to a new file named `.env`.
    *   Fill in the required API keys and client secrets in `.env`.
    ```bash
    cp .env.example .env
    # Now edit .env with your credentials
    ```

4.  **Place `client_secret.json`:**
    *   Ensure your Google OAuth `client_secret.json` file (for Google Drive and/or YouTube API access) is placed in this `backend` directory. This file is used by `google-auth-oauthlib` for the initial OAuth flow.

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Project Structure

*   `main.py`: FastAPI application entry point.
*   `routes/`: API endpoint definitions.
*   `services/`: Business logic and interactions with external APIs (Google Drive, Gemini, YouTube) and video editing tools.
*   `utils/`: Utility functions, e.g., for FFmpeg.
*   `.env`: Environment variables (ignored by Git).
*   `requirements.txt`: Python dependencies.
*   `client_secret.json`: Google OAuth client secrets (ignored by Git).
