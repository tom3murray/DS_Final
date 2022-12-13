import nltk

nltk.download('punkt')

from nltk import word_tokenize, sent_tokenize

from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
# read more on the steamer https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
import pymongo

link = open("/Users/andrewholzwarth/Desktop/DS 2002/Final_Project/Intents.json")
data = json.load(link)

client = pymongo.MongoClient('mongodb://localhost:27017/')

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:
            for tg in data["intents"]:
                responses = []
                if tg['tag'] == "Question_1":
                    filter = {'RELEASE_YEAR': 2020}
                    sort = list({'SCORE': -1}.items())
                    limit = 10

                    result = client['Final_Project']['Best_Movies'].find(filter=filter,sort=sort,limit=limit)
                    responses.append(result)

                elif tg['tag'] == "Question_2":
                    filter = {'RELEASE_YEAR': 2015}
                    sort = list({'SCORE': -1}.items())
                    limit = 1

                    result = client['Final_Project']['Best_Movies'].find(filter=filter, sort=sort, limit=limit)
                    responses.append(result)

                elif tg['tag'] == "Question_3":
                    filter = {'SCORE': {'$gte': 7.5}}
                    sort = list({'SCORE': -1}.items())

                    result = client['Final_Project']['Best_Shows'].find(filter=filter,sort=sort)
                    responses.append(result)

                elif tg['tag'] == "Question_4":
                    filter = {'RELEASE_YEAR': 2018,'SCORE': {'$gte': 7.5} }
                    sort = list({'SCORE': -1}.items())
                    limit = 10

                    result = client['Final_Project']['Best_Shows'].find(filter=filter,sort=sort,limit=limit)
                    responses.append(result)

                elif tg['tag'] == "Question_5":
                    filter = {'RELEASE_YEAR': 2016}
                    sort = list({'SCORE': -1}.items())
                    limit = 1

                    result = client['Final_Project']['Best_Movies'].find(filter=filter, sort=sort, limit=limit)
                    responses.append(result)

                elif tg['tag'] == "Question_6":
                    filter = {'RELEASE_YEAR': 2008}
                    sort = list({'Score': 1}.items())
                    limit = 1

                    result = client['Final_Project']['Best_Movies'].find( filter=filter,sort=sort,limit=limit)
                    responses.append(result)

                elif tg['tag'] == "Question_7":
                    filter = {  'RELEASE_YEAR': 2013 }
                    sort = list({'DURATION': -1}.items())
                    limit = 1

                    result = client['Final_Project']['Best_Movies'].find(  filter=filter,sort=sort,   limit=limit )
                    responses.append(result)

                elif tg['tag'] == "Question_8":
                    filter = {}
                    sort = list({'NUMBER_OF_SEASONS': -1 }.items())
                    limit = 1

                    result = client['Final_Project']['Best_Shows'].find(filter=filter,sort=sort,limit=limit)
                    responses.append(result)

                elif tg['tag'] == "Question_9":
                    filter = {'RELEASE_YEAR': 2019 }
                    sort = list({ 'SCORE': -1}.items())
                    limit = 1

                    result = client['Final_Project']['Best_Shows'].find(filter=filter, sort=sort,limit=limit)
                    responses.append(result)

                elif tg['tag'] == "Question_10":
                    filter = { 'RELEASE_YEAR': 2019 }
                    sort = list({'SCORE': -1}.items())
                    limit = 1

                    result = client['Final_Project']['Best_Shows'].find(filter=filter,sort=sort,limit=limit)
                    responses.append(result)

            print(responses)
            responses.clear()

        else:
            print("I didnt get that. Can you explain or try again.")

chat()
