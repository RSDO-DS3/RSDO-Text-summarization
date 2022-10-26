import argparse
import os
import re
import string
import uuid

import pandas as pd
from lemmagen3 import Lemmatizer
from nltk.corpus import stopwords
from tqdm import tqdm


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


def prepare_data_for_doc2vec():
    samples = []

    # get KAS
    for root, dirs, files in os.walk("/home/azagar/myfiles/kas_final/final/kas.corpus/kas.txt", topdown=False):
        for name in tqdm(files):
            if ".txt" in name:
                file_path = os.path.join(root, name)
                with open(file_path, 'r') as f:
                    content = f.read()
                    try:
                        content_filtered = filter_text(content)
                    except:
                        continue
                    samples.append({'text': content_filtered, 'id': str(uuid.uuid4()), 'source': 'kas'})

    # get STA+ASN
    root = '/home/azagar/myfiles/t5/data/asn-summary-plus-sta-lead'
    for mode in ['train.jsonl', 'val.jsonl', 'test.jsonl']:
        file = os.path.join(root, mode)
        df = pd.read_json(file, lines=True)
        for content in tqdm(df['text'].to_list()):
            try:
                content_filtered = filter_text(content)
            except:
                continue
            samples.append({'text': content_filtered, 'id': str(uuid.uuid4()), 'source': 'news'})

    # get SURS
    df = pd.read_json('/home/azagar/myfiles/metamodel/data/surs.jsonl', lines=True)
    for content in tqdm(df['KomentarSLO'].to_list()):
        try:
            content_filtered = filter_text(content)
        except:
            continue
        samples.append({'text': content_filtered, 'id': str(uuid.uuid4()), 'source': 'surs'})

    # export
    df = pd.DataFrame(samples)
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_json('/home/azagar/myfiles/metamodel/data/doc2vec-training.jsonl', lines=True, orient='records', force_ascii=False)


def prepare_data_for_metamodel():
    samples = []

    # get KAS texts and abstracts
    abstracts = '/home/azagar/myfiles/kas_final/final/kas.abstracts'
    bodies = "/home/azagar/myfiles/kas_final/final/kas.corpus/kas.txt"
    for root, dirs, files in os.walk(bodies, topdown=False):
        for name in tqdm(files):
            if ".txt" in name:
                file_idx = re.search('\d+', name).group(0)

                body_path = os.path.join(root, name)
                abstract_path = os.path.join(abstracts, file_idx[-3:], f'kas-{file_idx}-abs-sl.txt')
                if os.path.isfile(abstract_path):
                    with open(body_path, 'r') as b, open(abstract_path, 'r') as a:
                        body = b.read()
                        abstract = a.read()

                        samples.append({'text': body, 'abstract': abstract, 'id': str(uuid.uuid4()), 'source': 'kas'})

    # get STA+ASN
    root = '/home/azagar/myfiles/t5/data/asn-summary-plus-sta-lead'
    for mode in ['train.jsonl', 'val.jsonl', 'test.jsonl']:
        file = os.path.join(root, mode)
        df = pd.read_json(file, lines=True)
        for text, abstract in tqdm(zip(df['text'], df['lead']), total=len(df)):
            samples.append({'text': text, 'abstract': abstract, 'id': str(uuid.uuid4()), 'source': 'news'})

    # get SURS
    df = pd.read_json('/home/azagar/myfiles/metamodel/data/surs.jsonl', lines=True)
    for text, abstract in tqdm(zip(df['KomentarSLO'], df['PovzetekSLO']), total=len(df)):
        samples.append({'text': text, 'abstract': abstract, 'id': str(uuid.uuid4()), 'source': 'surs'})

    # export
    df = pd.DataFrame(samples)
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_json('/home/azagar/myfiles/metamodel/data/metamodel-training.jsonl', lines=True, orient='records', force_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='prepare data for both models')
    parser.add_argument('--model', type=str, help='text to generate a summary from')

    args = parser.parse_args()

    model = args.model

    # load external tools
    lem_sl = Lemmatizer('sl')
    stopwords = set(stopwords.words('slovene'))

    # start additional parameters
    if model == 'd2v':
        prepare_data_for_doc2vec()
    elif model == 'metamodel':
        prepare_data_for_metamodel()
