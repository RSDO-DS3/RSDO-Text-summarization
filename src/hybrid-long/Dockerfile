FROM python:3.8-slim-buster

COPY . .

RUN pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN python -m nltk.downloader punkt

EXPOSE 8005

CMD ["uvicorn", "main-fastapi:app", "--host", "0.0.0.0", "--port", "8005"]