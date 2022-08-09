from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from src.inference import summarize


class Item(BaseModel):
    text: str

app = FastAPI()

# import model
model_name = 'LaBSE'
model = SentenceTransformer('model/LaBSE', device='cpu')

@app.post("/summarize/")
async def generate_summary(item: Item):
    summary = summarize(model, item.text, 3)
    return {'summary': summary,
            'model': 'graph-based'}
