from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
from gensim.models.doc2vec import Doc2Vec
from lemmagen3 import Lemmatizer
from nltk.corpus import stopwords
from src.inference import get_recommended_model, filter_text
from tensorflow import keras
import uvicorn
import nltk
nltk.download('stopwords')


class Item(BaseModel):
    text: str

app = FastAPI()

ports = {
    'metamodel': 5003,
    'graph-based': 5004,
    't5-headline': 5005,
    't5-article': 5006,
    'sumbasic': 5007,
    'hybrid-long': 5008
}

# load d2v model and other requirements
fname = "./model/doc2vec/model"
d2v_model = Doc2Vec.load(fname)
lem_sl = Lemmatizer('sl')
stopwords = set(stopwords.words('slovene'))

# load metamodel
metamodel = keras.models.load_model('./model/metamodel/model.h5')

@app.post("/auto-select/")
async def select_model(item: Item):
    text = item.text

    # predict
    preprocessed_text = filter_text(text, lem_sl, stopwords).split()
    ranked_models = get_recommended_model(d2v_model, metamodel, preprocessed_text)
    print(ranked_models)

    for config in ['local', 'docker']:
        for sum_model in ranked_models:
            # get port of model
            model_port = ports[sum_model]

            # local and docker addresses differ
            if config == 'local':
                url = f'http://localhost:{str(model_port)}/summarize/'
                print("Sending text to ", url)
            else:
                url = f'http://{sum_model}:{str(model_port)}/summarize/'
                print("Sending text to ", url)

            # send text
            body = {
                "text": text,
            }

            body_json = json.dumps(body, ensure_ascii=False).encode('utf8')
            try:
                response = requests.post(url, data=body_json)
                json_obj = json.loads(response.text)
                return json_obj

            except requests.exceptions.ConnectionError:
                # print('Model is not available.')
                continue

    return {'summary': 'Missing summary!',
            'model': 'No available models!'}

