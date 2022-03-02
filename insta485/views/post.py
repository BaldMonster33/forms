"""
Insta485 post.

URLs include:
/posts/


"""
import uuid
from pathlib import Path
import flask
import insta485
from insta485.views.utils import remove_file, \
    save_file


@insta485.app.route('/posts/', methods=['POST'])
def post_post():
    """Help."""
    url = flask.request.args.get('target')
    forms = flask.request.form
    operation = forms['operation']
    # return forms
    username = flask.session["username"]
    if operation == "create":
        file = flask.request.files['file']
        stem = uuid.uuid4().hex
        suffix = Path(file.filename).suffix
        # print(suffix)
        if suffix[1:] not in insta485.app.config["ALLOWED_EXTENSIONS"]:
            return flask.abort(400)
        basename = f"{stem}{suffix}"
        filepath = insta485.app.config["UPLOAD_FOLDER"] / basename
        file.save(save_file(filepath))
        connection = insta485.model.get_db()
        connection.execute("INSERT INTO posts (filename, owner) "
                           "VALUES (?,?)",
                           (basename, username))
    elif operation == "delete":
        postid = forms["postid"]
        connection = insta485.model.get_db()
        comment_owner = connection.execute(
            "SELECT owner FROM posts WHERE postid = ?",
            (postid,)
        ).fetchone()
        # return comment_owner
        if comment_owner:
            if 'username' in comment_owner:
                if comment_owner['username'] != username:
                    return flask.abort(403)
        # return flask.abort(403)
        cur = connection.execute(
            "SELECT filename "
            "FROM posts "
            "WHERE postid = ?",
            (postid,)
        ).fetchone()["filename"]
        remove_file(cur)
        cur = connection.execute(
            "DELETE FROM posts WHERE postid = ?", (postid,)
        )
    if not url:
        return flask.redirect("/users/" + username + "/")
    return flask.redirect(url)


@insta485.app.route('/images/<filename>', methods=['GET', 'POST'])
def sendfile(filename):
    """Help."""
    # if 'name' not in flask.session:
    #     return flask.abort(403)
    # username = flask.session["username"]
    # connection = insta485.model.get_db()
    # lcl_fname = connection.execute(
    #     "SELECT owner FROM posts WHERE filename = ?",
    #     (filename,)).fetchone()
    # lcl_iname = connection.execute(
    #     "SELECT filename FROM users WHERE filename = ?",
    #     (filename,)).fetchone()
    # if lcl_fname or lcl_iname:
    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                         filename, as_attachment=True)
    # return flask.abort(404)
