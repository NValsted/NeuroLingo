# generator.py
#   make annoying data
# by: Neurolingos

# imports
import random
import json
import spacy
spacy.load('en_core_web_sm')
import checklist
from checklist.perturb import Perturb
from checklist.editor import Editor
editor = Editor()
adjpos = """ great fun lovely sexy wonderful amazing awesome good fantastic excelent masterful fabulous faboulus incredible salacious"""
adjpos = adjpos.strip().split()
adjneg = """terrible horrible shitty worst disasterous bad abominable atrocious crappy repulsive yucky irredeemable"""
adjneg = adjneg.strip().split()

rev_neg_pos = "some parts are {pos} but overall it is {neg}."
rev_pos_neg = "some parts are {neg} but overall it is {pos}."
out = editor.template(rev_neg_pos, pos=adjpos, neg=adjneg)
print(out)
out = editor.template(rev_pos_neg, pos=adjpos, neg=adjneg)
print(out)




seed = 'I had a {neg} day really {neg} but the album made it {pos}'
ous = editor.template(seed, pos=adjpos, neg=adjneg)
print(ous)




seed = 'I had a {pos} day really {pos} but the album made it {neg}'
ous = editor.template(seed, pos=adjpos, neg=adjneg)
print(ous)

with open('../data/music_reviews_dev.json', 'r') as f:
    data = []
    for line in f.readlines():
        data.append(json.loads(line))
data = random.sample(data, 100)

tmp = []
for d in data:
    tmp.append(d['reviewText'])
    
print(Perturb.perturb(tmp, Perturb.add_typos))
    







