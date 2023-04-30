# -*- coding: utf-8 -*-
#
# Copyright (c) IN2P3 Computing Centre, IN2P3, CNRS
#
# Contributor(s): Rémi Ferrand <remi.ferrand@cc.in2p3.fr>, 2023
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
from __future__ import annotations

from http import HTTPStatus

from cryptography.fernet import Fernet
from flask import Flask, session

from flask_encrypted_cookies_session import EncryptedCookieSession


def create_app(encryption_keys: bytes) -> Flask:
    app = Flask(__name__)
    app.config.update(
        {
            "SECRET_KEY": "fooooooo",
            "ENCRYPTED_COOKIES_SECRET_KEY": encryption_keys,
            "TESTING": True,
        }
    )
    EncryptedCookieSession(app)

    @app.route("/set/")
    def session_set():
        session["key"] = "value"
        return "ok"

    @app.route("/get/")
    def session_get():
        return session.get("key", "not set")

    return app


def test_single_key() -> None:
    app = create_app(Fernet.generate_key())
    _test_with_app(app)


def test_multi_keys() -> None:
    app = create_app(b",".join([Fernet.generate_key(), Fernet.generate_key()]))
    _test_with_app(app)


def _test_with_app(app: Flask) -> None:
    t_client = app.test_client()

    response = t_client.get("/get/")
    assert response.status_code == HTTPStatus.OK
    assert response.data == b"not set"

    response = t_client.get("/set/")
    assert response.status_code == HTTPStatus.OK
    assert response.data == b"ok"

    response = t_client.get("/get/")
    assert response.status_code == HTTPStatus.OK
    assert response.data == b"value"
