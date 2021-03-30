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
from datetime import datetime
import time

def to_json(text,label,ID):
    data_object = {"verified": random.choice([True,False]),
                   "reviewTime": "03 30, 2021",
                   "reviewerID": f"NeuroLingo{random.randint(100000,99999999)}",
                   "asin": str(random.randint(100000,99999999)),
                   "reviewText": text,
                   "sentiment":label,
                   "unixReviewTime": int(time.time()),
                   "id": ID
                   }
    return data_object

def main():
    editor = Editor()
    adjpos = """ great fun lovely sexy wonderful amazing awesome good fantastic excelent masterful fabulous incredible salacious"""
    adjpos = adjpos.strip().split()
    adjneg = """terrible horrible shitty worst disasterous bad abominable atrocious crappy repulsive yucky irredeemable"""
    adjneg = adjneg.strip().split()
    
    rev_neg_pos = "some parts are {pos} but overall it is {neg}."
    rev_pos_neg = "some parts are {neg} but overall it is {pos}."

    final_data = []
    id_counter = 0
    
    out_0 = editor.template(rev_neg_pos, pos=adjpos, neg=adjneg)
    #print(out_0)
    out_1 = editor.template(rev_pos_neg, pos=adjpos, neg=adjneg)
    #print(out_1)




    seed = 'I had a {neg} day really {neg} but the album made it {pos}'
    ous_0 = editor.template(seed, pos=adjpos, neg=adjneg)
    #print(ous_0)


    

    seed = 'I had a {pos} day really {pos} but the album made it {neg}'
    ous_1 = editor.template(seed, pos=adjpos, neg=adjneg)
    #print(ous_1)

    with open('../data/music_reviews_dev.json', 'r') as f:
        data = []
        for line in f.readlines():
            data.append(json.loads(line))
    data = random.sample(data, 100)

    tmp = []
    tmp_labels = []
    for d in data:
        tmp.append(d.get('reviewText'))
        tmp_labels.append(d.get('sentiment'))

    baseline = "{male} is my {religion_adj}, {sexual_adj} friend, and he showed me this song. I found it {pos}"
    ret_pos = editor.template(baseline,pos=adjpos)
    ret_neg = editor.template(baseline,pos=adjneg)
    
    for idx,entry in enumerate(random.sample(Perturb.perturb(tmp, Perturb.add_typos, keep_original=False).data,100)):
        final_data.append(to_json(entry[0],tmp_labels[idx],id_counter))
        id_counter += 1
        
    for entry in random.sample(out_0.data,100):
        final_data.append(to_json(entry,"negative",id_counter))
        id_counter += 1
    
    for entry in random.sample(out_1.data,100):
        final_data.append(to_json(entry,"positive",id_counter))
        id_counter += 1

    for entry in random.sample(ous_0.data,100):
        final_data.append(to_json(entry,"positive",id_counter))
        id_counter += 1

    for entry in random.sample(ous_1.data,100):
        final_data.append(to_json(entry,"negative",id_counter))
        id_counter += 1

    for entry in random.sample(ret_pos.data,100):
        final_data.append(to_json(entry,"positive",id_counter))
        id_counter += 1

    for entry in random.sample(ret_neg.data,100):
        final_data.append(to_json(entry,"negative",id_counter))
        id_counter += 1

    with open('../data/music_reviews_yucky.json','w') as file:
        for line in final_data:
            file.write(json.dumps(line))
            file.write("\n")

if __name__ == '__main__':
    main()