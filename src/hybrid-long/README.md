# Local
To run this project, install python 3.8 and dependencies:
`pip3 install -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html`

### Run from command line
`python main-cli.py --text 'Marsikdo nam zavida hitrost pri oblikovanju koalicije, a volja ljudi je bila jasna. Če ne bi bila, se nam ne bi uspelo tako hitro dogovoriti, kateri so projekti, smeri in vrednote, ki jih bomo skupaj zagovarjali v prihodnji vladi, je ob podpisu pogodbe dejal verjetni mandatar in predsednik Gibanja Svoboda Robert Golob. Nove organizacije vlade, ki jo pogodba predvideva, še ne morejo takoj udejanjiti, saj jih je ustavil SDS-ov predlog za posvetovalni referendum o zakonu o vladi, a Golob zatrjuje, da bodo to storili v prihodnjih mesecih. Na videz se povečuje kompleksnost vlade, ker se dodajajo nova ministrstva, a v resnici so ta nova ministrstva namenjena ravno tistemu, kar bo našo vlado razlikovalo od prejšnjih. Namenjena so ustvarjanju novih priložnosti, projektov in znanj, je pojasnil. Z ministrstvom za visoko šolstvo, znanost in inovacije, ministrstvom za solidarno prihodnost in ministrstvom zeleni preboj bodo po njegovih besedah omogočili, da bo Slovenija kot država odporna proti spremembam, ki jih prinaša prihodnost. Tudi predsednica SD-ja Tanja Fajon je zatrdila, da so oblikovali vlado sprememb. Naš cilj je, da Sloveniji zagotovimo močno gospodarstvo, socialno varnost za vse, skladen regionalni razvoj in Slovenijo v jedru Evrope. Nova vlada bo usmerjena v dvig dodane vrednosti, v zeleni in digitalni prehod ter v močne javne storitve. Tudi v mednarodni politiki želimo vrniti ugled državi, kjer je bil ta poškodovan. Po besedah koordinatorja Levice Luke Mesca je bilo namreč zadnje desetletje desetletje izgubljenih priložnosti, ko je Slovenija prehajala iz krize v krizo. Ta koalicijska pogodba je za dva mandata, da do leta 2030 ljudem organiziramo državo, kakršno si zaslužijo, je dodal.'`

### Run server
 `uvicorn main-fastapi:app --host 0.0.0.0 --port 5008`
To test the service, try sending a request with the curl command provided in the file `commands.sh`

# Docker
`docker buildx build --platform linux/amd64 . -t hybrid-long -f Dockerfile`

`docker run --rm --platform linux/amd64 -it --name hybrid-long -p:5008:5008 hybrid-long`

