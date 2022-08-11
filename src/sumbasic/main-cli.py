import argparse
import pandas as pd
from tqdm import tqdm
import os

from src.inference import summarize


def process_batch(input_path):
    os.makedirs('output', exist_ok=True)
    for idx, df in enumerate(pd.read_json(input_path, lines=True, chunksize=1000)):
        generated_summaries = []
        for text in tqdm(df['text']):
            summary = summarize(text)
            generated_summaries.append(summary)
        df['sumbasic'] = generated_summaries
        df.to_json(f'output/{idx}.jsonl', lines=True, orient='records', force_ascii=False)


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
