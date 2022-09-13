FROM python:3.8-slim-buster

COPY . .

RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader punkt stopwords

EXPOSE 5007

CMD ["uvicorn", "main-fastapi:app", "--host", "0.0.0.0", "--port", "5007"]