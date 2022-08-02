import argparse

from src.inference import summarize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SumBasic')
    parser.add_argument('--text', required=True, type=str, help='text to generate a summary from')
    parser.add_argument('--n', required=False, type=int, default=2, help='number of returned sentences')

    args = parser.parse_args()

    text = args.text
    n = args.n

    # run main
    summary = summarize(text, n)
    print(summary)
