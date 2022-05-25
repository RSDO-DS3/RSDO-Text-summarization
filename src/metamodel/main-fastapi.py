from fastapi import FastAPI
from pydantic import BaseModel
import requests
import subprocess
import json


class Item(BaseModel):
    text: str

app = FastAPI()

ports = {
    'metamodel': 8000,
    'graph-based': 8001,
    't5-headline': 8002,
    't5-article': 8003
}

@app.post("/auto-select/")
async def select_model(item: Item):
    text = item.text
    if len(text.split()) > 350:
        model = 'graph-based'
    else:
        model = 't5-headline'

    model_port = ports[model]

    url = f'http://{model}:{str(model_port)}/summarize/'
    print(url)

    body = {
        "text": text,
    }

    body_json = json.dumps(body, ensure_ascii=False).encode('utf8')
    response = requests.post(url, data=body_json)
    json_obj = json.dumps(json.loads(response.text), ensure_ascii=False)

    return json_obj