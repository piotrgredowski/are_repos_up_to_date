import os

import yaml


def read_file(path):
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


class FileNotExistsError(BaseException):
    pass


class Repo:
    def __init__(self, path, branch='master'):
        self.path = self._validate_path(path)
        self.branch = branch

    def _validate_path(self, path):
        if not os.path.exists(path):
            raise FileNotExistsError
        return path
