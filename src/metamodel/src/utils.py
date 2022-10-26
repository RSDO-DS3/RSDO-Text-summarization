import yaml


def load_params():
    params = yaml.safe_load(open("/home/azagar/myfiles/metamodel/params.yaml"))
    return params