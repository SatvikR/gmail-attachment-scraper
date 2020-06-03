# gmail-attachment-scraper
A gmail attachment scraper built using the google gmail api with python.

Functionality: <br>
Given a target email address and path, this script will download all attachments from the unread emails from the given email into the path.
<br>

# How to use
1. Go to https://developers.google.com/gmail/api/quickstart/python, click Enable the Gmail API.
3. Run pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib (use pip3 if this doesn't work)
2. Click DOWNLOAD CLIENT CONFIGURATION and save the file credentials.json to the folder that you downloaded this repo.
3. Run setup.py
4. Run main.py. If the OATH tells you that the script is unsafe, (which it isn't), click advanced, and there should be an option to trust the app.
5. The next time you run main.py, you will not get the OAUTH prompt
6. Run setup.py again if you want to change the path or the target email adress