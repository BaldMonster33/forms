"""
Insta485 likes view.

URLs include:
/likes/?target=URL

Le
"""
import flask
import insta485


@insta485.app.route('/following/', methods=['POST'])
def following():
    """Help."""
    forms = flask.request.form
    target = flask.request.args.get('target')
    operation = forms['operation']
    if operation == "follow":
        user1 = flask.session["username"]
        user2 = forms["username"]
        connection = insta485.model.get_db()
        if (len(connection.execute(
                "SELECT username1 "
                "FROM following "
                "WHERE username1 = ? AND username2 = ?",
                (user1, user2)).fetchall()) != 0):
            flask.abort(409)
        connection.execute(
            "INSERT INTO following (username1, username2) "
            "VALUES (?,?)",
            (user1, user2)
        )
    elif operation == "unfollow":
        user1 = flask.session["username"]
        user2 = forms["username"]
        connection = insta485.model.get_db()
        if (len(connection.execute(
                "SELECT username1 "
                "FROM following "
                "WHERE username1 = ? AND username2 = ?",
                (user1, user2)).fetchall()) == 0):
            flask.abort(409)
        connection.execute(
            "DELETE FROM following WHERE username1 = ? AND username2 = ?",
            (user1, user2)
        )
    if not target:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)
