import pickle
import numpy as np

def random_forest_predict(Z):
    
    Z = np.array(Z)
    Z = Z.reshape(1, -1)
    
    model = pickle.load(open('ML/decision_trees.sav', 'rb'))

    prediction = model.predict(Z)
    
    return prediction
