"""Applications authentication module

Authentication system is based on HTTPBasicAuth and consists of 2 users:
- admin
- regular user.
"""
import os
from typing import Any

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

admin_credentials = (
    os.getenv("HTTP_AUTH_ADMIN_USER"),
    generate_password_hash(os.getenv("HTTP_AUTH_ADMIN_PASSWORD", "")),
)
credentials = (
    os.getenv("HTTP_AUTH_USER", ""),
    generate_password_hash(os.getenv("HTTP_AUTH_PASSWORD", "")),
)

if admin_credentials[0] == credentials[0]:
    raise ValueError("admin username cannot be identical as user username")


def is_admin(username: Any) -> bool:
    """Verify if given username is admin"""
    if not admin_credentials[0]:
        return False

    return username == admin_credentials[0]


@auth.verify_password
def verify_credentials(username: str, password: str) -> str | None:
    """Validates given credentials"""
    if is_admin(username) and check_password_hash(admin_credentials[1], password):
        return username

    if not credentials[0]:
        return username

    if username == credentials[0] and check_password_hash(credentials[1], password):
        return username

    return None
