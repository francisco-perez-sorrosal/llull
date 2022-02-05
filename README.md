# llull

[![ci](https://github.com/francisco-perez-sorrosal/llull/workflows/ci/badge.svg)](https://github.com/francisco-perez-sorrosal/llull/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://francisco-perez-sorrosal.github.io/llull/)
[![pypi version](https://img.shields.io/pypi/v/llull.svg)](https://pypi.org/project/llull/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/francisco-perez-sorrosal/llull)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/llull/community)

Taxonomy Manager

## Requirements

llull requires Python 3.7 or above.

<details>
<summary>To install Python 3.7, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.7
pyenv install 3.7.12

# make it available globally
pyenv global system 3.7.12
```
</details>

## Installation

With `pip`:
```bash
pip install llull
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.7 -m pip install --user pipx
pipx install llull
```


## Dev

For running tests in vscode follow the instructions [here](https://pdm.fming.dev/#vscode), activating PEP582 globally
and launching VSCode from the command line with `code .` in the project directory.