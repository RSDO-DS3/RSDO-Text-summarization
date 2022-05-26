# Local
To run this project, install python 3.8 and dependencies:
`pip3 install -r requirements.txt`

### Run server
 `uvicorn main-fastapi:app --host 0.0.0.0 --port 8000`
To test the service, try sending a request with the curl command provided in the file `commands.sh`

# Docker
`docker build . -t metamodel -f Dockerfile`

`docker run --rm -it --name metamodel -p:8000:8000 metamodel`

