import json
import os
import sys

import numpy as np
import pandas as pd
import tensorflow as tf
import yaml
from sklearn.metrics import mean_squared_error
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


def train(data, embeddings):
    # get and prepare data
    print('Retrieving data ... ')
    train = pd.read_json(os.path.join(data, 'train.jsonl'), lines=True)
    val = pd.read_json(os.path.join(data, 'val.jsonl'), lines=True)
    test = pd.read_json(os.path.join(data, 'test.jsonl'), lines=True)

    train_vectors = np.load(os.path.join(embeddings, 'embeddings-train.npy'))
    val_vectors = np.load(os.path.join(embeddings, 'embeddings-val.npy'))
    test_vectors = np.load(os.path.join(embeddings, 'embeddings-test.npy'))
    print('Retrieved.')

    X_train = np.array(train_vectors)
    X_val = np.array(val_vectors)
    X_test = np.array(test_vectors)

    y_train = np.array(train.filter(regex='rouge'))
    y_val = np.array(val.filter(regex='rouge'))
    y_test = np.array(test.filter(regex='rouge'))

    # params
    tree = yaml.safe_load(open('params.yaml'))['tree']
    forest = yaml.safe_load(open('params.yaml'))['forest']

    # build tree model
    print('Training tree regressor ...')
    tree_regressor = DecisionTreeRegressor(random_state=0,
                                           min_samples_split=tree['min_samples_split'],
                                           min_samples_leaf=tree['min_samples_leaf']
                                           )
    tree_regressor.fit(X_train, y_train)

    # predict on test set
    y_pred = tree_regressor.predict(X_test)
    results = {'mse_test': mean_squared_error(y_test, y_pred)}

    with open('tree-metrics.json', 'w') as outfile:
        json.dump(results, outfile)

    # build random forest model
    print('Training forest regressor ...')
    forest_regressor = RandomForestRegressor(n_jobs=16,
                                             verbose=1,
                                             n_estimators=forest['n_estimators'],
                                             min_samples_split=forest['min_samples_split'],
                                             min_samples_leaf=forest['min_samples_leaf']
                                             )
    forest_regressor.fit(X_train, y_train)

    # predict on test set
    y_pred = forest_regressor.predict(X_test)
    results = {'mse_test': mean_squared_error(y_test, y_pred)}

    print(results)

    with open('forest-metrics.json', 'w') as outfile:
        json.dump(results, outfile)


if __name__ == '__main__':
    data = sys.argv[1]
    embeddings = sys.argv[2]
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.makedirs('model/metamodel', exist_ok=True)

    train(data, embeddings)
