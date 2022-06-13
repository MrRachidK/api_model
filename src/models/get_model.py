# Import of the libraries
from pyexpat import features
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.features.build_features import create_features
from src.models.predict_model import get_best_model

features = create_features()
model = get_best_model(features)
