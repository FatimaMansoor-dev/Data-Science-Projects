from flask import Flask, render_template, request, jsonify
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = Flask(__name__, static_url_path='/static')

# Load the LSTM model
model = load_model('text_generator/model.h5')

# Load the tokenizer
with open('text_generator/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Maximum sequence length for input
max_sequence_length = 21

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']

    # Tokenize the entire input text
    sequence = tokenizer.texts_to_sequences([text])

    # Pad the sequence
    padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length, padding='pre')

    # Make a prediction
    prediction = model.predict(padded_sequence)[0]

    # Get the predicted word index
    predicted_word_index = tf.argmax(prediction).numpy()

    # Map the index back to the word using the tokenizer
    predicted_word = tokenizer.index_word.get(predicted_word_index, '')

    return jsonify({'predicted_word': predicted_word})

if __name__ == '__main__':
    app.run(debug=True)
