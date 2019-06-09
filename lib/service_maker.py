import os
from sys import platform

from jinja2 import Template

from lib import utils


class ServiceMaker:
    def __init__(self, root_dir):
        self.consts = utils.read_yaml_file(os.path.join(root_dir, "consts.yaml"))
        self.platform = platform
        self.service_template = None
        self.rendered_template = None

    def load_template(self):
        path_to_template = self.consts.get("service_template_path").get(self.platform)
        with open(path_to_template) as f:
            self.service_template = Template(f.read())

    def render_template(self, **kwargs):
        self.rendered_template = self.service_template.render(**kwargs)

    def save_template(self):
        path_for_rendered_template = self.consts.get("service_rendered_path").get(
            self.platform
        )
        with open(path_for_rendered_template, "w") as f:
            f.write(self.rendered_template)
