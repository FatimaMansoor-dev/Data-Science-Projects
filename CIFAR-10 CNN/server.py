
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from tensorflow.keras.preprocessing import image

app = Flask(__name__, template_folder='app/templates', static_folder='app')



# Load your image classification model
with open('model.pickle', 'rb') as file:
    loaded_model = pickle.load(file)

# Assuming you have a list of classes for your model
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

@app.route("/")
def index():
    # Adjust the template path to point to the 'app' folder
    return render_template("app/index.html")

@app.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"})

    image_file = request.files["image"]

    # Load and preprocess the image
    img = image.load_img(image_file, target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values to between 0 and 1

    # Make predictions
    predictions = loaded_model.predict(img_array)

    # Assuming your model is a classification model with 10 classes
    class_index = np.argmax(predictions)
    predicted_class = classes[class_index]

    return jsonify({"prediction": predicted_class})

if __name__ == "__main__":
    app.run(debug=True)
