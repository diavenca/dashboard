from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import mimetypes

def guardar_drive(file):
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('drive', 'v3', credentials=creds)

        name=file.name
        mime_type = mimetypes.guess_type(file)

        file_metadata = {'name': name}
        media = MediaFileUpload(file,
                                mimetype=mime_type)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')
