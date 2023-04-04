FROM python:3.8-slim-buster

ENV MODEL_PATH "model/SloT5-cnndm_slo_pretraining"

COPY . .

RUN pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html \
    --disable-pip-version-check

EXPOSE 5006

CMD ["uvicorn", "main-fastapi:app", "--host", "0.0.0.0", "--port", "5006"]