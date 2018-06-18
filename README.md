# gmail-api-python3
You can easy to use Gmail API by python3. This module support multi bite language. It works even *Japanese, Chinese and Hangul*. 

## Prepare Gmail API
1. Turn on the Gmail API
1. Use this wizard to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
On the Add credentials to your project page, click the Cancel button.
1. At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
1. Select the Credentials tab, click the Create credentials button and select OAuth client ID.
1. Select the application type Other, enter the name "Gmail API Quickstart", and click the Create button.
1. Click OK to dismiss the resulting dialog.
1. Click the file_download (Download JSON) button to the right of the client ID.
1. Move this file to your working directory and rename it client_secret.json.

This is [document](https://developers.google.com/gmail/api/quickstart/python) about gmail api for python.

## Install
    git clone https://github.com/sleepless-se/gmail-api-python3.git
    
    pip install --upgrade google-api-python-client
    or
    pip install -r ./gmail-api-python3/requirements.txt

## Setting
You need set json_path to your client_secret.json.

```ruby:kobito.rb
json_path = './your/client_secret.json'
```

## Run

    python3 sample.py

You can select your gmail account.

`credentials.json` was created in gmail-api-python3 after login.

When you want to change gmail account. You need delete `credentials.json`
