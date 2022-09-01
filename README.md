# Povzemanje besedil

V tem repozitoriju se nahaja rezultat aktivnosti A3.4 - R3.4.1 Orodje za povzemanje besedil, ki je nastalo v okviru projekta Razvoj slovenščine v digitalnem okolju.

# Available models
At the moment, 6 models are available in this repository (in the `src` folder): `graph-based`, `metamodel`, `t5-article`, `t5-headline`, `hybrid-long`, and `sumbasic`. Each model can be run separately, or together with the `metamodel` (see the instructions below). The role of the metamodel is to automatically select the most appropriate summarization model, based on the analysis of the input text. 

A brief description of models: 

| **Model**       | **Description**                                                                                                |
|-----------------|----------------------------------------------------------------------------------------------------------------|
| metamodel       | neural model based on the Doc2Vec document representation (`docs/metamodel.pdf`), suggests the best summarizer |
| graph-based [1] | unsupervised extractive approach, graph-based, returns `n` most important sentences                            |
| t5-headline     | supervised abstractive approach, transformer-based, returns headlines                                          |
| t5-article      | supervised abstractive approach, transformer-based, returns short summaries                                    |
| sumbasic        | unsupervised, simple summarizer that works with word frequencies, returns `n` most important sentences         |
| hybrid-long     | unsupervised hybrid approach, graph-based & transformer-base, returns short summaries of long texts            |


# Download pre-trained models

Download models from [link](https://nas.cjvt.si/index.php/s/Bpob8qZ64TY3LM3) and extract them into the folders with their source code. For example, the model `t5-article` should be extracted in the `src/t5-article/model` folder.

# Run locally

### Use each model separately
We suggest using virtual environments and python 3.8 for all models. Dependencies for each model can be installed with `pip install -r requirements.txt` from the root folder of models. After you installed all dependencies, you can run inference in two ways: 

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
| sumbasic    | 8004     |
| hybrid-long | 8005     |

`main.sh` is an example of a script that automates the manual creation of uvicorn servers. 

After all six models are up and running, you can call only the metamodel, which will automatically select the best summarizer based on the analysis of the input text. You can find example requests in the `commands.sh` script in each . 

# Run a docker
Models can be run with Docker as well. The instructions are in the `README.md` file of each model. 

# Run a docker-compose
This is the most straightforward method to run the project, but requires the most resources. First, make sure that you have downloaded and extracted pre-trained models to the specified folders. Next, run `docker-compose up`. This will build the environment defined in the `docker-compose.yml` file. It will take some time to build the full environment. After that, you can call the metamodel or single models. For example, to call the metamodel, use the following command:

`curl -X POST --location "http://localhost:8000/auto-select/" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Marsikdo nam zavida hitrost pri oblikovanju koalicije, a volja ljudi je bila jasna. Če ne bi bila, se nam ne bi uspelo tako hitro dogovoriti, kateri so projekti, smeri in vrednote, ki jih bomo skupaj zagovarjali v prihodnji vladi, je ob podpisu pogodbe dejal verjetni mandatar in predsednik Gibanja Svoboda Robert Golob. Nove organizacije vlade, ki jo pogodba predvideva, še ne morejo takoj udejanjiti, saj jih je ustavil SDS-ov predlog za posvetovalni referendum o zakonu o vladi, a Golob zatrjuje, da bodo to storili v prihodnjih mesecih. Na videz se povečuje kompleksnost vlade, ker se dodajajo nova ministrstva, a v resnici so ta nova ministrstva namenjena ravno tistemu, kar bo našo vlado razlikovalo od prejšnjih. Namenjena so ustvarjanju novih priložnosti, projektov in znanj, je pojasnil. Z ministrstvom za visoko šolstvo, znanost in inovacije, ministrstvom za solidarno prihodnost in ministrstvom zeleni preboj bodo po njegovih besedah omogočili, da bo Slovenija kot država odporna proti spremembam, ki jih prinaša prihodnost. Tudi predsednica SD-ja Tanja Fajon je zatrdila, da so oblikovali vlado sprememb. Naš cilj je, da Sloveniji zagotovimo močno gospodarstvo, socialno varnost za vse, skladen regionalni razvoj in Slovenijo v jedru Evrope. Nova vlada bo usmerjena v dvig dodane vrednosti, v zeleni in digitalni prehod ter v močne javne storitve. Tudi v mednarodni politiki želimo vrniti ugled državi, kjer je bil ta poškodovan. Po besedah koordinatorja Levice Luke Mesca je bilo namreč zadnje desetletje desetletje izgubljenih priložnosti, ko je Slovenija prehajala iz krize v krizo. Ta koalicijska pogodba je za dva mandata, da do leta 2030 ljudem organiziramo državo, kakršno si zaslužijo, je dodal.\" }"`

To call a single model, check the specified ports defined above and use the following command, e.g., `t5-headline`: 

`curl -X POST --location "http://localhost:8002/summarize/" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Marsikdo nam zavida hitrost pri oblikovanju koalicije, a volja ljudi je bila jasna. Če ne bi bila, se nam ne bi uspelo tako hitro dogovoriti, kateri so projekti, smeri in vrednote, ki jih bomo skupaj zagovarjali v prihodnji vladi, je ob podpisu pogodbe dejal verjetni mandatar in predsednik Gibanja Svoboda Robert Golob. Nove organizacije vlade, ki jo pogodba predvideva, še ne morejo takoj udejanjiti, saj jih je ustavil SDS-ov predlog za posvetovalni referendum o zakonu o vladi, a Golob zatrjuje, da bodo to storili v prihodnjih mesecih. Na videz se povečuje kompleksnost vlade, ker se dodajajo nova ministrstva, a v resnici so ta nova ministrstva namenjena ravno tistemu, kar bo našo vlado razlikovalo od prejšnjih. Namenjena so ustvarjanju novih priložnosti, projektov in znanj, je pojasnil. Z ministrstvom za visoko šolstvo, znanost in inovacije, ministrstvom za solidarno prihodnost in ministrstvom zeleni preboj bodo po njegovih besedah omogočili, da bo Slovenija kot država odporna proti spremembam, ki jih prinaša prihodnost. Tudi predsednica SD-ja Tanja Fajon je zatrdila, da so oblikovali vlado sprememb. Naš cilj je, da Sloveniji zagotovimo močno gospodarstvo, socialno varnost za vse, skladen regionalni razvoj in Slovenijo v jedru Evrope. Nova vlada bo usmerjena v dvig dodane vrednosti, v zeleni in digitalni prehod ter v močne javne storitve. Tudi v mednarodni politiki želimo vrniti ugled državi, kjer je bil ta poškodovan. Po besedah koordinatorja Levice Luke Mesca je bilo namreč zadnje desetletje desetletje izgubljenih priložnosti, ko je Slovenija prehajala iz krize v krizo. Ta koalicijska pogodba je za dva mandata, da do leta 2030 ljudem organiziramo državo, kakršno si zaslužijo, je dodal.\" }"`


 ---

# References
[1] Aleš Žagar and Marko Robnik-Šikonja. 2021. [Unsupervised Approach to Multilingual User Comments Summarization](https://aclanthology.org/2021.hackashop-1.13). In Proceedings of the EACL Hackashop on News Media Content Analysis and Automated Report Generation, pages 89–98, Online. Association for Computational Linguistics.

> Operacijo Razvoj slovenščine v digitalnem okolju sofinancirata Republika Slovenija in Evropska unija iz Evropskega sklada za regionalni razvoj. Operacija se izvaja v okviru Operativnega programa za izvajanje evropske kohezijske politike v obdobju 2014-2020.

![](Logo_EKP_sklad_za_regionalni_razvoj_SLO_slogan.jpg)