import argparse
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import torch
import os

from transformers import T5Tokenizer, T5ForConditionalGeneration

from src.inference import summarize


def process_batch(input_path, abs_tokenizer, abs_model, ext_model, device):
    os.makedirs('output', exist_ok=True)
    for idx, df in enumerate(pd.read_json(input_path, lines=True, chunksize=1000)):
        generated_summaries = []
        for text in tqdm(df['text']):
            summary = summarize(abs_tokenizer, abs_model, ext_model, text, device)
            generated_summaries.append(summary)
        df['hybrid-long'] = generated_summaries
        df.to_json(f'output/{idx}.jsonl', lines=True, orient='records', force_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hybrid-long')
    parser.add_argument('--text', type=str, help='text to generate a summary from')
    parser.add_argument('--input_path', type=str, help='file to generate summaries')

    args = parser.parse_args()

    text = args.text
    input_path = args.input_path
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(device)

    # import models
    ext_model_path = 'model/LaBSE'
    ext_model = SentenceTransformer(ext_model_path)

    abs_model_path = 'model/SloT5-cnndm_slo_pretraining'
    abs_tokenizer = T5Tokenizer.from_pretrained(abs_model_path)
    abs_model = T5ForConditionalGeneration.from_pretrained(abs_model_path).to(device)

    # run main
    if input_path:
        texts = process_batch(input_path, abs_tokenizer, abs_model, ext_model, device)
    elif text:
        summary = summarize(abs_tokenizer, abs_model, ext_model, text, device)
        print(summary)
    else:
        print('None of the arguments were given')
