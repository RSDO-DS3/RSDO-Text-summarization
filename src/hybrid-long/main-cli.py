import argparse

from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer

from src.inference import summarize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hybrid summarizer for long texts.')
    parser.add_argument('--text', required=True, type=str, help='text to generate a summary of')

    args = parser.parse_args()

    text = args.text

    # import models
    ext_model_path = 'model/LaBSE'
    ext_model = SentenceTransformer(ext_model_path, device='cpu')

    abs_model_path = 'model/SloT5-cnndm_slo_pretraining'
    abs_tokenizer = T5Tokenizer.from_pretrained(abs_model_path)
    abs_model = T5ForConditionalGeneration.from_pretrained(abs_model_path)

    # run main
    summary = summarize(abs_tokenizer, abs_model, ext_model, text)
    print(summary)
