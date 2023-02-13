from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def upload_to_youtube(video_file):
    credentials = Credentials.from_authorized_user_file("path/to/credentials.json")
    youtube = build("youtube", "v3", credentials=credentials)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": "Famous Person's Video",
                    "description": "A video of a famous person answering interesting questions",
                    "tags": [
                        "famous person",
                        "interview",
                        "questions",
                        "answers"
                    ],
                    "categoryId": 22
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=video_file
        )
        response = request.execute()
        print(f"Video was uploaded successfully with ID: {response['id']}")
    except HttpError as error:
        print(f"An error occurred while uploading the video: {error}")
