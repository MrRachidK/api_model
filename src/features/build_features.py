# Import of the libraries
import sys 
import os

import data
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import pandas as pd
from src.features.functions import create_dictionaries, replace_things, calculate_stats, calculate_effectiveness
from flask_sqlalchemy import SQLAlchemy
from model_app.db import database, Pokemon, Combat
from app import app

def create_features():

    with app.app_context():
        # Get pokemon data
        pokemon_data = database.session.query(Pokemon).all()
        pokemon_df = pd.DataFrame([p.json() for p in pokemon_data])

        # Get combats data
        combats_data = database.session.query(Combat).all()
        combats_df = pd.DataFrame([c.json() for c in combats_data])

        # Data processing

        ## Creation of columns

        ## Update of columns

        #changing winner to 0 and 1, each corresponds to first and second pokemon respectively
        combats_df.winner[combats_df.winner == combats_df.first_pokemon] = 0
        combats_df.winner[combats_df.winner == combats_df.second_pokemon] = 1
        ## Creation of dictionnaries

        name_dict, type_dict, stats_dict = create_dictionaries(pokemon_df)

        ## Map the battle to pokemon's data

        train_df = replace_things(combats_df, stats_dict, type_dict)
        train_df = calculate_stats(train_df)
        train_df = calculate_effectiveness(train_df)

        return train_df