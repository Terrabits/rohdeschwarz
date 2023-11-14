from ruamel.yaml import YAML


# init
yaml = YAML(typ='safe', pure=True)


def load_yaml(file):
    return yaml.load(file)
