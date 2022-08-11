import argparse
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os
import torch

from transformers import T5Tokenizer, T5ForConditionalGeneration

from src.inference import summarize


def process_batch(input_path, tokenizer, model, device):
    os.makedirs('output', exist_ok=True)
    for idx, df in enumerate(pd.read_json(input_path, lines=True, chunksize=1000)):
        generated_summaries = []
        for text in tqdm(df['text']):
            summary = summarize(tokenizer, model, text, device)
            generated_summaries.append(summary)
        df['t5-article'] = generated_summaries
        df.to_json(f'output/{idx}.jsonl', lines=True, orient='records', force_ascii=False)


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
