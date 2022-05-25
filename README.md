# Povzemanje besedil

V tem repozitoriju se nahaja rezultat aktivnosti A3.3 Orodje za povzemanje besedil, ki je nastalo v okviru projekta Razvoj slovenščine v digitalnem okolju.

# Available models
At the moment, 4 models are available in this repository (in the `src` folder): `graph-based`, `metamodel`, `t5-article`, and `t5-headline`. Each model can be run separately, or together with the `metamodel` (see the instructions below). The role of the metamodel is to automatically select the most appropriate summarization model, based on the analysis of the input text. 

# Download pre-trained models

Download models from https://nas.cjvt.si/index.php/s/Bpob8qZ64TY3LM3 and extract them into the folders with their source code. For example, the model `t5-article` should be extracted in the `src/t5-article/model` folder.

# Run locally

### Use each model separately
We suggest using virtual environments and python 3.8 for all models. Dependecies for each model can be installed with `pip install requirements.txt` from the root folder of models. After you installed all dependencies, you can run inference in two ways: 

1) Command-line interface: `python main-cli.py --text 'the content of an article'`
2) Uvicorn server: `uvicorn main-fastapi:app --host 0.0.0.0 --port xxxx`

You will find the details and examples of both ways in the `README.md` file of each model. 

### Use metamodel
To use the `metamodel`, you have to start each model as a uvicorn server with the following ports: 

| **Model**   | **Port** |
|-------------|----------|
| metamodel   | 8000     |
| graph-based | 8001     |
| t5-headline | 8002     |
| t5-article  | 8003     |

`main.sh` is an example of a script that automates the manual creation of uvicorn servers. 

After all four models are up and running, you can call only the metamodel, which will automatically select the best summarizer based on the analysis of the input text. You can find example requests in the `commands.sh` script. 

# Run with docker
Each model can be run with Docker as well. The instructions are in the `README.md` file of each model. 


