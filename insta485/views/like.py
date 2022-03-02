"""
Insta485 likes view.

URLs include:
/likes/?target=URL

Le
"""
import flask
import insta485


@insta485.app.route('/likes/', methods=['POST'])
def likes():
    """Help."""
    # url = flask.request.args.get('target')
    # post_id = url.split('/')[-2]
    user = flask.session["username"]
    forms = flask.request.form
    target = flask.request.args.get('target')
    post_id = forms["postid"]
    operation = forms['operation']
    if operation == "like":
        connection = insta485.model.get_db()
        # print(forms)
        double_check = connection.execute(
            "SELECT * "
            "FROM likes "
            "WHERE owner = ? AND postid = ? ",
            (user, post_id)
        ).fetchall()
        # print("H", double_check)
        if double_check != []:
            return flask.abort(409)
        connection.execute(
            "INSERT INTO likes(owner, postid) "
            "VALUES (?,?)",
            (user, post_id)
        )
    else:
        connection = insta485.model.get_db()
        double_check = connection.execute(
            "SELECT * "
            "FROM likes "
            "WHERE owner = ? AND postid = ? ",
            (user, post_id)
        ).fetchall()
        if double_check == []:
            return flask.abort(409)
        connection.execute(
            "INSERT INTO likes(owner, postid) "
            "VALUES (?,?)",
            (user, post_id)
        )
        connection.execute(
            "DELETE FROM likes WHERE postid = ? AND owner = ?", (post_id, user)
        )
    return flask.redirect(target)
