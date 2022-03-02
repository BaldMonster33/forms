"""Utilis functions used across files."""
import os
import uuid
import hashlib
from pathlib import Path
import flask
import arrow
import insta485


def comp_hash(salt, password):
    """Use in validation process."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def humanize_time(time):
    """Help."""
    return arrow.get(time).humanize()


def save_file(name):
    """Save files from POST to local var folder."""
    return Path(insta485.app.config['UPLOAD_FOLDER']) / name


def comp_salt_password(password):
    """Put salt on steak."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def validate_not_empty(*args):
    """Help."""
    for i in args:
        if i == "":
            return False
    return True


def remove_file(filename):
    """Help."""
    if filename:
        path = insta485.app.config["UPLOAD_FOLDER"] / filename
        os.remove(path)


def get_users_image_url_by_name(users: list):
    """Help."""
    con = insta485.model.get_db()
    not_following = con.execute(
        "SELECT username, filename "
        "FROM users "
        f"WHERE username IN ({','.join('?' * len(users))})",
        users
    ).fetchall()
    return not_following


def debug_dict(info: list, temp_note="1"):
    """Return a simple dict so that can be returned in flask."""
    return {temp_note: info}


def store_and_remove(username):
    """Store and remove old new files."""
    file = flask.request.files['file']
    stem = uuid.uuid4().hex
    # get Name
    get_suffix = Path(file.filename).suffix
    allowed_names = insta485.app.config["ALLOWED_EXTENSIONS"]
    if get_suffix[1:] not in allowed_names:
        return flask.abort(400)
    uuid_basename = f"{stem}{get_suffix}"
    filepath = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
    file.save(save_file(filepath))

    # Remove old file from local storage
    connection = insta485.model.get_db()
    old_filename = connection.execute(
        "SELECT filename FROM users WHERE username = ?",
        (username,)).fetchone()["filename"]

    connection.execute("UPDATE users "
                       "SET filename = ? WHERE username = ?",
                       (uuid_basename, username))
    remove_file(old_filename)
    return None
