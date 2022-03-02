"""REST API for likes."""
import flask
import insta485
from insta485.api.utils import authentication


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def get_likes():
    """Get likes."""
    postid = flask.request.args.get("postid", int)
    connection = insta485.model.get_db()
    if flask.request.authorization:
        username, password = flask.request.authorization["username"], \
                             flask.request.authorization["password"]
        authentication(username, password, connection)
    elif flask.session.get('username'):
        username = flask.session["username"]
    else:
        return flask.abort(403)

    likes = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (username, postid)
    ).fetchone()
    if likes:
        likeid = likes["likeid"]
        like_d = {"likeid": likeid, "url": f"/api/v1/likes/{likeid}/"}
        return flask.jsonify(like_d), 200

    connection.execute(
        "INSERT INTO likes(owner, postid) "
        "VALUES (?,?)",
        (username, postid)
    )
    ids = connection.execute("SELECT last_insert_rowid() ").fetchone()[
        "last_insert_rowid()"]
    like_d = {"likeid": ids, "url": f"/api/v1/likes/{ids}/"}
    return flask.jsonify(like_d), 201


@insta485.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
def delete_likes(likeid):
    """Delete likes."""
    connection = insta485.model.get_db()
    if flask.request.authorization:
        username, password = flask.request.authorization["username"], \
                             flask.request.authorization["password"]
        authentication(username, password, connection)
    elif 'username' in flask.session:
        username = flask.session["username"]
    else:
        return flask.abort(403)

    likes = connection.execute(
        "SELECT likeid, owner "
        "FROM likes "
        "WHERE likeid = ? ",
        (likeid,)
    ).fetchone()
    if not likes:
        return flask.abort(404)
    if likes["owner"] != username:
        return flask.abort(403)

    connection.execute(
        f"DELETE FROM likes WHERE likeid = {likeid}"
    )
    return "", 204
