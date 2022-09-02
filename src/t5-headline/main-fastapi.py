from fastapi import FastAPI
from pydantic import BaseModel

from transformers import T5ForConditionalGeneration, T5Tokenizer

from src.inference import summarize


class Item(BaseModel):
    text: str

app = FastAPI()

# import model
model_path = 'model/SloT5-sta_headline'
tokenizer = T5Tokenizer.from_pretrained(model_path, local_files_only=True)
model = T5ForConditionalGeneration.from_pretrained(model_path, local_files_only=True)

@app.post("/summarize/")
async def generate_summary(item: Item):
    summary = summarize(tokenizer, model, item.text)
    return {'summary': summary,
            'model': 't5-headline'}