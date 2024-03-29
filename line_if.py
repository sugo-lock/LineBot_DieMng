# -*- coding: utf-8 -*-
import os
import json

import urllib.request, urllib.parse


def reply_msg(user_id, msg, replyToken):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ os.environ['LINE_ACCESS_TOKEN'],
    }
    body = {
        'replyToken': replyToken,
        'messages': [
            {
                "type":"text",
                "text":msg,
            }
        ]
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method='POST')
    with urllib.request.urlopen(req) as res:
            logger.info(res.read().decode("utf-8"))


def push_msg(user_id, msg):
    try:
        url = 'https://api.line.me/v2/bot/message/push'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ os.environ['LINE_ACCESS_TOKEN'],
        }
        body = {
            'to': user_id,
            'messages': [
                {
                    "type":"text",
                    "text":msg,
                }
            ]
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method='POST')
        responce = urllib.request.urlopen(req)
        return responce.read()
    except:
        print("Line push_msg Error : msg= "+str(msg))

def push_fig(user_id, fig_url):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ os.environ['LINE_ACCESS_TOKEN'],
    }
    body = {
        'to': user_id,
        'messages': [
            {
                "type":"image",
                "originalContentUrl":fig_url,
                "previewImageUrl":fig_url,
            }
        ]
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method='POST')
    responce = urllib.request.urlopen(req)
    return responce.read()

def quick_reply(user_id):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ os.environ['LINE_ACCESS_TOKEN'],
    }
    body = {
        'to': user_id,
        'messages': 
        [
            {
                "type": "text",
                "text": "何をしますか?",
                "quickReply": 
                {
                    "items": 
                    [
                        {
                            "type": "action",
                            "action": {
                            "type": "message",
                            "label": "プロフィールを入力",
                            "text": "profile"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                            "type": "message",
                            "label": "消費カロリーを入力",
                            "text": "cal_burned"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                            "type": "message",
                            "label": "摂取カロリーを入力",
                            "text": "cal_intake"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                            "type": "message",
                            "label": "グラフを表示",
                            "text": "graph"
                            }
                        }
                    ]
                }
            }
        ]
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method='POST')
    responce = urllib.request.urlopen(req)
    return responce.read()
    
if __name__ == '__main__':
    USER_ID = os.environ['LINE_USER_ID']
    TEST_MSG = 'HelloWorld'
    push_msg(USER_ID, TEST_MSG)