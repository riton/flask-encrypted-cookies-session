# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from functools import cached_property
from typing import TYPE_CHECKING

from cryptography.fernet import Fernet, MultiFernet
from flask.sessions import SecureCookieSessionInterface

if TYPE_CHECKING:
    from typing import Any, Optional, Union

    from flask import Flask

    FernetType = Union[Fernet, MultiFernet]

FERNET_KEYS_SEPARATOR = b","


class SerializerInterface:
    """
    A very minimal serializer interface used by flask base SessionInterface
    """

    def dumps(self, obj: Any) -> bytes:
        raise NotImplementedError()

    def loads(
        self, s: Union[str, bytes], **kwargs: Any  # pylint: disable=invalid-name
    ) -> Any:
        raise NotImplementedError()


class FernetJSONSerializer(SerializerInterface):
    """
    A simple JSON backed serializer that rely on Fernet authenticated encryption
    """

    def __init__(self, encryption_key: FernetType) -> None:
        self._encryption_key = encryption_key
        print(type(encryption_key))

    def dumps(self, obj: Any) -> Union[str, bytes]:
        data = json.dumps(obj).encode("utf-8")
        return self._encryption_key.encrypt(data)

    def loads(
        self, s: Union[str, bytes], **kwargs: Any  # pylint: disable=invalid-name
    ) -> Any:
        if isinstance(s, str):
            s = s.encode("utf-8")

        return json.loads(self._encryption_key.decrypt(s))


class EncryptedCookieSessionInterface(SecureCookieSessionInterface):
    """
    A cookie based session interface that 'hacks' into the core Flask code
    and only overrides the 'signing serializer' used to implement Flask secure cookies.
    This implementation does not only sign cookies but also encrypts content using Fernet.
    """

    def __init__(self, encryption_key: FernetType) -> None:
        super().__init__()
        self._serializer = FernetJSONSerializer(encryption_key)

    def get_signing_serializer(self, app: Flask) -> FernetJSONSerializer:
        return self._serializer


class EncryptedCookieSession:
    """
    An encrypted cookie based session implementation that relies on Fernet (128-bit AES in CBC mode + HMAC SHA-256)
    Private key must be provided in application configuration using the 'ENCRYPTED_COOKIES_SECRET_KEY' attribute.

    If you'd like to rotate your keys (and you should), just provide two private keys separated by ',' in the
    'ENCRYPTED_COOKIES_SECRET_KEY' configuration attribute.

    To generate a private key, just use `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"`
    and keep it secret.
    """

    def __init__(self, app: Optional[Flask]) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    @cached_property
    def _secret_keys(self) -> bytes:
        assert self.app is not None
        assert "ENCRYPTED_COOKIES_SECRET_KEY" in self.app.config

        if isinstance(self.app.config["ENCRYPTED_COOKIES_SECRET_KEY"], str):
            return self.app.config["ENCRYPTED_COOKIES_SECRET_KEY"].encode("utf-8")
        return self.app.config["ENCRYPTED_COOKIES_SECRET_KEY"]

    def init_app(self, app: Flask) -> None:
        encryption_key: FernetType
        if FERNET_KEYS_SEPARATOR in self._secret_keys:
            keys = self._secret_keys.split(FERNET_KEYS_SEPARATOR, 1)
            encryption_keys: list[Fernet] = []
            for key in keys:
                encryption_keys.append(Fernet(key))
            encryption_key = MultiFernet(encryption_keys)
        else:
            encryption_key = Fernet(self._secret_keys)

        app.session_interface = EncryptedCookieSessionInterface(
            encryption_key=encryption_key
        )
