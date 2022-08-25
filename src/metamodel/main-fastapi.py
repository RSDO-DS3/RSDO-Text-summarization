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


class Item(BaseModel):
    text: str

app = FastAPI()

ports = {
    'metamodel': 8000,
    'graph-based': 8001,
    't5-headline': 8002,
    't5-article': 8003,
    'sumbasic': 8004,
    'hybrid-long': 8005
}

# load d2v model and other requirements
fname = "model/doc2vec/model"
d2v_model = Doc2Vec.load(fname)
lem_sl = Lemmatizer('sl')
stopwords = set(stopwords.words('slovene'))

# load metamodel
metamodel = keras.models.load_model('model/metamodel/model.h5')

@app.post("/auto-select/")
async def select_model(item: Item):
    text = item.text

    # predict
    preprocessed_text = filter_text(text, lem_sl, stopwords).split()
    sum_model = get_recommended_model(d2v_model, metamodel, preprocessed_text)
    print(sum_model)

    # get port of model
    model_port = ports[sum_model]

    # print url of a model
    url = f'http://{sum_model}:{str(model_port)}/summarize/'
    print("Sending text to ", url)

    # send text
    body = {
        "text": text,
    }

    body_json = json.dumps(body, ensure_ascii=False).encode('utf8')
    response = requests.post(url, data=body_json)
    json_obj = json.dumps(json.loads(response.text), ensure_ascii=False)

    return json_obj
