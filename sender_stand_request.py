import configuration

import requests

import data 

def post_new_kit(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_KIT_PATH,
                         json=body,
                         headers=data.headers)

def get_kits_by_card_id(card_id):
    return requests.get(
        configuration.URL_SERVICE + configuration.CREATE_KIT_PATH,
        params={"cardId": card_id},
        headers=data.headers
    )