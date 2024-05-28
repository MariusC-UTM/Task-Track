import dropbox
import os
from scraper import dropbox_pre_auth, dropbox_post_auth


def read_dropbox_token():
    token_file_path = os.path.join('private user data', 'dropbox_api_token.txt')
    with open(token_file_path, 'r') as file:
        return file.read().strip()


def save_to_dropbox():
    DROPBOX_ACCESS_TOKEN = read_dropbox_token()
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'rb') as f:
        dbx.files_upload(f.read(), '/tasks.db', mode=dropbox.files.WriteMode.overwrite)
    print("Database saved to Dropbox")


def download_from_dropbox():
    DROPBOX_ACCESS_TOKEN = read_dropbox_token()
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'wb') as f:
        metadata, res = dbx.files_download(path='/tasks.db')
        f.write(res.content)
    print("Database downloaded from Dropbox")
