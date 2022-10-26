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
from sklearn.model_selection import train_test_split


def train(data, embeddings, model_save_path):
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
    p = yaml.safe_load(open('params.yaml'))['metamodel']

    # build model
    model = Sequential()
    model.add(Dense(p['hidden_layer_size'], input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(p['hidden_layer_size'], activation='relu'))
    model.add(Dense(y_train.shape[1]))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.summary()

    print(p['hidden_layer_size'])
    # define callback
    callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=p['patience'])

    # train
    history = model.fit(X_train, y_train,
                        batch_size=8,
                        epochs=100,
                        verbose=1,
                        validation_data=(X_val, y_val),
                        callbacks=[callback])

    # save or load model
    model.save(model_save_path)

    # predict on test set
    y_pred = model.predict(X_test)
    results = {'mse_test': mean_squared_error(y_test, y_pred)}

    # history
    metrics = {k: v[-1] for k, v in history.history.items()}
    metrics.update(results)
    with open('advanced-metrics.json', 'w') as outfile:
        json.dump(metrics, outfile)


if __name__ == '__main__':
    data = sys.argv[1]
    embeddings = sys.argv[2]
    model_save_path = sys.argv[3]
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    os.makedirs('model/metamodel', exist_ok=True)

    train(data, embeddings, model_save_path)
