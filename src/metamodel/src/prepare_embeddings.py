import os
import string
import sys

import numpy as np
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from lemmagen3 import Lemmatizer
from nltk.corpus import stopwords
from tqdm import tqdm


def prepare_embeddings(data, stopwords, d2v_model, save_path):
    def filter_text(content):
        content_filtered = []
        for token in content.split():
            lemma = lem_sl.lemmatize(token)
            if lemma not in stopwords:
                content_filtered.append(lemma.lower())
        content_filtered = ' '.join(content_filtered)
        content_filtered = ''.join([i for i in content_filtered if not i.isdigit()])  # remove digits
        content_filtered = content_filtered.translate(str.maketrans('', '', string.punctuation))
        return content_filtered

    # load doc2vec model & load external tools
    lem_sl = Lemmatizer('sl')
    stopwords = set(stopwords.words('slovene'))
    model = Doc2Vec.load(d2v_model)

    # get and prepare data
    os.makedirs(save_path)
    for file in os.listdir(data):
        source = os.path.join(data, file)
        print('Retrieving data ... ')
        df = pd.read_json(source, lines=True)
        print('Retrieved.')

        # calculate embeddings
        doc_vectors = []
        for text in tqdm(df['text']):
            doc_vec = model.infer_vector(filter_text(text).split())
            doc_vectors.append(doc_vec)
        doc_vectors = np.array(doc_vectors)

        # save
        target = os.path.join(save_path, f'embeddings-{file.split(".")[0]}.npy')
        np.save(target, doc_vectors)  # .npy extension is added if not given


if __name__ == '__main__':
    data = sys.argv[1]
    d2v_model = sys.argv[2]
    embeddings = sys.argv[3]

    prepare_embeddings(data, stopwords, d2v_model=d2v_model, save_path=embeddings)
