import argparse
from transformers import T5ForConditionalGeneration, T5Tokenizer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='T5 lead generation.')
    parser.add_argument('--text', required=True, type=str, help='text to generate a headline from')

    args = parser.parse_args()

    text = args.text

    # import tokenizer and model
    model_path = 'model/SloT5-asn_plus_sta/checkpoint-170000'
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    # run main
    summary = summarize(tokenizer, model, text)
    print(summary)