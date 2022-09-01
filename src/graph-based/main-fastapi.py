from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from src.inference import summarize


class Item(BaseModel):
    text: str

app = FastAPI()

# import model
model_path = './model/LaBSE'
model = SentenceTransformer(model_path, device='cpu')

@app.post("/summarize/")
async def generate_summary(item: Item):
    summary = summarize(model, item.text)
    return {'summary': summary,
            'model': 'graph-based'}
