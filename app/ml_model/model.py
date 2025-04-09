import os
import numpy as np
import random


# Function to make predictions
def classify_image(img_path):
    prediction = np.array([[random.uniform(0, 1) for i in range(6)]])
    predicted_class = np.argmax(prediction, axis=1)[0]
    print(prediction)
    return predicted_class, prediction[0, predicted_class]
