#

[![pipeline status](https://gitlab.com/riton/flask-fernet-cookies-session/badges/develop/pipeline.svg)](https://gitlab.com/riton/flask-fernet-cookies-session/-/commits/develop)
[![coverage report](https://gitlab.com/riton/flask-fernet-cookies-session/badges/develop/coverage.svg)](https://gitlab.com/riton/flask-fernet-cookies-session/-/commits/develop)
[![black badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://img.shields.io/badge/code%20style-black-000000.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Development

[`poetry`](https://python-poetry.org/) is used to manage this project.

[`poe the poet`](https://github.com/nat-n/poethepoet) is used as the _task runner_ of this project. If you don't know what a _task runner_ is, think about an alternative version of a `Makefile`.

### Install project dependencies

```
$ poetry install
```

### Unit testing

#### Test with all python versions

```
$ poe test
```

#### Test with a specific python version

```
$ poe test-py38
```

### F.A.Q

#### Should I commit the `poetry.lock` file ?

**Yes**. This file is used to _lock your project dependencies version_.

This is a very important file to ensure _reproducible executions_.

#### Was this project generated from a template ?

**Yes**. This project was generated using @rferrand [`copier-python-project-skeleton`](https://gitlab.in2p3.fr/rferrand/copier-python-project-skeleton).

[![copier-python-project-skeleton](https://gitlab.in2p3.fr/uploads/-/system/project/avatar/16610/python_copier.png?width=48)](https://gitlab.in2p3.fr/rferrand/copier-python-project-skeleton)
