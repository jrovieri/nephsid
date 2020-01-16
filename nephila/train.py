# -*- coding: utf-8 -*-
import csv
import random
from pathlib import Path

import pymongo
import spacy
from spacy.strings import hash_string
from spacy.util import minibatch, compounding

from language.pt import Portuguese


client = pymongo.MongoClient()
scrapdb = client['scrappeddata']
traindb = client['train']

field2sent = ['name', 'recipeIngredient']
base = Path('../data')

VALID_BILOU_TAGS = [
    'U-PRODUCT', 'B-PRODUCT', 'I-PRODUCT', 'L-PRODUCT',
    'U-QUANTITY', 'B-QUANTITY', 'I-QUANTITY', 'L-QUANTITY',
    'U-CARDINAL', 'B-CARDINAL', 'I-CARDINAL', 'L-CARDINAL',
    'O']

def add_sentences(source):
    # Create sentences from scrapped items

    for doc in scrapdb[source].find():
        for key, value in doc.items():
            if key not in field2sent:
                continue

            for text in list(value):
                try:
                    traindb['sentence'].insert({
                        '_id': 'S{}'.format(str(hash_string(text.lower()))),
                        'language': doc['language'],
                        'source': doc['isPartOf'],
                        'subject': 'cookery',
                        'text': text.lower()
                    })
                except pymongo.errors.DuplicateKeyError:
                    continue

def save_train_file(filename, subject, n_sent):
    # Creates a csv file with sentences to train
    tokenizer = Portuguese()

    sentences = [(doc['_id'], doc['text'])
        for doc in traindb['sentence'].find({
            'subject': subject,
            'train': {
                '$exists': False}})]

    random.shuffle(sentences)

    path = '../data/{}.csv'.format(filename)
    with open(path, mode='w', encoding='utf8') as f:
        writer = csv.writer(f,
            delimiter='|',
            quotechar='@',
            quoting=csv.QUOTE_ALL)

        for identifier, text in sentences[0:n_sent]:
            doc = tokenizer(text)
            row = [identifier]
            [row.append(word) for word in doc]

            writer.writerow(row)
            writer.writerow([])

def generate_train_file(filename):
    path = base.joinpath(filename)

    with path.open('r', encoding='utf8') as f:
        reader = csv.reader(f, delimiter='|', quotechar='@')
        data = [row for row in reader]

    train_data = zip(data[0:][::2], data[1:][::2])
    for index, (tokens, tags) in enumerate(train_data):
        _id = tokens.pop(0)

        line = (index + 1) * 2

        tokens = [token for token in tokens if token]
        tags = [tag for tag in tags if tag]

        yield (line, _id, tokens, tags)

def validate_train_file(filename):
    # No typing mistakes
    tokenizer = Portuguese()

    errors = 0
    for line, _id, tokens, tags in generate_train_file(filename):
        sentence = traindb['sentence'].find_one({'_id': _id})

        if not sentence:
            print("Line {} - Sentence not found: '{}'".format(line, _id))
            errors += 1
            continue

        doc = tokenizer(sentence['text'])
        _tokens = [word.text for word in doc]

        if not len(_tokens) == len(tags):
            print("Line {} - Incorrect vector size".format(line))
            errors += 1
            continue

        for tag in tags:
            if not tag in VALID_BILOU_TAGS:
                print("Line {} - Invalid tag: '{}'").format(line, tag)
                errors += 1

    return not(bool(errors))

def load_train_file(filename):
    # Updates sentence collection with trained data

    if not validate_train_file(filename):
        exit(1)

    for _, _id, tokens, tags in generate_train_file(filename):
        traindb['sentence'].update_one({'_id': _id}, {
            '$set': {
                'train.tokens': tokens,
                'train.tags': tags
            }
        })


def train(subject, n_sent, n_iter):
    # Creates or updates the NER model for a subject

    train_data = []
    for doc in traindb['sentence'].find({'subject': subject,
            'train': {'$exists': True}}).limit(n_sent):
        train_data.append((doc['text'], {'entities': doc['train']['tags']}))

    path = base.joinpath(subject)
    if path.exists():
        nlp = spacy.load(path)
        ner = nlp.get_pipe('ner')
    else:
        nlp = Portuguese()
        ner = nlp.create_pipe('ner')
        ner.add_label('CARDINAL')
        ner.add_label('QUANTITY')
        ner.add_label('PRODUCT')

        nlp.add_pipe(ner, last=True)
        nlp.begin_training()

    for itn in range(n_iter):
        random.shuffle(train_data)

        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))

        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, drop=0.5, losses=losses,)
            print("Losses", losses)

    nlp.to_disk(path)
