import argparse

from sentence_transformers import SentenceTransformer

from src.inference import summarize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Graph-based text summarization.')
    parser.add_argument('--text', required=True, type=str, help='text to summarize')

    args = parser.parse_args()

    text = args.text

    # import model
    model_name = 'LaBSE'
    model = SentenceTransformer(model_name, device='cpu')

    # run main
    summary = summarize(model, text)
    print(summary)
