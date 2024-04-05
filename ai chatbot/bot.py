import random 
import json 
import pickle 
import numpy as np 

import nltk 
# nltk.download('wordnet')
# nltk.download('punkt')
from nltk.stem import WordNetLemmatizer  # to take works ,work, worked as same word


from tensorflow.keras.models import load_model

# firstly, make a lemmatizer
lemmatizer = WordNetLemmatizer()

# load json
with open('intens.json') as file:
    intents = json.load(file)  # now intents is a dicionary


words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot.h5')


def cleanup_sent(sentence):
    sent_words = nltk.word_tokenize(sentence)
    sent_words = [lemmatizer.lemmatize(word) for word in sent_words]
    return sent_words

def  bag_of_words(sentence):
    sent_words = cleanup_sent(sentence)
    bag = [0] * len(words)
    for wor in sent_words:
        for i, w in enumerate(words):
            if w == wor:
                bag[i] = 1
    return np.array(bag)


def predict_class(Sentence):
    bow = bag_of_words(Sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESH = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESH]
    results.sort(key=lambda x: x[1], reverse=True)  # have highest probability first

    ret_list = []
    for i in results:
        ret_list.append({'intent': classes[i[0]], 'probability': str(i[1])})  # Fix the variable name here

    return ret_list


def get_response(intents_lst, intents_json):
    tag = intents_lst[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break

    return result


print('Go')
while True:
    mess = input()
    ints = predict_class(mess)
    res = get_response(ints, intents)
    print(res)