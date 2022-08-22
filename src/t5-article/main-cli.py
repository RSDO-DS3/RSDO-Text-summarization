import argparse
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os
import torch
import json

from transformers import T5Tokenizer, T5ForConditionalGeneration

from src.inference import summarize


def process_batch(input_path, tokenizer, model, device):
    os.makedirs('output', exist_ok=True)
    df = pd.read_json(input_path, lines=True)
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        example_id = row['id']
        if os.path.isfile(f'output/{example_id}.json'):
            continue
        summary = summarize(tokenizer, model, row['text'], device)
        out = {
            'id' : example_id,
            't5-article': summary,
            'text': row['text'],
            'abstract': row['abstract'],
            'source': row['source']
        }
        with open(f'output/{example_id}.json', 'w') as j:
            json.dump(out, j, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='t5-article')
    parser.add_argument('--text', type=str, help='text to generate a summary from')
    parser.add_argument('--input_path', type=str, help='file to generate summaries')

    args = parser.parse_args()

    text = args.text
    input_path = args.input_path
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # import tokenizer and model
    model_path = 'model/SloT5-cnndm_slo_pretraining'
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)

    # run main
    if input_path:
        texts = process_batch(input_path, tokenizer, model, device)
    elif text:
        summary = summarize(tokenizer, model, text, device)
        print(summary)
    else:
        print('None of the arguments were given')
