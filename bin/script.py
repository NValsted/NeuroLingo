import torch
import json
from nltk.tokenize import word_tokenize
import gensim
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from tqdm import tqdm

def reader(file):
    data = []
    with open(f'../data/{file}', 'r') as file:
        for line in file.readlines():
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
                if review['sentiment'] == 'positive':
                    y.append(1)
                elif review['sentiment'] == 'negative':
                    y.append(0)
                else:
                    y.append(-1)
        return X, y

dev_tok, test_tok, train_tok = [tokenize(file) for file in [dev, test, train]]
dev_X, dev_y, test_X, test_y, train_X, train_y = dev_tok[0], dev_tok[1], test_tok[0], test_tok[1], train_tok[0], train_tok[1]


model = gensim.models.KeyedVectors.load_word2vec_format('../data/twitter.bin', binary=True)
vocab = set(model.vocab.keys())


def embed(data):
    out = []
    for review in data:
        tmp = []
        for word in review:
            tmp.append(model[word]) if word in vocab else data.append(model['<U>'])
        out.append(sum(tmp))
    return out


dev_X, test_X, train_X = [embed(data) for data in [dev_X, test_X, train_X]]o


clf = SVC()
clf.fit(train_X, train_y)
p = clf.predict(dev_X)
print(f1_score(dev_y, p))

