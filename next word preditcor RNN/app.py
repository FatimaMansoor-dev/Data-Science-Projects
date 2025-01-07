from flask import Flask, render_template, request, jsonify
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = Flask(__name__, static_url_path='/static')

# Load the LSTM model
model = load_model('text_generator/model.h5', compile=False)
model.compile(loss = 'categorical_crossentropy', optimizer ='adam', metrics = ['accuracy'])

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

    # Get the indices of the top 3 predicted words
    top_3_indices = tf.argsort(prediction, direction='DESCENDING')[:3].numpy()

    # Map the indices back to words using the tokenizer
    top_3_words = [tokenizer.index_word.get(index, '') for index in top_3_indices]

    return jsonify({'top_3_words': top_3_words})

if __name__ == '__main__':
    app.run(debug=True)
