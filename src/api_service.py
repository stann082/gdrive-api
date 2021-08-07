from __future__ import print_function

import io
import os.path

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from pathlib import Path
from src.options import Options

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

    def get_files(self, options):
        kwargs = self.__build_args(options)
        results = self.service.files().list(**kwargs).execute()
        files = results['files']

        while "nextPageToken" in results:
            results = self.service.files().list(**kwargs,
                                                pageToken=results['nextPageToken']).execute()
            files.extend(results['files'])

        if options.order_by_size:
            return sorted(files, key=lambda x: int(x['size']) if 'size' in x else 0, reverse=options.is_descending)

        return files

    # region Helper Methods

    def __build_args(self, options):
        args = {}

        if options.query is not None:
            args['q'] = f"{options.filter_by}='{options.query}'"
        if not options.order_by_size and options.order_by is not None:
            args['orderBy'] = options.order_by
        if options.total is not None:
            args['pageSize'] = options.total
        if options.fields is not None:
            args['fields'] = options.fields
            if options.fetch_all_files:
                args['fields'] = f"nextPageToken, {options.fields}"
                args['pageSize'] = '100'

        return args
