# Import of the libraries
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir

import pandas as pd
import joblib
import mysql.connector
from credentials import sql_user, sql_password, sql_host, sql_database

from src.features.functions import create_dictionaries, replace_things, calculate_stats, calculate_effectiveness

def predict_result(pokemon_1, pokemon_2):

    # Initialize MYSQL connection
    cursor = mysql.connector.connect(user=sql_user, password=sql_password, host=sql_host, database=sql_database)
    pokemon_data = pd.read_sql("SELECT * FROM pokemon", con=cursor)

    # Create dictionnaries
    name_dict, type_dict, stats_dict = create_dictionaries(pokemon_data)

    # Unpickle model
    model = joblib.load(os.path.join(basedir, 'src/models/best_model.pkl'))

    # Get values through input bars
    X = pd.DataFrame([[pokemon_1, pokemon_2]], columns = ["First_pokemon", "Second_pokemon"]).astype('int64')
    print(type(X))

    # Put inputs to dataframe        
    mapped_X = X.copy()
    mapped_X_replacement = replace_things(mapped_X, stats_dict, type_dict)
    mapped_X_statistics = calculate_stats(mapped_X_replacement)
    mapped_X_types = calculate_effectiveness(mapped_X_statistics)
    
    # Get prediction
    X['Winner'] = model.predict(mapped_X_types)[0]
    X['First_pokemon'] = X['First_pokemon'].map(name_dict)
    X['Second_pokemon'] = X['Second_pokemon'].map(name_dict)

    X['Winner'][X['Winner'] == 0] = X['First_pokemon']
    X['Winner'][X['Winner'] == 1] = X['Second_pokemon']

    prediction = X['Winner'].iloc[0]
    cursor.close()

    return prediction