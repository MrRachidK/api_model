import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
import pandas as pd

### Initialize MySQL database
def init_db(mysql):
    pokemon_data = pd.read_csv(os.path.join(basedir, 'data/intermediate/pokemon.csv'), index_col=False, delimiter = ',')

    combats_data = pd.read_csv(os.path.join(basedir, 'data/raw/combats.csv'), index_col=False, delimiter = ',')

    cursor = mysql.connection.cursor()
    # Executing SQL Statements

    ## Database
    cursor.execute("DROP DATABASE IF EXISTS pokemon_analytics")
    cursor.execute("CREATE DATABASE IF NOT EXISTS pokemon_analytics")
    cursor.execute("USE pokemon_analytics")

    ## Tables
    ### Pokemon
    cursor.execute('''DROP TABLE IF EXISTS pokemon''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon (
        Number INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Type_1 VARCHAR(255) NOT NULL,
        Type_2 VARCHAR(255) NOT NULL,
        HP INT NOT NULL,
        Attack INT NOT NULL,
        Defense INT NOT NULL,
        Sp_Atk INT NOT NULL,
        Sp_Def INT NOT NULL,
        Speed INT NOT NULL,
        Generation INT NOT NULL,
        Legendary TINYINT NOT NULL,
        PRIMARY KEY (Number)
    ) 
    ''')

    ### Duels
    cursor.execute('''DROP TABLE IF EXISTS combats''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS combats (
        First_pokemon INT NOT NULL,
        Second_pokemon INT NOT NULL,
        Winner INT NOT NULL,
        FOREIGN KEY (First_pokemon) REFERENCES pokemon(Number),
        FOREIGN KEY (Second_pokemon) REFERENCES pokemon(Number),
        FOREIGN KEY (Winner) REFERENCES pokemon(Number)
    )
    ''')

    # Insertion of data
    for i, row in pokemon_data.iterrows():
        sql = "INSERT INTO pokemon VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, tuple(row))

    for i, row in combats_data.iterrows():
        sql = "INSERT INTO combats (First_pokemon, Second_pokemon, Winner) VALUES (%s, %s, %s)"
        cursor.execute(sql, tuple(row))
    
    # Saving the Actions performed on the DB
    mysql.connection.commit()
    
    # Closing the cursor
    cursor.close()


