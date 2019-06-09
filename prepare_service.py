#!/usr/bin/env python3

import os

from lib import ServiceMaker
from lib import SystemInfo

curr_dir = os.path.dirname(os.path.realpath(__file__))


def make_service():
    service_maker = ServiceMaker(root_dir=curr_dir)
    service_maker.load_template()
    info = SystemInfo(root_dir=curr_dir)
    service_maker.render_template(
        path_to_script=info.path_to_main_script,
        path_to_script_dir=info.path_to_script_dir,
        path_to_repos_list_file=info.path_to_repos_list_file,
        username=info.username,
        display=info.display,
        user_uid=info.user_uid,
        global_site_packages_path=info.global_site_packages_path,
        venv_python_path=info.venv_python_path,
    )

    service_maker.save_template()


if __name__ == "__main__":
    make_service()
