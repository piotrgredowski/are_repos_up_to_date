# Are repos up to date?

This script will check if current commits of specified local repos are the same as on remote.

## Requirements

- `python>=3.6`
- `python3-pip`
- `sudo`

## Installation

Prepare `yaml` file with repos to watch:

```yaml
## repos.yaml

- path: /path/to/1/repo # Default branch is 'master'
- path: /path/to/2/repo
  branch: develop       # You can specify other branch
```

You can install it with one command but it will require to enter `root` password.

Place this repository in some cozy place from where it can be started.

Below script will create systemd service, enable it and start.
In consequence `check_repos.py` will check for repositories indicated in `repos.yaml` file.

> NOTE: Python packages has (as far as I know) to be installed globally, not in virtualenv.
> Why? Because of using `gi` by `pystray`.

```shell
./install.sh
```