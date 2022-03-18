from cgitb import reset
import os
import json
from json.decoder import JSONDecodeError
from re import T

DIR_DATABASE = os.getenv("DIR_DATABASE")

def read_json():
    try:
        with open(f'{DIR_DATABASE}/database.json', "r") as json_database:
            return json.load(json_database)
    except (FileNotFoundError, JSONDecodeError):       
        file = {"data":[]}
        with open(f'{DIR_DATABASE}/database.json', "w") as json_database:
            return json.dump(file,json_database,indent=2)
             
def validate_keys(payload: dict, expected_keys: set):
    bory_keys_set = set(payload.keys())

    invalis_keys = bory_keys_set - expected_keys

    if invalis_keys:
        raise KeyError(
            {
                 "error":"Keys Invalidas",
                "expected":list(expected_keys),
                "received":list(bory_keys_set),
            }
        )

def formar_data(data:dict):
    id = ''
    with open(f'{DIR_DATABASE}/database.json', "r") as json_database:
        id = len(json.load(json_database)["data"]) + 1
    name = data["nome"].split(" ")
    new_name = []
    for item in name:
        new_name.append(item.title())
    new_name = " ".join(new_name)
    new_email = data["email"].lower()

    return {'nome':new_name, 'email':new_email, 'id':id}


def upload_data(data):
    json_list = read_json()
    json_list["data"].append(data)
    with open(f'{DIR_DATABASE}/database.json', "w") as json_database:
        json.dump(json_list, json_database, indent=2)
        return True

def verification_email(data):
    result = True
    json_list= read_json()["data"]
    print(json_list)
    for item in json_list:
        if item['email'] == data['email']:
            return False

    return result

def verification_value(data):
    if type(data["nome"]) != str:
        return False
    if type(data["email"]) != str:
        return False
    
    return True

    