# Import of the libraries
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

import joblib

def get_best_model(features):
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(features.drop(['id', 'winner'], axis=1), features['winner'], test_size=0.2, random_state=0)

    # Create the models
    models = {
        'Logistic Regression': LogisticRegression(),
        'Naive Bayes': GaussianNB(),
        'Random Forest': RandomForestClassifier(n_estimators=100),
        'AdaBoost': AdaBoostClassifier(n_estimators=100),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100),
        'KNN': KNeighborsClassifier(),
        'Linear SVC': LinearSVC(),
        'Decision Tree': DecisionTreeClassifier()
    }

    # Evaluate each model, adding results to a results array
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        results[name] = (model, accuracy_score(preds, y_test))


    # Sort the results so the best model is first
    results = sorted(results.items(), key=lambda x: x[1][1], reverse=True)
    print(results)
    # Save the best model for future use
    joblib.dump(results[0][1][0], os.path.join(basedir, 'src/models/best_model.pkl'))

    return results
