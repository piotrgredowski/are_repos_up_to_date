#!/usr/bin/env python3

import os
import subprocess
import time

from PIL import Image
from pystray import Icon, Menu, MenuItem

from gi import require_version
require_version('Notify', '0.7')
from gi.repository import Notify


# TODO: Load that from file, get 'master' by default
paths_and_branches = [
    ('/path/to/repo', 'branch name'),
    ('/path/to/second/repo', 'branch name'),
]

MESSAGE = "Repositories which are not up to date"
DELAY = 10
ICON_OK = Image.open('./images/ok.png')
ICON_FAIL = Image.open('./images/fail.png')
ICON_LOADING = Image.open('./images/loading.png')


def execute_command(command: str, cwd: str, with_stdout=False):
    if with_stdout:
        stdout = subprocess.PIPE
    else:
        stdout = None

    output = subprocess.run(command.split(" "), cwd=cwd, stdout=stdout).stdout

    if with_stdout:
        return output.decode('utf-8')


def repo_is_up_to_date(path_branch):
    path, branch = path_branch
    commands = {
        "fetch": "git fetch",
        "origin": f"git rev-parse origin/{branch}",
        "local": f"git rev-parse {branch}",
    }

    fetch = execute_command(commands["fetch"], cwd=path)
    origin_commit_id = execute_command(commands["origin"], cwd=path, with_stdout=True)
    local_commit_id = execute_command(commands["local"], cwd=path, with_stdout=True)

    return origin_commit_id == local_commit_id


def send_notification(text):
    n = Notify.Notification.new(MESSAGE, text)
    n.set_urgency(Notify.Urgency.CRITICAL)
    n.show()


def void():
    pass


def setup(icon: Icon):
    icon.visible = True
    is_up_to_date = True

    Notify.init(MESSAGE)

    while True:
        output = []
        for path_branch in paths_and_branches:
            path, branch = path_branch
            if not repo_is_up_to_date(path_branch):
                output.append(f"{path} ({branch})")
        was_up_to_date = is_up_to_date
        is_up_to_date = not bool(output)

        if is_up_to_date:
            _icon = ICON_OK
            _items = [MenuItem('Everything is up to date', action=void)]
        else:
            _icon = ICON_FAIL
            _items = [MenuItem(f'{MESSAGE}:', action=void)] + \
                [MenuItem(f'\t{text}', action=void) for text in output]
            if was_up_to_date:
                send_notification("\n\n".join(output))
        _menu = Menu(*_items)

        icon.icon = _icon
        icon.menu = _menu

        time.sleep(DELAY)


menu = Menu(MenuItem(text='Checking repositories...',
                     action=void))

icon = Icon(name=MESSAGE, icon=ICON_LOADING, menu=menu)

icon.run(setup)
