import argparse

from transformers import T5ForConditionalGeneration, T5Tokenizer

from src.inference import summarize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='T5 headline generation.')
    parser.add_argument('--text', required=True, type=str, help='text to generate a headline from')

    args = parser.parse_args()

    text = args.text

    # import tokenizer and model
    model_path = 'models/SloT5-sta_headline'
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    # run main
    summary = summarize(tokenizer, model, text)
    print(summary)
