import json
import os

import pandas as pd
import yaml
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import sys


class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1


def train(training_data, output_model):
    print('Retrieving data ... ')
    df = pd.read_json(training_data, lines=True)

    texts = [text.split() for text in df['text']]
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(texts)]

    # train model
    p = yaml.safe_load(open('params.yaml'))['d2v']
    print('Model training ...')
    epoch_logger = EpochLogger()
    model = Doc2Vec(documents,
                    vector_size=p['vector_size'],
                    window=p['window'],
                    min_count=p['min_count'],
                    workers=p['workers'],
                    max_vocab_size=p['max_vocab_size'],
                    epochs=p['epochs'],
                    callbacks=[epoch_logger],
                    compute_loss=True
                    )

    # save model
    model.save(output_model)


if __name__ == '__main__':
    training_data = sys.argv[1]
    output_model = sys.argv[2]
    os.makedirs("/".join(output_model.split('/')[:2]), exist_ok=True)
    train(training_data, output_model)
