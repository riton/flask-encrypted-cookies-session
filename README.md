#

[![pipeline status](https://gitlab.com/riton/flask-fernet-cookies-session/badges/develop/pipeline.svg)](https://gitlab.com/riton/flask-fernet-cookies-session/-/commits/develop)
[![coverage report](https://gitlab.com/riton/flask-fernet-cookies-session/badges/develop/coverage.svg)](https://gitlab.com/riton/flask-fernet-cookies-session/-/commits/develop)
[![black badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://img.shields.io/badge/code%20style-black-000000.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Description

A cookie based session for `flask` relying on `Fernet` encrypted cookies.

### Motivation

`flask` default session rely on _signed cookies_. This sometimes is not enough, and encrypted data should be used.

_Example_ : Use cookies to store OAuth2 _access tokens_ without the burden of server side storage.


## Usage

Private key used to encrypt cookies can be generated with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"`

```python
# -*- coding: utf-8 -*-
from flask import Flask, session

from flask_encrypted_cookies_session import EncryptedCookieSession

DEBUG = "True"
ENCRYPTED_COOKIES_SECRET_KEY = (
    "JNJQuYdaUGr8XBSoZNYF9FC-A7RZ7iFqV_KqrCwYr0s="  # Fernet.generate_key()
)
# To rotate your keys:
# ENCRYPTED_COOKIES_SECRET_KEY = "JNJQuYdaUGr8XBSoZNYF9FC-A7RZ7iFqV_KqrCwYr0s=,Dfo2hCeG-S6CeY-_tgJ33gip9rxC2t8qNK0CM0gZlRk="  # [Fernet.generate_key(), Fernet.generate_key()]

app = Flask(__name__)
app.config.from_object(__name__)

# This will replace the default Flask application session interface with the encrypted
# cookie based session
EncryptedCookieSession(app)


@app.route("/set/")
def session_set():
    session["key"] = "value"
    return "ok"


@app.route("/get/")
def session_get():
    return session.get("key", "not set")
```

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
$ poe test-py39
```

### F.A.Q

#### Should I commit the `poetry.lock` file ?

**Yes**. This file is used to _lock your project dependencies version_.

This is a very important file to ensure _reproducible executions_.

#### Was this project generated from a template ?

**Yes**. This project was generated using @rferrand [`copier-python-project-skeleton`](https://gitlab.in2p3.fr/rferrand/copier-python-project-skeleton).

[![copier-python-project-skeleton](https://gitlab.in2p3.fr/uploads/-/system/project/avatar/16610/python_copier.png?width=48)](https://gitlab.in2p3.fr/rferrand/copier-python-project-skeleton)
