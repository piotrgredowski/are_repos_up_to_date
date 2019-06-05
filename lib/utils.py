import os

import yaml
from jinja2 import Template


def read_yaml_file(path):
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


class Repo:
    def __init__(self, path, branch='master'):
        self.path = self._validate_path(path)
        self.branch = branch
        self.can_ff = False

    def _validate_path(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        return path

def get_repos_and_wrong_paths(path):
    repos = []
    not_existing_paths = []
    for repo in read_yaml_file(path):
        try:
            r = Repo(**repo)
        except FileNotFoundError:
            not_existing_paths.append(repo['path'])
        else:
            repos.append(r)
    return repos, not_existing_paths

def _get_environ_variable(name):
    return os.environ.get(name)


def get_username():
    return _get_environ_variable('USER')


def get_display():
    return _get_environ_variable('DISPLAY')


def get_uid():
    return os.getuid()


def load_template(path: str):
    with open(path) as f:
        template = Template(f.read())
    return template


def save_to_file(data, path):
    with open(path, 'w') as f:
        f.write(data)
