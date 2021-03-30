import torch
import json
import nltk
import pickle
import numpy as np
from tqdm import tqdm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import nltk
#nltk.download("punkt")
from nltk.tokenize import word_tokenize
import gensim
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from sys import exit


def reader(file):
    data = []
    with open(f'../data/{file}', 'r') as file:
        for line in file.readlines()[:]:
            data.append(json.loads(line))
    return data


dev, test, train = [reader(file) for file in ['music_reviews_dev.json',
                                              'music_reviews_test_masked.json',
                                              'music_reviews_train.json']]

def tokenize(file):
        X = []
        y = []
        for review in file:
            if 'reviewText' in review.keys():
                X.append(word_tokenize(review['reviewText']))
            else:
                X.append("<U>")
            label = review['sentiment'] == 'positive'
            y.append(label)
        
        return X, y

dev_X, dev_y = tokenize(dev)

#print("LOADING EMBEDDINGS")
model = gensim.models.KeyedVectors.load_word2vec_format('../data/twitter.bin', binary=True)
vocab = set(model.vocab.keys())
#print("EMBEDDINGS LOADED")

def embed(data):
    out = []
    for review in tqdm(data):
        tmp = []
        for word in review:
            tmp.append(model[word]) if word in vocab else tmp.append(model['<U>'])
        t = np.mean(np.array(tmp),axis=0)
        out.append(t)
    return out

#print("STARTED HERE")

dev_X = embed(dev_X)

pred = []
counter = 0
#print("PREDICTING")
clf = pickle.load(open("../models/baseline_SVM", "rb"))
for x_inst, y_inst in zip(dev_X, dev_y):
    pred.append(clf.predict(x_inst.reshape(1, -1)))
    if 'reviewText' not in dev[counter]:
        continue 
    if pred[-1] != y_inst:
        print(dev[counter]['reviewText'])     
        print(y_inst)
        print()
    counter += 1

#print("NO TEXT DATA COUNTER:",counter)
print("id,prediction")
for i in range(len(pred)):
    print(f"{dev[i]['id']},{pred[i]}")
