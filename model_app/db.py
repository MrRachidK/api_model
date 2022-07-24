import sys 
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import logging as lg

database = SQLAlchemy()

class Pokemon(database.Model):
    __tablename__ = 'pokemon'
    number = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255))
    type_1 = database.Column(database.String(255))
    type_2 = database.Column(database.String(255))
    hp = database.Column(database.Integer)
    attack = database.Column(database.Integer)
    defense = database.Column(database.Integer)
    sp_atk = database.Column(database.Integer)
    sp_def = database.Column(database.Integer)
    speed = database.Column(database.Integer)
    generation = database.Column(database.Integer)
    legendary = database.Column(database.Boolean)
    
    def __repr__(self):
        return '<Pokemon %r>' % self.name

    def json(self):
        return {
            'number': self.number,
            'name': self.name,
            'type_1': self.type_1,
            'type_2': self.type_2,
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'sp_atk': self.sp_atk,
            'sp_def': self.sp_def,
            'speed': self.speed,
            'generation': self.generation,
            'legendary': self.legendary,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()

class Combat(database.Model):
    __tablename__ = 'combats'
    id = database.Column(database.Integer, primary_key=True)
    first_pokemon = database.Column(database.Integer, ForeignKey('pokemon.number'))
    second_pokemon = database.Column(database.Integer, ForeignKey('pokemon.number'))
    winner = database.Column(database.Integer, ForeignKey('pokemon.number'))

    def __repr__(self):
        return '<Combat %r>' % self.id

    def json(self):
        return {
            'id': self.id,
            'first_pokemon': self.first_pokemon,
            'second_pokemon': self.second_pokemon,
            'winner': self.winner,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()

def init_db():
    database.drop_all()
    database.create_all()

    pokemon_data = pd.read_csv(os.path.join(basedir, 'data/intermediate/pokemon.csv'), index_col=False, delimiter = ',')
    pokemon_data = pokemon_data.rename(columns={'Sp. Atk': 'sp_atk', 'Sp. Def': 'sp_def'})
    pokemon_data.to_sql('pokemon', database.engine, if_exists='append', index=False)

    combats_data = pd.read_csv(os.path.join(basedir, 'data/raw/combats.csv'), index_col=False, delimiter = ',')
    combats_data.to_sql('combats', database.engine, if_exists='append', index=False)

    lg.info('Database initialized')

