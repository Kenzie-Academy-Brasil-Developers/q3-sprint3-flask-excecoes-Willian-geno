from http import HTTPStatus
from operator import ne
from flask import Flask, jsonify, request
from .servicis import read_json, validate_keys, formar_data, upload_data, verification_email, verification_value
import os
import json

app = Flask(__name__)

DIR_DATABASE = os.getenv("DIR_DATABASE")

if not os.path.isdir(DIR_DATABASE):
    os.mkdir(DIR_DATABASE)
    with open(f'{DIR_DATABASE}/database.json', "w") as json_database:
        file = {"data":[]}
        json.dump(file,json_database,indent=2)

@app.get("/user")
def get_user():
    result = read_json()
    return jsonify(result), HTTPStatus.OK

@app.post("/user")
def post_user():
    excted_keys = {"nome", "email"}
    data = request.get_json()

    try: 
        validate_keys(data, excted_keys)
    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST 
    
    if not verification_value(data):
        return {"msg":"Valres invalido, Todos os valores passados devem ser do tipo 'stg'"}, HTTPStatus.BAD_REQUEST
        
    if not verification_email(data):
        return {"msg":"Email já cadastrado"}, HTTPStatus.CONFLICT
        
    if upload_data(formar_data(data)):
        return {"msg": "Criado com sucesso"}, HTTPStatus.CREATED
    