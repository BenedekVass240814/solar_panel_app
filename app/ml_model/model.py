import os
import numpy as np
import gdown
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore

# Constants
FILE_ID = "1WfHG_Zs08Wlltu2FsAWMlUpo3vYHfd-g"
MODEL_FILENAME = "final_best.h5"
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)

# Function to download the model from Google Drive using gdown
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Model file not found. Downloading via gdown...")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("Model downloaded successfully.")

# Ensure model is available
download_model()

# Load the trained model
model = load_model(MODEL_PATH)

# Define image preprocessing function
def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Function to make predictions
def classify_image(img_path):
    processed_img = preprocess_image(img_path)
    prediction = model.predict(processed_img)
    predicted_class = np.argmax(prediction, axis=1)[0]
    print(prediction)
    return predicted_class, prediction[0, predicted_class]
