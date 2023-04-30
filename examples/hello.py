# -*- coding: utf-8 -*-
from flask import Flask, session

from flask_encrypted_cookies_session import EncryptedCookieSession

SECRET_KEY = "22ad5f6d-8004-4f59-a876-bba7812174d9"  # CHANGE ME for production
SESSION_COOKIE_HTTPONLY = "True"
SESSION_COOKIE_SECURE = "False"  # Set to True for production
PERMANENT_SESSION_LIFETIME = 3600  # 1h
DEBUG = "True"
# ENCRYPTED_COOKIES_SECRET_KEY = (
#     "JNJQuYdaUGr8XBSoZNYF9FC-A7RZ7iFqV_KqrCwYr0s="  # Fernet.generate_key()
# )
ENCRYPTED_COOKIES_SECRET_KEY = "JNJQuYdaUGr8XBSoZNYF9FC-A7RZ7iFqV_KqrCwYr0s=,Dfo2hCeG-S6CeY-_tgJ33gip9rxC2t8qNK0CM0gZlRk="  # [Fernet.generate_key(), Fernet.generate_key()]

app = Flask(__name__)
app.config.from_object(__name__)

EncryptedCookieSession(app)


@app.route("/set/")
def session_set():
    session["key"] = "value"
    return "ok"


@app.route("/get/")
def session_get():
    return session.get("key", "not set")


if __name__ == "__main__":
    app.run(debug=True)
