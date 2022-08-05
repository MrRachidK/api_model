# Import of the libraries
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir

import pandas as pd
import joblib
from flask_sqlalchemy import SQLAlchemy
from model_app.db import database, Pokemon, Combat

from src.features.functions import create_dictionaries, replace_things, calculate_stats, calculate_effectiveness

def predict_result(pokemon_1, pokemon_2):

    # Initialize SQLAlchemy variables
    pokemon_data = database.session.query(Pokemon).all()
    pokemon_df = pd.DataFrame([p.json() for p in pokemon_data])

    # Create dictionnaries
    name_dict, type_dict, stats_dict = create_dictionaries(pokemon_df)

    # Unpickle model
    model = joblib.load(os.path.join(basedir, 'src/models/best_model.pkl'))

    # Get values through input bars
    X = pd.DataFrame([[pokemon_1, pokemon_2]], columns = ["first_pokemon", "second_pokemon"]).astype('int64')
    print(X)

    # Put inputs to dataframe        
    mapped_X = X.copy()
    mapped_X_replacement = replace_things(mapped_X, stats_dict, type_dict)
    mapped_X_statistics = calculate_stats(mapped_X_replacement)
    mapped_X_types = calculate_effectiveness(mapped_X_statistics)
    
    # Get prediction
    X['winner'] = model.predict(mapped_X_types)[0]
    # X['first_pokemon'] = X['first_pokemon'].map(name_dict)
    # X['second_pokemon'] = X['second_pokemon'].map(name_dict)

    X['winner'][X['winner'] == 0] = X['first_pokemon']
    X['winner'][X['winner'] == 1] = X['second_pokemon']

    prediction = X['winner'].iloc[0]

    return prediction