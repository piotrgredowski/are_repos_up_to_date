#!/usr/bin/env python3

import os
import subprocess
import time


from PIL import Image, ImageOps
from pystray import Icon, Menu, MenuItem

from lib.cli import args
from lib import utils

from sys import platform
if platform == 'darwin':
    def notify(title: str, text: str):
            os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title))
else:
    from gi import require_version
    require_version('Notify', '0.7')
    from gi.repository import Notify

    def notify(title: str, text: str):
        Notify.init(title)
        n = Notify.Notification.new('', text)
        n.set_urgency(Notify.Urgency.CRITICAL)
        n.show()

curr_dir = os.path.dirname(os.path.realpath(__file__))

MESSAGE = "Repositories which are not up to date"

def _prepare_image(full_img_path):
    return ImageOps.expand(Image.open(full_img_path), border=5, fill=0)

def get_image(rel_img_path):
    return _prepare_image(os.path.join(curr_dir, rel_img_path))

icon_ok = get_image('images/ok.png')
icon_fail = get_image('images/fail.png')
icon_loading = get_image('images/loading.png')


def execute_command(command: str, cwd: str):
    return subprocess.run(command.split(" "), cwd=cwd)


def repo_is_up_to_date(repo: utils.Repo):
    commands = {
        "fetch": "git fetch",
        "is_up_to_date": f"git merge-base --is-ancestor origin/{repo.branch} {repo.branch}",
    }

    execute_command(commands["fetch"], cwd=repo.path)
    returncode = execute_command(commands["is_up_to_date"], cwd=repo.path).returncode

    return returncode == 0


def void():
    pass


def setup(icon: Icon):
    icon.visible = True
    is_up_to_date = True

    while True:
        output = []
        wrong_output = []

        # TODO: Please do it better...
        repos, wrong_paths = utils.get_repos_and_wrong_paths(args.file)

        for repo in repos:
            if repo_is_up_to_date(repo):
                continue
            output.append(f'- {repo.path} ({repo.branch})')

        was_up_to_date = is_up_to_date
        is_up_to_date = not bool(output)

        if wrong_paths:
            wrong_output.extend(['', 'Those directories does not exist:'])
            for path in wrong_paths:
                wrong_output.append(f'-  {path}')

        if is_up_to_date:
            _icon = icon_ok
            _items = [MenuItem('All existing repositories are up to date', action=void)]
        else:
            _icon = icon_fail
            _items = [MenuItem(f'{MESSAGE}:', action=void)] + \
                [MenuItem(f'{text}', action=void) for text in output]
            if was_up_to_date:
                msg = "\n".join(output + wrong_output)
                notify(MESSAGE, msg)

        if wrong_paths:
            _items.extend([MenuItem(f'{text}', action=void) for text in wrong_output])

        _menu = Menu(*_items)

        icon.icon = _icon
        icon.menu = _menu

        time.sleep(args.delay)


menu = Menu(MenuItem(text='Checking repositories...',
                     action=void))

icon = Icon(name=MESSAGE, icon=icon_loading, menu=menu)

icon.run(setup)
