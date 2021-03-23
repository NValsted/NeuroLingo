import torch
import json
import nltk
import pickle
import numpy as np
from tqdm import tqdm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import nltk
nltk.download("punkt")
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
                y.append(1)
            else:
                y.append(-1)
                X.append("_")
        
        return X, y

test_X, test_y = tokenize(test)

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

test_X = embed(test_X)

pred = []
counter = 0
#print("PREDICTING")
clf = pickle.load(open("SVM","rb"))
for x_inst,y_inst in zip(test_X,test_y):
    if y_inst == -1:
        counter += 1
        pred.append(1)
    else:
        pred.append(clf.predict(x_inst.reshape(1,-1))[0])

#print("NO TEXT DATA COUNTER:",counter)
print("id,prediction")
for i in range(len(pred)):
    print(f"{test[i]['id']},{pred[i]}")
