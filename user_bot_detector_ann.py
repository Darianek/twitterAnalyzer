import numpy as np


def ann_predict(Z):        
    
    Z = np.array(Z)
    Z = Z.reshape(1, -1)
    
    # Importing the Keras libraries and packages
    import keras
    
    model = keras.models.load_model('ML/user_bot_detector_ann.h5')
    
    pred = model.predict(Z)
    pred = (pred > 0.5)
    
    return pred
    