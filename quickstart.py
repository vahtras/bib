import os.path
import pathlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gdown

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
# MYLIB = os.environ["MYLIB"]
MYLIB = "/tmp"


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name, size)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return items
        print("Files:")
        outdir = pathlib.Path(MYLIB) / "My Library"
        if not outdir.is_dir():
            outdir.mkdir()
        for item in items:
            if item["name"] in ["mylibrary.db", "MyLibraryImages.txt"]:
                print(f"{item['name']} ({item['id']})")
                gdown.download(id=item["id"], output=str(outdir / item["name"]))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")

    return items


if __name__ == "__main__":
    main()
