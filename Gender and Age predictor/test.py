import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load your pre-trained model
model = load_model('model.keras', compile=False)

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to preprocess the image
def preprocess_image(image):
    # Convert to grayscale
    if image.ndim == 3:  # Check if the image has three dimensions (i.e., color)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    image = cv2.resize(image, (64, 64))  # Resize to match model input size
    image = img_to_array(image) / 255.0  # Normalize to [0, 1]
    image = np.expand_dims(image, axis=-1)  # Add channel dimension for grayscale
    return np.expand_dims(image, axis=0)  # Add batch dimension

# Function to predict age and gender
def predict_age_gender(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]  # Get the face region
        face_array = preprocess_image(face)  # Preprocess the face

        # Make predictions
        preds = model.predict(face_array)
        predicted_gender = 'Male' if round(preds[1][0][0]) == 1 else 'Female'
        predicted_age = round(preds[0][0][0])

        # Draw rectangle around the face and put predictions
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f'Age: {predicted_age}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f'Gender: {predicted_gender}', (x, y+h+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Predict age and gender for the current frame
    frame = predict_age_gender(frame)

    # Display the video feed with predictions
    cv2.imshow('Webcam Age and Gender Prediction', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
