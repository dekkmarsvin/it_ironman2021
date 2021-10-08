from configparser import ConfigParser
from requests.models import Response
import jwt
from jwt.algorithms import RSAAlgorithm
import time
import json
from linebot import LineBotApi
from linebot.models import (
    RichMenu, RichMenuArea, RichMenuResponse, RichMenuSize, RichMenuBounds, URITemplateAction, URIAction
)
import os

import APIPm

def GenJWT(cfg):
    privateKey = cfg['key']
    headers = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": cfg['kid']
    }
    payload = {
        # https://developers.line.biz/en/docs/messaging-api/generate-json-web-token/#generate-jwt
        # Channel ID
        "iss": cfg['cid'],
        # Channel ID
        "sub": cfg['cid'],
        "aud": "https://api.line.me/",
        # The expiration time of the JWT. Set this value in UNIX timestamp. The max lifetime of a JWT Assertion is 30 minutes.
        "exp":int(time.time())+(60 * 30),
        # Required when requesting a channel access token. This represents a valid expiration time for the channel access token in seconds. The max lifetime of a channel access token is 30 days.
        # "token_exp": 60 * 60 * 24 * 30 # 30days
        "token_exp": 60 * 30
    }
    key = RSAAlgorithm.from_jwk(privateKey)
    JWT = jwt.encode(payload, key, algorithm="RS256", headers=headers, json_encoder=None)
    # print(f"JWT:{JWT}")
    return JWT

def Issue_channel_access_token(JWT):
    #https://developers.line.biz/en/reference/messaging-api/#issue-channel-access-token-v2-1
    url = "https://api.line.me/oauth2/v2.1/token"
    headers = APIPm.xwwwformurlencodedheaders
    data = {
        "grant_type":"client_credentials",
        "client_assertion_type":"urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": JWT
    }
    resp = APIPm.sendreq(url=url, headers=headers, data=data)
    # resp = json.loads(resp.text)
    return jsonresphandler(resp)

def Get_all_valid_channel_access_token_key_IDs(JWT):
    url = "https://api.line.me/oauth2/v2.1/tokens/kid"
    payload = {
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": JWT
    }
    resp = APIPm.sendreq(method="GET", url=url, headers={}, params=payload)
    return jsonresphandler(resp)

def jsonresphandler(resp:Response):
    data = json.loads(resp.text)
    if "error" in resp:
        #todo a logging level:error
        return False, f"error:{data['error'], data['error_description']}"
    else:
        #todo a logging level:debug
        return True, data

def Revoke_channel_access_token(cfg, access_token):
    url = "https://api.line.me/oauth2/v2.1/revoke"
    payload = {
        "client_id": cfg['cid'],
        "client_secret": cfg['cst'],
        "access_token": None
    }
    if(access_token == "ALL"):
        print("WARING!!! Remove ALL access_token")
    else:
        p = payload.copy()
        p['access_token'] = access_token
        resp = APIPm.sendreq(url=url, headers={}, params=p)
        if(resp.status_code!=200):jsonresphandler(resp)
        else:print("OK") #todo a logging level:debug

def Send_push_message(token, IDs):
    access_token = token['access_token']
    url = "https://api.line.me/v2/bot/message/push"
    headers = APIPm.jsonheaders.copy()
    headers['Authorization'] = f"Bearer {access_token}"
    data = {
        "to": IDs,
        "messages":[
            {
                "type":"text",
                "text":"Hello, world"
            },
            {
                "type":"text",
                "text":"Hello, ITironman"
            }
        ]
    }
    resp = APIPm.sendreq(url=url, headers=headers, data=json.dumps(data, indent=4))
    return jsonresphandler(resp)

def Create_Rich_Menu(line_bot_api:LineBotApi, image_width:int, image_height:int, name:str, char_bar_text:str, richmenuarea):
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=image_width, height=image_height),
        selected=False,
        name=name,
        chat_bar_text=char_bar_text,
        areas=richmenuarea
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    return rich_menu_id

def Upload_Rich_Menu(line_bot_api:LineBotApi, file_path, rich_menu_id):
    extension = os.path.splitext(file_path)[1]
    if(extension == 'jpg' or extension == 'jpeg'):
        content_type = 'image/jpeg'
    elif(extension == 'png'):
        content_type = 'image/png'
    else:
        return False
    with open(file_path, 'rb') as f:
        print(f)
        line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
    return True

def get_rich_menu_list(line_bot_api:LineBotApi, timeout=None):
    rich_menu_list = line_bot_api.get_rich_menu_list(timeout=timeout)
    return rich_menu_list

if __name__ == '__main__':
    # env = ConfigParser(allow_no_value=True)
    # env.read('env.ini')
    # cfg = env._sections['Line']
    # JWT = GenJWT(cfg)
    # print(f"JWT:{JWT}")
    # isSucc, token = Issue_channel_access_token(JWT)
    # print(token)
    # isSucc, kids = Get_all_valid_channel_access_token_key_IDs(JWT)
    # print(kids)
    # token = {'access_token': 'eyJhbGciOiJIUzI1NiJ9.rCPxHhzPh9a695jVnlvWBuWTwCmIQZZU2gXp0BP6be70wIkDG1Hm_SXP39__uBTlhUDHea7l4aXeqK8e9udgyIskq4-qNx2lGWLwiTPENhahBuJOGYPWT6RXlpaKb9Ee.w8yew-gqmnXqg56W2GXWYltLQNpoJLERBvv4D-9P_pY', 'token_type': 'Bearer', 'expires_in': 1800, 'key_id': 'YWtMca9HrnOYS93ibBYF8Q'}
    # print(Send_push_message(token, cfg['me']))

    print()