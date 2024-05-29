import dropbox
import os
import time
from scraper import dropbox_pre_auth, dropbox_post_auth


def dropbox_token_status():
    token_file_path = os.path.join('user data', 'private', 'dropbox_api_token.txt')

    # Step 1: Check if the Dropbox token file exists
    if os.path.exists(token_file_path):
        try:
            # Step 2: Get the existing token from the file
            DROPBOX_ACCESS_TOKEN = read_dropbox_token()

            # Check if the token is valid
            dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
            dbx.users_get_current_account()

            # If no AuthError is raised, return success
            return True

        except dropbox.exceptions.AuthError:
            # If AuthError is raised, go to step 3
            pass
    else:
        # If the token file does not exist, ensure the directory is created
        os.makedirs(os.path.dirname(token_file_path), exist_ok=True)

    # Step 3: Perform authentication
    dropbox_pre_auth()
    new_token = dropbox_post_auth()

    # Step 4: Write the new token to the 'dropbox_api_token.txt' file
    with open(token_file_path, 'w') as file:
        file.write(new_token.strip())

    return True


def read_dropbox_token():
    token_file_path = os.path.join('user data', 'private', 'dropbox_api_token.txt')
    with open(token_file_path, 'r') as file:
        return file.read().strip()


def upload_to_dropbox():  # Not finished
    if dropbox_token_status() == 'fail':  # ?
        print('You must manually authenticate and let the program grab your token.')
        return

    DROPBOX_ACCESS_TOKEN = read_dropbox_token()
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'rb') as f:
        dbx.files_upload(f.read(), '/tasks.db', mode=dropbox.files.WriteMode.overwrite)
    print("Database uploaded to Dropbox")


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
