import distutils.sysconfig
import os

from lib import utils


class SystemInfo:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.consts = utils.read_yaml_file(os.path.join(root_dir, "consts.yaml"))

    @staticmethod
    def _get_environ_variable(name):
        return os.environ.get(name)

    @property
    def username(self):
        return self._get_environ_variable("USER")

    @property
    def display(self):
        return self._get_environ_variable("DISPLAY")

    @staticmethod
    @property
    def user_uid():
        return os.getuid()

    @property
    def path_to_main_script(self):
        return os.path.join(self.root_dir, self.consts.get("main_script_name"))

    @property
    def path_to_script_dir(self):
        return os.path.abspath(os.path.join(self.path_to_main_script, ".."))

    @property
    def path_to_repos_list_file(self):
        return os.path.join(self.root_dir, self.consts.get("repos_list_filename"))

    @property
    def global_site_packages_path(self):
        return distutils.sysconfig.get_python_lib()

    @property
    def venv_python_path(self):
        return os.path.join(self.root_dir, self.consts.get("venv_python_path"))

