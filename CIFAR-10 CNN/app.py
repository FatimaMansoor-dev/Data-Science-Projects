import streamlit as st
import pickle
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models

# Load the Keras model from the pickle file
model_path = 'model.pickle'  
with open(model_path, 'rb') as file:
    loaded_model = pickle.load(file)

# Streamlit app
st.header("Image Classification App")

# Upload image through a file uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image.", use_column_width=True)

    # Preprocess the image
    img = img.resize((32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values to between 0 and 1

    # Make predictions using the loaded Keras model
    predictions = loaded_model.predict(img_array)

    # # Display the prediction
    # st.subheader("Prediction:")
    # predicted_class_index = np.argmax(predictions)
    # st.write(f"The predicted class index is: {predicted_class_index}")

    
    class_labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    # predicted_class = class_labels[predicted_class_index]
    # st.write(f"The predicted class is: {predicted_class}")

    # # Display class probabilities
    # st.subheader("Class Probabilities:")
    # for i, prob in enumerate(predictions[0]):
    #     st.write(f"Class {i}: {prob:.4f}")
    # Display the prediction
    st.header("Prediction:")

    predicted_class_index = np.argmax(predictions)
    predicted_probability = predictions[0, predicted_class_index] * 100
    predicted_class = class_labels[predicted_class_index]

    st.subheader(f"I'm {predicted_probability:.0f}% sure it is a {predicted_class}")
