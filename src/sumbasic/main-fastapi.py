from fastapi import FastAPI
from pydantic import BaseModel

from src.inference import summarize


class Item(BaseModel):
    text: str

app = FastAPI()

@app.post("/summarize/")
async def generate_summary(item: Item):
    summary = summarize(item.text)
    return {'summary': summary,
            'model': 'sumbasic'}