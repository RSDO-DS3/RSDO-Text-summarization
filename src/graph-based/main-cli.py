import argparse

from sentence_transformers import SentenceTransformer

from src.inference import summarize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Graph-based text summarization.')
    parser.add_argument('--text', required=True, type=str, help='text to summarize')
    parser.add_argument('--n', required=False, type=int, default=2, help='number of returned sentences')

    args = parser.parse_args()

    text = args.text
    n = args.n

    # import model
    model_name = 'LaBSE'
    model = SentenceTransformer(model_name, device='cpu')

    # run main
    summary = summarize(model, text, n)
    print(summary)
