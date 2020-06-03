from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from getdata import ListMessagesMatchingQuery, ListMessagesWithLabels, GetAttachments


def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """
    downloads attachments
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    try:
        targets = read_json('paths.json')
    except json.JSONDecodeError:
        print("Please run setup.py\n")
        exit()

    email = str(targets['target'])
    path = str(targets['path'])

    unread_messages = ListMessagesWithLabels(service, 'me', 'UNREAD')
    target_messages = ListMessagesMatchingQuery(service, 'me', query='from:'+ email + ' is:unread')
    
    for msg in target_messages:
        print(GetAttachments(service, 'me', msg['id'], path))
    
    print("Sucess! \n")

    

if __name__ == '__main__':
    main()