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
        
        
# In this script, video_file is the path to the final video file, and credentials.json is the path to the Google API Console project credentials file. The video's title, description, tags, and category ID are specified in the body parameter of the youtube.videos().insert() method. The privacy status is set to "public", meaning that the video will be visible to anyone.

# Note that uploading a video to YouTube using the API can take a long time, especially for large video files. You should be prepared to handle timeouts and retry the upload if necessary. You may also want to consider using a service account for authentication, as opposed to an authorized user, to avoid the need for manual authentication.
