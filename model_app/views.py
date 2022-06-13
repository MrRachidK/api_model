import sys
import os

from flask import jsonify, request
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from model_app import app 
from src.results.prediction import predict_result
import requests
import json


@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/get_prediction')
def get_prediction():
    data = json.loads(request.get_json())
    pokemon_1 = int(data['First_pokemon'])
    pokemon_2 = int(data['Second_pokemon'])
    prediction = predict_result(pokemon_1, pokemon_2)

    return prediction
    