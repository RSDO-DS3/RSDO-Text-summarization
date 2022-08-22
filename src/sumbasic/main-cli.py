import argparse
import pandas as pd
from tqdm import tqdm
import os
import json

from src.inference import summarize


def process_batch(input_path):
    os.makedirs('output', exist_ok=True)
    df = pd.read_json(input_path, lines=True)
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        example_id = row['id']
        if os.path.isfile(f'output/{example_id}.json'):
            continue
        summary = summarize(row['text'])
        out = {
            'id' : example_id,
            'sumbasic': summary,
            'text': row['text'],
            'abstract': row['abstract'],
            'source': row['source']
        }
        with open(f'output/{example_id}.json', 'w') as j:
            json.dump(out, j, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SumBasic')
    parser.add_argument('--text', type=str, help='text to generate a summary from')
    parser.add_argument('--input_path', type=str, help='file to generate summaries')

    args = parser.parse_args()

    text = args.text
    input_path = args.input_path

    # run main
    if input_path:
        texts = process_batch(input_path)
    elif text:
        summary = summarize(text)
        print(summary)
    else:
        print('None of the arguments were given')
