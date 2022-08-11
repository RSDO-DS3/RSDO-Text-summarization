import argparse

from src.inference import summarize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SumBasic')
    parser.add_argument('--text', required=True, type=str, help='text to generate a summary from')

    args = parser.parse_args()

    text = args.text

    # run main
    summary = summarize(text)
    print(summary)
