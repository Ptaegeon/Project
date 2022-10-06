#!/usr/bin/env python
# coding: utf-8

import requests
import json
import datetime
import os

def save_tokens(filename, tokens):
    with open(filename, "w") as fp:
        json.dump(tokens, fp)


def load_tokens(filename):
    with open(filename) as fp:
        tokens = json.load(fp)

    return tokens

def update_tokens(app_key, filename):
    tokens = load_tokens(filename)

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
        print(tokens)
        now = datetime.datetime.now().strftime("%Y%m%D_%H%M%S")
        backup_filename = filename + '.' + now
        os.rename(filename, backup_filename)

        tokens['access_token'] = response.json()['access_token']
        save_tokens(filename, tokens)
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
