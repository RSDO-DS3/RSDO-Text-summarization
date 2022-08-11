import argparse
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os

from src.inference import summarize


def process_batch(input_path, model):
    df = pd.read_json(input_path, lines=True)
    generated_summaries = []
    for text in tqdm(df['text']):
        summary = summarize(model, text)
        generated_summaries.append(summary)
    df['graph-based'] = generated_summaries
    df.to_json('graph-based.jsonl', lines=True, orient='records', force_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Graph-based')
    parser.add_argument('--text', type=str, help='text to generate a summary from')
    parser.add_argument('--input_path', type=str, help='file to generate summaries')

    args = parser.parse_args()

    text = args.text
    input_path = args.input_path

    # import model
    model_name = 'model/LaBSE'
    model = SentenceTransformer(model_name)

    # run main
    if input_path:
        texts = process_batch(input_path, model)
    elif text:
        summary = summarize(model, text)
        print(summary)
    else:
        print('None of the arguments were given')
