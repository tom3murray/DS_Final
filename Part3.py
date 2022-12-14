#Andrew Holzwarth, Tommy Murray, Brett Carey
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
from bson.json_util import dumps


link = open("Intents.json")
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
                
                if tag == "Question_1":
                    #Query Pymongo
                    filter = {'RELEASE_YEAR': 2020}
                    sort = list({'SCORE': -1}.items())
                    limit = 10
                    
                    result = client['Final_Project']['Best_Movies'].find(filter=filter,sort=sort,limit=limit)
                    
                    #Convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information for Question 1 from the JSON file
                    title1 = str(json_list[0]["TITLE"]) 
                    rating1 = str(json_list[0]["SCORE"])
                    movie1 = title1 +": "+ rating1
                    responses.append(movie1)
                    
                    title2 = str(json_list[1]["TITLE"]) 
                    rating2 = str(json_list[1]["SCORE"])
                    movie2 = title2 +": "+ rating2
                    responses.append(movie2)
                    
                    title3 = str(json_list[2]["TITLE"]) 
                    rating3 = str(json_list[2]["SCORE"])
                    movie3 = title3 +": "+ rating3
                    responses.append(movie3)
                    
                    title4 = str(json_list[3]["TITLE"]) 
                    rating4 = str(json_list[3]["SCORE"])
                    movie4 = title4 +": "+ rating4
                    responses.append(movie4)
                    
                    title5 = str(json_list[4]["TITLE"]) 
                    rating5 = str(json_list[4]["SCORE"])
                    movie5 = title5 +": "+ rating5
                    responses.append(movie5)
                    
                    title6 = str(json_list[5]["TITLE"]) 
                    rating6 = str(json_list[5]["SCORE"])
                    movie6 = title6 +": "+ rating6
                    responses.append(movie6)
                    
                    title7 = str(json_list[6]["TITLE"]) 
                    rating7 = str(json_list[6]["SCORE"])
                    movie7 = title7 +": "+ rating7
                    responses.append(movie7)
                    
                    title8 = str(json_list[7]["TITLE"]) 
                    rating8 = str(json_list[7]["SCORE"])
                    movie8 = title8 +": "+ rating8
                    responses.append(movie8)
                    
                    title9 = str(json_list[8]["TITLE"]) 
                    rating9 = str(json_list[8]["SCORE"])
                    movie9 = title9 +": "+ rating9
                    responses.append(movie9)
                    
                    title10 = str(json_list[9]["TITLE"]) 
                    rating10 = str(json_list[9]["SCORE"])
                    movie10 = title10 +": "+ rating10
                    responses.append(movie10)
                    
                elif tag == "Question_2":
                    #Query Pymongo
                    filter = {'RELEASE_YEAR': 2015}
                    sort = list({'SCORE': -1}.items())
                    limit = 1
                    
                    result = client['Final_Project']['Best_Movies'].find(filter=filter, sort=sort, limit=limit)
                    
                    #Convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information from the JSON format
                    title1 = str(json_list[0]["TITLE"]) 
                    duration1 = str(json_list[0]["DURATION"])
                    movie1 = "The longest movie was: "+ title1 + " with a length of " + duration1 + " minutes."
                    responses.append(movie1)
                    
                elif tag == "Question_3":
                    #Query Pymongo
                    filter = {'SCORE': {'$gte': 7.5}}
                    
                    result = client['Final_Project']['Best_Shows'].find(filter=filter)
                    
                    #Convert the pymongo cursor into a JSON file
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #count the number of shows in the JSON file
                    count = len(json_list)
                     
                    count = str(count)
                    responses.append("There are " + count + " shows with rankings above 7.5")
                    
                elif tag == "Question_4":
                    #Query Pymongo
                    filter = {'RELEASE_YEAR': 2018}
                    sort = list({'SCORE': -1}.items())
                    limit = 10
                    
                    result = client['Final_Project']['Best_Shows'].find(filter=filter,sort=sort,limit=limit)
                    
                    #Convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information from the JSON file
                    title1 = str(json_list[0]["TITLE"]) 
                    rating1 = str(json_list[0]["SCORE"])
                    show1 = title1 +": "+ rating1
                    responses.append(show1)
                    
                    title2 = str(json_list[1]["TITLE"]) 
                    rating2 = str(json_list[1]["SCORE"])
                    show2 = title2 +": "+ rating2
                    responses.append(show2)
                    
                    show3 = str(json_list[2]["TITLE"]) 
                    rating3 = str(json_list[2]["SCORE"])
                    movie3 = title3 +": "+ rating3
                    responses.append(show3)
                    
                    title4 = str(json_list[3]["TITLE"]) 
                    rating4 = str(json_list[3]["SCORE"])
                    show4 = title4 +": "+ rating4
                    responses.append(show4)
                    
                    title5 = str(json_list[4]["TITLE"]) 
                    rating5 = str(json_list[4]["SCORE"])
                    show5 = title5 +": "+ rating5
                    responses.append(show5)
                    
                    title6 = str(json_list[5]["TITLE"]) 
                    rating6 = str(json_list[5]["SCORE"])
                    show6 = title6 +": "+ rating6
                    responses.append(show6)
                    
                    title7 = str(json_list[6]["TITLE"]) 
                    rating7 = str(json_list[6]["SCORE"])
                    show7 = title7 +": "+ rating7
                    responses.append(show7)
                    
                    title8 = str(json_list[7]["TITLE"]) 
                    rating8 = str(json_list[7]["SCORE"])
                    show8 = title8 +": "+ rating8
                    responses.append(show8)
                    
                    title9 = str(json_list[8]["TITLE"]) 
                    rating9 = str(json_list[8]["SCORE"])
                    show9 = title9 +": "+ rating9
                    responses.append(show9)
                    
                    title10 = str(json_list[9]["TITLE"]) 
                    rating10 = str(json_list[9]["SCORE"])
                    show10 = title10 +": "+ rating10
                    responses.append(show10)
                    
                elif tag == "Question_5":
                    #Query Pymongo
                    filter = {'RELEASE_YEAR': 2016}
                    sort = list({'SCORE': -1}.items())
                    limit = 1
                    
                    result = client['Final_Project']['Best_Movies'].find(filter=filter, sort=sort, limit=limit)
                    
                    #Convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information from the JSON file
                    title1 = str(json_list[0]["TITLE"]) 
                    genre1 = str(json_list[0]["MAIN_GENRE"])
                    movie1 = "The best movie was: "+ title1 + " with a genre of " + genre1
                    responses.append(movie1)
                    
                elif tag == "Question_6":
                    #Query Pymongo
                    filter={'RELEASE_YEAR': 2008}
                    sort=list({'SCORE': 1}.items())
                    limit=1
                    
                    result = client['Final_Project']['Best_Movies'].find(filter=filter,sort=sort,limit=limit)
                    
                    #Convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information from the JSON file
                    title1 = str(json_list[0]["TITLE"]) 
                    rating1 = str(json_list[0]["SCORE"])
                    movie1 = "The worst movie was: "+ title1 + " with a score of " + rating1
                    responses.append(movie1)
                    
                elif tag == "Question_7":
                    #uery Pymongo
                    filter = {  'RELEASE_YEAR': 2013 }
                    sort = list({'DURATION': -1}.items())
                    limit = 1
                    
                    result = client['Final_Project']['Best_Movies'].find(filter=filter,sort=sort,limit=limit)
                    
                    #Convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information from the JSON file
                    title1 = str(json_list[0]["TITLE"]) 
                    duration1 = str(json_list[0]["DURATION"])
                    movie1 = "The longest movie was: "+ title1 + " with a lenght of " + duration1 + " minutes."
                    responses.append(movie1)
                    
                elif tag == "Question_8":
                    #Query Pymongo
                    filter = {}
                    sort = list({'NUMBER_OF_SEASONS': -1 }.items())
                    limit = 1
                    
                    result = client['Final_Project']['Best_Shows'].find(filter=filter,sort=sort,limit=limit)
                    
                    #Convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information from the JSON file
                    title1 = str(json_list[0]["TITLE"]) 
                    seasons1 = str(json_list[0]["NUMBER_OF_SEASONS"])
                    show1 = title1 + " had the most seasons with: " + seasons1
                    responses.append(show1)
                    
                elif tag == "Question_9":
                    #Query Pymongo
                    filter = {'RELEASE_YEAR': 2019 }
                    sort = list({ 'SCORE': -1}.items())
                    limit = 1
                    
                    result = client['Final_Project']['Best_Shows'].find(filter=filter, sort=sort,limit=limit)
                    
                    #convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the relevant information from JSON file
                    title1 = str(json_list[0]["TITLE"]) 
                    genre1 = str(json_list[0]["MAIN_GENRE"])
                    show1 = "The best show was: "+ title1 + " with a genre of " + genre1
                    responses.append(show1)
                    
                elif tag == "Question_10":
                    #Query Pymongo
                    filter={'release_year': 2009, 'age_certification': 'R'}
                    
                    result = client['Final_Project']['Raw_Titles'].find(filter=filter)
                    
                    #convert the pymongo cursor object into JSON
                    list_cur = list(result)
                    json_data = dumps(list_cur)
                    json_list = json.loads(json_data)
                    
                    #Find the number of movies in the JSON file
                    count = len(json_list)
                     
                    count = str(count)
                    
                    count = str(count)
                    responses.append("There are " + count + " movies that were rated 'R'")
                elif tag == "help":
                    print("Here are some questions that you can ask: ")
                    response = tg['responses']
                    responses.append(response)
                    
                    
                    
            print(responses)
            responses.clear()
            
        else:
            print("I didnt get that. Can you explain or try again.")

chat()
