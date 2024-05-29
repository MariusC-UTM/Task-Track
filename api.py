import dropbox
import os
from scraper import dropbox_pre_auth, dropbox_post_auth


def read_dropbox_token():
    token_file_path = os.path.join('user data', 'private', 'dropbox_api_token.txt')
    with open(token_file_path, 'r') as file:
        return file.read().strip()


def dropbox_token_status():  # Not implemented yet
    # 1:
    # check if the dropbox token file 'dropbox_api_token.txt' exists in the 'user data\private' folder

    # 1.1:
    # if yes then check if the token is valid by going to step # 2
    # i.2:
    # if not then create the folder and the file, go to step # 3

    # 2:
    DROPBOX_ACCESS_TOKEN = read_dropbox_token()
    # check for AuthError
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)  # ?
    # 2.1:
    # if no AuthError return succes ?
    # 2.2:
    # else auth and scrap by going to step # 3 ?

    # 3:
    dropbox_pre_auth()
    # ?
    dropbox_post_auth()
    # ?

    # 4:
    # write the token to the 'dropbox_api_token.txt' file


def save_to_dropbox():  # Not finished
    if dropbox_token_status() == 'fail':  # ?
        print('You must manually authenticate and let the program grab your token.')
        return

    DROPBOX_ACCESS_TOKEN = read_dropbox_token()
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'rb') as f:
        dbx.files_upload(f.read(), '/tasks.db', mode=dropbox.files.WriteMode.overwrite)
    print("Database saved to Dropbox")


def download_from_dropbox():  # Not finished
    if dropbox_token_status() == 'fail':  # ?
        print('You must manually authenticate and let the program grab your token.')
        return

    DROPBOX_ACCESS_TOKEN = read_dropbox_token()
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'wb') as f:
        metadata, res = dbx.files_download(path='/tasks.db')
        f.write(res.content)
    print("Database downloaded from Dropbox")
