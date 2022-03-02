"""
Insta485 comments view.

URLs include:
/comments/?target=URL

Le
"""
import flask
import insta485


@insta485.app.route('/comments/', methods=['POST'])
def add_comment():
    """Help."""
    url = flask.request.args.get('target')
    # validate_not_empty(forms.get('postid', type=str))
    forms = flask.request.form
    operation = forms['operation']
    if operation == "create":
        post_id = forms.get('postid', type=int)
        text = forms['text']
        if text == "":
            flask.abort(400)
        owner = flask.session["username"]
        connection = insta485.model.get_db()
        connection.execute(
            "INSERT INTO comments(owner,postid,text) "
            "VALUES (?,?,?)",
            (owner, post_id, text)
        )
    elif operation == "delete":
        commentid = forms["commentid"]
        connection = insta485.model.get_db()
        username = flask.session["username"]
        comment_owner = connection.execute(
            "SELECT owner FROM comments WHERE commentid = ?",
            (commentid,)
        ).fetchone()["owner"]
        if comment_owner != username:
            return flask.abort(403)

        connection.execute(
            "DELETE FROM comments WHERE commentid = ?", (commentid,)
        )

    if not url:
        return flask.redirect("/")
    return flask.redirect(url)
