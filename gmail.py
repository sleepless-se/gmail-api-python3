"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import quopri
from httplib2 import Http
from oauth2client import file, client, tools
import email ,base64
from apiclient.discovery import build
from apiclient import errors
from email.mime.text import MIMEText

auth_url = "https://accounts.google.com/o/oauth2/auth?"

response_setting = {
    "scope": "https://mail.google.com/",
    "response_type": "code",
}


class GmailApi():
    def reconnect(self):
        try:
            self.service = GmailServiceFactory().createService(self.auth_info)
        except errors.HttpError as error:
            pass

    def send_message(self, user, message):
        """send mail. Please check createMesage
            Keyword arguments:
            user -- select "me"
            message -- pass object createMessage
            Returns: None
        """
        try:
            message = (self.service.users().messages().send(userId=user, body=message).execute())
            return message
        except errors.HttpError as error:
            print('An error occurred:s' % error)

    def get_mail_list(self, user, qu):
        ''' Get mail list.
          qu -- filter
           Keyword arguments:
           user -- me or registered address by googleDevloper
           qu -- query
                 Ex) When get mails from example@gmail.com
                "from: example@gmail.com is:unread"
           Returns: mails info list. It's dictionary id and ThreadId
             "messages": [
                  {
                   "id": "nnnnnnnnnnnn",
                   "threadId": "zzzzzzzzzzz"
                  },
                  {
                   "id": "aaaaaa",
                   "threadId": "bbbbbb"
                  },,,,
              }
        '''
        try:
            return self.service.users().messages().list(userId=user, q=qu).execute()
        except errors.HttpError as error:
            self.reconnect()

    def get_mail_content(self, user, i):
        """Get mail by mail ID.
                Keyword arguments:
                user -- select "me"
                i -- mail ID. Get it by getMailList()
                Returns: get mail contents by dictionary
                Detail
                http://developers.google.com/apis-explorer/#p/gmail/v1/gmail.users.messages.get
        """
        try:
            message = self.service.users().messages().get(userId=user, id=i,format='full').execute()
            return message
        except errors.HttpError as error:
            self.reconnect()

    def do_mail_as_read(self, user, i):
        """make mail opened by mail ID
            Keyword arguments:
            user -- select "me"
            i -- mail ID. Get it by getMailList()
            Returns:　None
        """
        query = {"removeLabelIds": ["UNREAD"]}
        self.service.users().messages().modify(userId=user, id=i, body=query).execute()

    def create_message(self, sender, to, subject, message_text):
        """create Message
            Keyword arguments:
            sender -- select "me"
            to -- mail ID. Get it by getMailList()
            subject -- Subject
            message_text --　mail body
            Returns:　None
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def exp_mail_contents(self, user, i, key):
        try:
            content = self.getMailContent(user, i)
            return ([header for header in content["payload"]["headers"] if header["name"] == key])[0]["value"]
        except errors.HttpError as error:
            self.reconnect()

    def get_mail_from(self, user, i):
        try:
            return self.expMailContents(user, i, "From")
        except errors.HttpError as error:
            self.reconnect()

    def get_mail_subject(self, user, i):
        try:
            return self.expMailContents(user, i, "Subject")
        except errors.HttpError as error:
            self.reconnect()

    def __init__(self, auth_info):
        self.auth_info = auth_info
        self.service = GmailServiceFactory().createService(self.auth_info)


class GmailServiceFactory():

    def createService(self, json_path):
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(json_path, SCOPES)
            creds = tools.run_flow(flow, store)
        return build('gmail', 'v1', http=creds.authorize(Http()))


# Call the Gmail API
def get_label(self):
    results = self.service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


def show_chatty_threads(service, user_id='me'):
    threads = service.users().threads().list(userId=user_id).execute().get('threads', [])
    for thread in threads:
        tdata = service.users().threads().get(userId=user_id, id=thread['id']).execute()
        nmsgs = len(tdata['messages'])

        if nmsgs > 0:
            msg = tdata['messages'][0]['payload']
            subject = ''
            for header in msg['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            if subject:  # skip if no Subject line
                print('- %s (%d msgs)' % (subject, nmsgs))
                try:
                    message = service.users().messages().get(userId=user_id, id=thread['id'],format='raw').execute()

                    print ('Message snippet: %s' % message['snippet'])
                    print(message['raw'].encode('ASCII'))
                    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
                    print(msg_str)
                    msg_str = base64.urlsafe_b64decode( msg_str )
                    print(msg_str)
                    msg_str = msg_str.decode('utf-8')
                    print(msg_str)
                    mime_msg = email.message_from_string(msg_str)

                    return mime_msg
                except errors.HttpError as error:
                    print ('An error occurred: %s' % error)

        break

def get_mail_content(self, user, i):
    """get mail by mail ID.
            Keyword arguments:
            user -- select "me"
            i -- mail ID. Get it by getMailList()
            Returns: Get contents by dictionary
            detail
            http://developers.google.com/apis-explorer/#p/gmail/v1/gmail.users.messages.get
    """
    try:
        return self.service.users().messages().get(userId=user, id=i).execute()
    except errors.HttpError as error:
        self.reconnect()



def read_title(content):
    msg = content['payload']
    subject = None
    for header in msg['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
            break
    return subject

def read_from(content):
    text = content['payload']['headers'][21]["value"]
    start_index = text.find("<") + 1
    return text[start_index:-1]

def data_encoder(text)-> str:
    if len(text)>0:
        message = base64.urlsafe_b64decode(text)
        message = str(message, 'utf-8')
    return message

def read_message(content)->str:
    message = None
    if "data" in content['payload']['body']:
        message = content['payload']['body']['data']
        message = data_encoder(message)
    elif "data" in content['payload']['parts'][0]['body']:
        message = content['payload']['parts'][0]['body']['data']
        message = data_encoder(message)
    else:
        print("body has no data.")
        print(content)
    return message

def read_snippet(content)->str:
    message = None
    if content['snippet']:
        message = content['snippet']
    return message
