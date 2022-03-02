"""
Insta485 login view.

URLs include:
/accounts/login
/accounts/logout/
/accounts/create/
/accounts/delete/

Le
"""
import uuid
from pathlib import Path
import flask
import insta485
from insta485.views.utils import comp_hash, save_file, \
    comp_salt_password, validate_not_empty, remove_file, store_and_remove


# @insta485.app.route('/accounts/login/', methods=['GET'])
# def login():
#     """Help."""
#     if 'username' in flask.session:
#         return flask.redirect(flask.url_for('/'))
#     # print("DEBUG Login:", flask.request.form['username'])
#     # flask.session['username'] = flask.request.form['username']
#     # return flask.redirect(flask.url_for('show_index'))
#     return flask.render_template("login.html")


# def login_helper(forms):
#     """Help."""
#     if 'username' not in forms or 'password' not in forms:
#         flask.abort(400)
#     username, password = forms['username'], forms['password']
#     if not (username and password):
#         flask.abort(400)
#     connection = insta485.model.get_db()
#     cur = connection.execute(
#         "SELECT password FROM users WHERE username = ?", (username,)
#     )
#     users = cur.fetchall()
#     if len(users) != 1:
#         flask.abort(403)
#     salt = users[0]['password'].split('$')[1]
#     hashed_password = comp_hash(salt, password)
#     if hashed_password != users[0]['password']:
#         flask.abort(403)
#
#     # After validation, set cookies
#     flask.session["username"] = username
#     return flask.redirect(flask.url_for('show_index'))


def create_helper(request):
    """Help."""
    forms = request.form
    # Read forms and validate none is empty. Also hash password
    if 'name' not in forms:
        name = uuid.uuid4().hex
        username = name
        flask.abort(400)
    else:
        name = forms["name"]
        username = uuid.uuid4().hex
    # UUID for filename and store it


    # Verify username haven't been registered before
    connection = insta485.model.get_db()
    # cur = connection.execute("SELECT username FROM users WHERE username = ?",
    #                          (username,)).fetchall()
    # if len(cur) != 0:
    #     flask.abort(409)
    # Store all info plus hashed password into user db
    connection.execute(
        "INSERT INTO users(username, name) "
        "VALUES (?,?)",
        (username, name)
    )
    print(username, name)
    # url = flask.request.args.get('target')
    flask.session["name"] = username
    # if not url:
    return flask.redirect(flask.url_for('show_index'))
    # return flask.redirect(url)


# def delete_helper():
#     """Help."""
#     # If login
#     if "username" not in flask.session:
#         return flask.abort(403)
#     username = flask.session["username"]
#     # Delete post
#     connection = insta485.model.get_db()
#     connection.execute("DELETE FROM posts WHERE owner = ?", (username,))
#     # Delete user icon
#     old_filename = connection.execute(
#         "SELECT filename FROM users WHERE username = ?",
#         (username,)).fetchone()["filename"]
#     connection.execute("DELETE FROM users WHERE username = ?", (username,))
#     remove_file(old_filename)
#
#     # Redirect to url
#     url = flask.request.args.get('target')
#     flask.session.clear()
#     if not url:
#         return flask.redirect(flask.url_for('show_index'))
#     return flask.redirect(url)


# def edit_helper(forms):
#     """Help."""
#     url = flask.request.args.get('target')
#     # If login
#     if "username" not in flask.session:
#         return flask.abort(403)
#     username = flask.session["username"]
#     if 'fullname' not in forms or 'email' not in forms:
#         return flask.abort(400)
#
#     fullname, email = forms["fullname"], forms["email"]
#
#     if 'file' in flask.request.files:
#         if flask.request.files["file"]:
#             store_and_remove(username)
#     if not validate_not_empty(fullname, email):
#         return flask.abort(400)
#     connection = insta485.model.get_db()
#     connection.execute(
#         "UPDATE users SET fullname = ?, email = ? WHERE username = ?",
#         (fullname, email, username))
#     if not url:
#         return flask.redirect(flask.url_for('show_index'))
#     return flask.redirect(url)


# def update_helper(forms):
#     """Help."""
#     url = flask.request.args.get('target')
#     # If login
#     if "username" not in flask.session:
#         return flask.abort(403)
#     username = flask.session["username"]
#     if 'password' not in forms or \
#             'new_password1' not in forms or \
#             'new_password2' not in forms:
#         return flask.abort(400)
#     password, new_password1, new_password2 = \
#         forms["password"], forms["new_password1"], forms["new_password2"]
#     if not validate_not_empty(password, new_password1, new_password2):
#         return flask.abort(400)
#     if new_password2 != new_password1:
#         return flask.abort(401)
#
#     connection = insta485.model.get_db()
#     cur = connection.execute(
#         "SELECT password FROM users WHERE username = ?", (username,)
#     )
#     old_hashed_password = cur.fetchall()[0]['password']
#     print(old_hashed_password)
#     salt = old_hashed_password.split('$')[1]
#     hashed_password = comp_hash(salt, password)
#     print(hashed_password)
#     if hashed_password != old_hashed_password:
#         return flask.abort(403)
#
#     # hash password again for database usage
#     hashed_password = comp_salt_password(new_password1)
#     print(hashed_password)
#     # Update into database
#     connection.execute("UPDATE users SET password = ? WHERE username=?",
#                        (hashed_password, username))
#     if not url:
#         url = flask.url_for('show_index')
#         # return flask.redirect()
#     return flask.redirect(url)


@insta485.app.route('/accounts/', methods=['POST'])
def validate():
    """Help."""
    request = flask.request
    forms = request.form
    operation = str(forms["operation"])
    # if operation == "login":
    #     return login_helper(forms)
    if operation == "create":
        return create_helper(request)
    # if operation == "delete":
    #     return delete_helper()
    # if operation == "edit_account":
    #     return edit_helper(forms)
    # if operation == "update_password":
    #     return update_helper(forms)
    return None


@insta485.app.route('/accounts/logout/', methods=['POST', 'GET'])
def logout():
    """Help."""
    flask.session.clear()
    return flask.redirect(flask.url_for('create'))

#
@insta485.app.route('/accounts/create/', methods=['GET'])
def create():
    """Help."""
    if 'name' in flask.session:
        return flask.redirect(flask.url_for('get_index'))
    return flask.render_template("create.html")

#
# @insta485.app.route('/accounts/delete/', methods=['GET'])
# def delete():
#     """Help."""
#     if "username" not in flask.session:
#         return flask.redirect(flask.url_for('login'))
#     return flask.render_template("delete.html",
#                                  **{"username": flask.session["username"]})
#
#
# @insta485.app.route('/accounts/edit/', methods=['GET'])
# def edit():
#     """Help."""
#     if "username" not in flask.session:
#         return flask.redirect(flask.url_for('login'))
#     # path = flask.request.path
#     username = flask.session["username"]
#     # Get profile image and name
#     # forms = flask.request.forms
#     connection = insta485.model.get_db()
#     cur = connection.execute(
#         "SELECT email, filename, fullname, username "
#         "FROM users WHERE username = ?",
#         (username,)
#     ).fetchone()
#     # return cur
#
#     return flask.render_template("edit.html", **cur)
#
#
# @insta485.app.route('/accounts/password/', methods=['GET'])
# def set_password():
#     """Help."""
#     return flask.render_template("password.html",
#                                  **{'username': flask.session["username"]})
