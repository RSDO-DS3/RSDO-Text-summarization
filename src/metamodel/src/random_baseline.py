import json
import os
import sys

import pandas as pd
from sklearn.metrics import mean_squared_error


def mean_predict(train, test):
    # get and prepare data
    print('Retrieving data ... ')
    train = pd.read_json(train, lines=True)
    test = pd.read_json(test, lines=True)
    print('Retrieved.')

    y_train = train.filter(regex='rouge')
    y_test = test.filter(regex='rouge')

    # random predict
    y_pred = pd.concat([y_train.mean(axis=0).to_frame().T] * len(y_test)).reset_index(drop=True)
    results = {'mse_test': mean_squared_error(y_test, y_pred)}

    with open('baseline-metrics.json', 'w') as outfile:
        json.dump(results, outfile)


if __name__ == '__main__':
    train = sys.argv[1]
    test = sys.argv[2]

    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    mean_predict(train, test)
