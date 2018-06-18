import json
import quopri

from gmail import *


if __name__ == "__main__":
    '''
        GmailApi sample code。
    '''

    user = 'me'

    json_path = './client_secret_626154498738-l0qmanntp7ghmlkmr521s1ote3qmfnla.apps.googleusercontent.com.json'
    api = GmailApi(json_path) #You need authorized when you run at first time.
    query =  "is:unread"#Unread message query

    #Show unread message list
    maillist = api.getMailList(user, query )
    print("---Show unread message list as id and threadId---")
    print( json.dumps(maillist, indent=4))

    #show row mail contents
    content = api.getMailContent(user, maillist["messages"][0]['id']) # [0]<-select message from message list
    print("---Show mail row contents---")
    print( json.dumps(content, indent=4))

    readTitle(content)
    print("---Title---")
    title = readTitle(content)
    print(title)
    print("---Body---")
    body = readMessage(content)
    print(body)
    print("---Snippet---")
    snippet = readSnippet(content)
    print(snippet)