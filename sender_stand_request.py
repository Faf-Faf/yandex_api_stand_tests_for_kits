import configuration

import requests

import data 

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

def post_new_kit(body, auth_token):
    # набор создаётся от имени пользователя — передаём его токен
    headers = {**data.headers, "Authorization": f"Bearer {auth_token}"}
    return requests.post(
        configuration.URL_SERVICE + configuration.CREATE_KIT_PATH,
        json=body,
        headers=headers
    )