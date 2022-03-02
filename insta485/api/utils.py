"""Utilis functions used across file."""
import flask
from insta485.views.utils import comp_hash


def authentication(username, password, db_a):
    """Auth."""
    cur = db_a.execute(
        "SELECT password FROM users WHERE username = ?", (username,)
    )
    user = cur.fetchone()
    salt = user['password'].split('$')[1]
    hashed_password = comp_hash(salt, password)
    if hashed_password != user['password']:
        flask.abort(403)
