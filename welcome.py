import os
from typing import Iterator

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
SECRET_FILE_NAME = "secret.json"
TARGET_TAG = "itubeteam"


def request_credentials() -> Credentials:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        SECRET_FILE_NAME,
        SCOPES,
    )
    return flow.run_console()


def build_api(credentials: Credentials) -> Resource:
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


def get_uploads_playlist_id(api: Resource) -> str:
    response = (
        api.channels()
        .list(part="snippet,contentDetails,statistics", mine=True)
        .execute()
    )
    item = response["items"][0]
    return item["contentDetails"]["relatedPlaylists"]["uploads"]


def get_videos_ids_by_playlist(api: Resource, playlist_id: str) -> Iterator[list]:
    next_page = None
    while True:
        response = (
            api.playlistItems()
            .list(
                part="snippet,contentDetails,id,status",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page,
            )
            .execute()
        )
        video_ids = [x["snippet"]["resourceId"]["videoId"] for x in response["items"]]
        yield video_ids

        next_page = response.get("nextPageToken")
        if not next_page:
            return


def update_video_tags(api: Resource, video: dict) -> None:
    tags = video["snippet"].get("tags", [])
    if TARGET_TAG in tags:
        return

    tags.append(TARGET_TAG)
    body = {
        "id": video["id"],
        "snippet": {
            "title": video["snippet"]["title"],
            "categoryId": video["snippet"]["categoryId"],
            "tags": tags,
        },
    }
    # TODO: check response
    api.videos().update(part="snippet", body=body).execute()


def get_extended_videos(api: Resource, videos_ids: list) -> list:
    response = api.videos().list(part="snippet", id=",".join(videos_ids)).execute()
    return response["items"]


def main():
    credentials = request_credentials()
    api = build_api(credentials)

    channel_upload_playlist_id = get_uploads_playlist_id(api)
    for videos_ids in get_videos_ids_by_playlist(api, channel_upload_playlist_id):
        for video in get_extended_videos(api, videos_ids):
            update_video_tags(api, video)


if __name__ == "__main__":
    main()
