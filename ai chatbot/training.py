import random
import json
import numpy as np 
import pickle 

import nltk 
nltk.download('wordnet')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer  # to take works ,work, worked as same word

import tensorflow as tf
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Activation, Dropout 
from tensorflow.keras.optimizers import SGD


# firstly, make a lemmatizer
lemmatizer = WordNetLemmatizer()

# load json
with open('intens.json') as file:
    intents = json.load(file)  # now intents is a dicionary

words = []
classes = []
documents = []
ignore_letters = ['?', '!',  '.', ',', '@', '$', '&c']


# get inside dict
for inten in intents['intents']:
    # tokenize all the patterns and add to words list
    for pattern in inten['patterns']:
        words_lst = nltk.word_tokenize(pattern)
        words.extend(words_lst)
        documents.append((words_lst, inten['tag'])) # [(['how', 'are', 'you'], 'greeting')]

        if  inten['tag'] not in classes:
            classes.append(inten['tag'])


# lemmatize the word
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


## training
training =[]
output_empty = [0]* len(classes) # a list of 0's equal to classes

for doc in documents:
    bag = []
    word_pattern = doc[0] # ['how', 'are', 'you']
    word_pattern = [lemmatizer.lemmatize(word.lower()) for word in word_pattern]
    for word in words:
        bag.append(1) if word in word_pattern else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1 # set the value of array at index corresponding to doc tag to
    training.append(bag + output_row )  # [[[0,0,0,1,0,0,1,0,0], [0,0,1]]]
                                        #    --- words ---      --class--
random.shuffle(training)
training = np.array(training)

train_x = training[:, :len(words)]
train_y = training[:, len(words):]

## model building 

model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax')) # one per each class variable

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=8, verbose=1)

model.save('chatbot.h5')