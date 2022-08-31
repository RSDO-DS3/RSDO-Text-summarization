from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from transformers import T5ForConditionalGeneration, T5Tokenizer

from src.inference import summarize


class Item(BaseModel):
    text: str

app = FastAPI()

# import models
ext_model_path = 'model/LaBSE'
ext_model = SentenceTransformer(ext_model_path, device='cpu')

abs_model_path = 'model/SloT5-cnndm_slo_pretraining'
abs_tokenizer = T5Tokenizer.from_pretrained(abs_model_path)
abs_model = T5ForConditionalGeneration.from_pretrained(abs_model_path)

@app.post("/summarize/")
async def generate_summary(item: Item):
    summary = summarize(abs_tokenizer, abs_model, ext_model, item.text, 'cpu')
    return {'summary': summary,
            'model': 'hybrid-long',
            }