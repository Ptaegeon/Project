#!/usr/bin/env python
# coding: utf-8

import requests
import json
import datetime
import os


def save_tokens(filename, tokens):
    with open(filename, "w") as fp:
        json.dump(tokens, fp)


def save_tokens_first():
    KAKAO_TOKEN_FILENAME = 'res/kakao_message/kakao_token.json'
    KAKAO_APP_KEY = "b73f63f314870db4afb9a0531fcefd08"

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_APP_KEY,
        "redirect_url": "https://localhost.com",
        "code": "nnv-RWUdeO0giNx04DcsO2pTqW8WUV7__ENWmNby4ZFm0OQN73h0TZt7Eu_zT0DuyVvCNwo9dRkAAAGCCfsNog"
    }

    response = requests.post(url, data=data)
    if response.status_code != 200:
        print('error', response.json())
        tokens = None
    else:
        tokens = response.json()
        save_tokens(KAKAO_TOKEN_FILENAME, tokens)
    return tokens


def load_tokens(filename):
    with open(filename) as fp:
        tokens = json.load(fp)

    return tokens


def update_tokens(app_key, filename):
    tokens = load_tokens(filename)
    if tokens == None:
        tokens = save_tokens_first()
        print('first save')

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": app_key,
        "refresh_token": tokens['refresh_token']
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        print('error', response.json())
        tokens = None
    else:
        print(response.json)
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = filename+"."+ now
        os.rename(filename, backup_filename)

        tokens['access_token'] = response.json()['access_token']

        save_tokens(filename, tokens)
        print('update done')
    return tokens


def send_message(filename, template):
    tokens = load_tokens(filename)

    headers = {
        "Authorization": "Bearer " + tokens['access_token']
    }

    payload = {
        "template_object": json.dumps(template)
    }

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    response = requests.post(url, headers=headers, data=payload)
    return response
