from __future__ import print_function

import io
import os.path

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from pathlib import Path

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive.file']

CREDS_FILE = 'etc/credentials.json'
TOKEN_FILE = 'etc/token.json'


class ApiService:

    def __init__(self) -> None:
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    def download_file(self, file_name, download_path):
        print(f"Searching for file {file_name}...")
        file = self.__get_file(file_name)
        if file is None:
            print(f"Could not locate {file_name}...")
            return

        download_to = os.path.join(download_path, file_name)
        Path(download_path).mkdir(parents=True, exist_ok=True)

        request = self.service.files().get_media(fileId=file['id'])
        fh = io.FileIO(download_to, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        print(f"Downloaded file {download_to}")

    def get_files(self, items_total):
        items_total = 10 if items_total is None else items_total
        if (items_total == "all"):
            return self.__get_all_files()

        return self.__get_recent_files(items_total)

    def __get_all_files(self):
        results = self.service.files().list(pageSize=500).execute()
        files = results['files']
        while "nextPageToken" in results:
            results = self.service.files().list(
                pageSize=500, pageToken=results['nextPageToken']).execute()
            files.extend(results['files'])
        return files

    def __get_file(self, file_name):
        files = self.__get_all_files()
        file = next(
            (f for f in files if f['name'].startswith(file_name)), None)
        return file

    def __get_recent_files(self, items_total):
        results = self.service.files().list(
            pageSize=items_total, fields="nextPageToken, files(id, name)").execute()
        return results['files']
