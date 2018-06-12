"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
import json
import sys
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import email
from apiclient import errors
# # Setup the Gmail API
# SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
# store = file.Storage('credentials.json')
# creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('./client_secret_626154498738-l0qmanntp7ghmlkmr521s1ote3qmfnla.apps.googleusercontent.com.json', SCOPES)
#     creds = tools.run_flow(flow, store)
# service = build('gmail', 'v1', http=creds.authorize(Http()))






#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from apiclient.discovery import build
import webbrowser
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
# from oauth2client.tools import run
import httplib2
from apiclient import errors
from multiprocessing import Process, Value

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

auth_url = "https://accounts.google.com/o/oauth2/auth?"

response_setting = {
    "scope": "https://mail.google.com/",
    "response_type": "code",
}


class GmailApi():
    def reconnect(self):
        '''サーバーにアクセスして認証をもう一度行う
        '''
        try:
            self.service = GmailServiceFactory().createService(self.auth_info)
        except errors.HttpError as error:
            pass

    def sendMessage(self, user, message):
        """メールを送信します。messageの作り方はcreateMesage関数を参照
            Keyword arguments:
            user -- meを指定する。
            message -- createMessageで生成したオブジェクトを渡す必要があります
            Returns: None
        """
        try:
            message = (self.service.users().messages().send(userId=user, body=message).execute())
            return message
        except errors.HttpError as error:
            print('An error occurred:s' % error)

    def getMailList(self, user, qu):
        ''' メールの情報をリストで取得します
          quの内容でフィルタリングする事が出来ます
           Keyword arguments:
           user -- me又はgoogleDevloperに登録されたアドレスを指定します。
           qu -- queryを設定します
                 例えばexample@gmail.comから送られてきた未読のメールの一覧を取得するには以下のように指定すればよい
                "from: example@gmail.com is:unread"
           Returns: メール情報の一覧　idとThreadIdをKeyとした辞書型のリストになる
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

    def getMailContent(self, user, i):
        """指定したメールのIDからメールの内容を取得します。
                Keyword arguments:
                user -- meを指定する。
                i -- メールのId getMailList()等を使用して取得したIdを使用する
                Returns: メールの内容を辞書型で取得する
                詳細は以下
                http://developers.google.com/apis-explorer/#p/gmail/v1/gmail.users.messages.get
        """
        try:
            return self.service.users().messages().get(userId=user, id=i).execute()
        except errors.HttpError as error:
            self.reconnect()

    def doMailAsRead(self, user, i):
        """指定したメールのIDを既読にします
            Keyword arguments:
            user -- meを指定する。
            i -- メールのId getMailList()等を使用して取得したIdを使用する
            Returns:　なし
        """
        query = {"removeLabelIds": ["UNREAD"]}
        self.service.users().messages().modify(userId=user, id=i, body=query).execute()

    def createMessage(self, sender, to, subject, message_text):
        """sendMessageで送信するメールを生成します
            Keyword arguments:
            sender -- meを指定する。
            to -- メールのId getMailList()等を使用して取得したIdを使用する
            subject -- 件名
            message_text --　メールの内容
            Returns:　なし
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def expMailContents(self, user, i, key):
        try:
            content = self.getMailContent(user, i)
            return ([header for header in content["payload"]["headers"] if header["name"] == key])[0]["value"]
        except errors.HttpError as error:
            self.reconnect()

    def getMailFrom(self, user, i):
        try:
            return self.expMailContents(user, i, "From")
        except errors.HttpError as error:
            self.reconnect()

    def getMailSubject(self, user, i):
        try:
            return self.expMailContents(user, i, "Subject")
        except errors.HttpError as error:
            self.reconnect()

    def __init__(self, auth_info):
        self.auth_info = auth_info
        self.service = GmailServiceFactory().createService(self.auth_info)


class GmailServiceFactory():

    def createService(self, json_path):
        # STORAGE = Storage('gmail.auth.storage')
        # credent = STORAGE.get()
        # if credent is None or credent.invalid:
        #     info = auth_info['installed']
        #     flow = OAuth2WebServerFlow(info["client_id"], info["client_secret"], response_setting["scope"], info["redirect_uris"][0])
        #     auth_url = flow.step1_get_authorize_url()
        #     # ブラウザを開いて認証する
        #     webbrowser.open(auth_url)
        #     code = input("input code : ")
        #     credent = flow.step2_exchange(code)
        #     STORAGE.put(credent)
        # http = httplib2.Http()
        # http = credent.authorize(http)
        #
        # gmail_service = build("gmail", "v1", http=http)
        # return gmail_service
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(json_path, SCOPES)
            creds = tools.run_flow(flow, store)
        return build('gmail', 'v1', http=creds.authorize(Http()))


# Call the Gmail API
def get_label():
    results = service.users().labels().list(userId='me').execute()
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

def getMailContent(self, user, i):
    """指定したメールのIDからメールの内容を取得します。
            Keyword arguments:
            user -- meを指定する。
            i -- メールのId getMailList()等を使用して取得したIdを使用する
            Returns: メールの内容を辞書型で取得する
            詳細は以下
            http://developers.google.com/apis-explorer/#p/gmail/v1/gmail.users.messages.get
    """
    try:
        return self.service.users().messages().get(userId=user, id=i).execute()
    except errors.HttpError as error:
        self.reconnect()


if __name__ == "__main__":
    '''
        GmailApiのサンプルコードです。
        実際の処理はgmailapi.pyで行っています。
        詳しい処理はgmailapi.pyの処理を見てください。
    '''

    user = 'me'

    json_path = './client_secret_626154498738-l0qmanntp7ghmlkmr521s1ote3qmfnla.apps.googleusercontent.com.json'
    api = GmailApi(json_path)#初回実行時は認証が求められます。#初回実行時は認証が求められます。
    query =  "is:unread"#未読メッセージでフィルタリングするクエリ

    #未読メールのリストを表示
    maillist = api.getMailList(user, query )
    print( json.dumps(maillist, indent=4))

    #Idからメールの内容を表示
    content = api.getMailContent(user, maillist["messages"][0]['id'])

    print()
    print( json.dumps(content, indent=4))