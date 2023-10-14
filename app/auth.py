import os

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

credentials = (
    os.getenv("HTTP_AUTH_USER", ""),
    generate_password_hash(os.getenv("HTTP_AUTH_PASSWORD", "")),
)


@auth.verify_password
def verify_credentials(username: str, password: str) -> str | None:
    if not credentials[0]:
        return username

    if username == credentials[0] and check_password_hash(credentials[1], password):
        return username

    return None
