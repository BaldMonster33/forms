"""REST API for comments."""
import flask
import insta485
from insta485.api.utils import authentication


@insta485.app.route("/api/v1/comments/", methods=['POST'])
def post_comment():
    """Comment."""
    con = insta485.model.get_db()
    if flask.request.authorization:
        username, password = flask.request.authorization["username"], \
                             flask.request.authorization["password"]
        authentication(username, password, con)
    elif 'username' in flask.session:
        username = flask.session["username"]
    else:
        flask.abort(403)

    args = flask.request.args
    postid = args.get("postid", 0, int)
    jsons = flask.request.json
    text = jsons.get('text')

    con.execute("INSERT INTO comments (owner, postid, text) "
                "VALUES (?,?,?)",
                (username, postid, text))

    commentid = con.execute("SELECT last_insert_rowid() ").fetchone()[
        "last_insert_rowid()"]
    comment = con.execute("SELECT owner, text "
                          "FROM comments "
                          f"WHERE commentid = {commentid}").fetchone()

    comment["commentid"] = commentid
    comment_owner = comment["owner"]
    comment_id = comment["commentid"]
    comment["lognameOwnsThis"] = (comment_owner == username)
    comment["ownerShowUrl"] = f"/users/{comment_owner}/"
    comment["url"] = f"/api/v1/comments/{comment_id}/"
    return flask.jsonify(**comment), 201


@insta485.app.route("/api/v1/comments/<int:commentid>/", methods=['DELETE'])
def delete_comment(commentid):
    """Delete."""
    connection = insta485.model.get_db()

    if flask.request.authorization:
        username = flask.request.authorization["username"]
        password = flask.request.authorization["password"]
        authentication(username, password, connection)
    elif 'username' in flask.session:
        username = flask.session["username"]
    else:
        flask.abort(403)
    comment = connection.execute(
        "SELECT commentid, owner "
        "FROM comments "
        f"WHERE commentid = {commentid}"
    ).fetchone()
    if not comment:
        return flask.abort(404)
    if comment["owner"] != username:
        return flask.abort(403)
    connection.execute(
        f"DELETE FROM comments WHERE commentid = {commentid}"
    )
    return "", 204
