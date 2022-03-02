"""
Insta485 post.

URLs include:
/explore/

Le
"""
import flask
import insta485
from insta485.views.utils import debug_dict, get_users_image_url_by_name


@insta485.app.route('/explore/', methods=['GET'])
def explore():
    """Help Message."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    # Select all users except username from users
    # get their image_url
    d_b = insta485.model.get_db()
    return flask.render_template("explore.html",
                                 **{**debug_dict(get_users_image_url_by_name(
                                     [i for i in [i["username"] for i in
                                                  d_b.execute(
                                                      "SELECT username "
                                                      "FROM users "
                                                      "WHERE username != ?",
                                                      (flask.session[
                                                           'username'],)
                                                  ).fetchall()] if
                                      i not in [i["username2"] for i in
                                                d_b.execute(
                                                    "SELECT username2 "
                                                    "FROM following "
                                                    "WHERE username1 = ?",
                                                    (flask.session[
                                                         'username'],)
                                                ).fetchall()]]),
                                     "not_following"),
                                    "current_url": flask.request.path,
                                    "username": flask.session['username']})
