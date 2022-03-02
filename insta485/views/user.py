"""
Insta485 user.

URLs include:
/users/


"""
import flask
import insta485


@insta485.app.route('/users/<user_url_slug>/', methods=['GET'])
def get_user(user_url_slug):
    """Help."""
    # if not logged in
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    log = flask.session['username']

    connection = insta485.model.get_db()

    user = connection.execute(
        "SELECT username, fullname, filename FROM users WHERE username = ?",
        (user_url_slug,)
    ).fetchone()
    if not user:
        flask.abort(404)
    filename = user["filename"]
    posts = connection.execute(
        "SELECT postid, filename FROM posts WHERE owner = ? "
        "ORDER BY created DESC, postid DESC ",
        (user["username"],)
    ).fetchall()
    num_posts = len(posts)

    followers = connection.execute(
        "SELECT username1 FROM following WHERE username2 = ? ",
        (user["username"],)
    ).fetchall()
    num_followers = len(followers)

    log_follow_user = connection.execute(
        "SELECT username1 FROM following "
        "WHERE username1 = ? AND username2 = ?",
        (log, user["username"])
    ).fetchall()

    logname_follows_username = (len(log_follow_user) == 1)

    following = connection.execute(
        "SELECT username1 FROM following WHERE username1 = ? ",
        (user["username"],)
    ).fetchall()
    num_following = len(following)

    context = {
        "user": user,
        "owner_img_url": filename,
        "followers": num_followers,
        "following": num_following,
        "posts": posts,
        "total_posts": num_posts,
        "logname_follows_username": logname_follows_username}

    return flask.render_template("user.html",
                                 username=flask.session["username"],
                                 targetuser=user_url_slug, **context)


@insta485.app.route('/users/<user_url_slug>/followers/', methods=['GET'])
def show_followers(user_url_slug):
    """Help."""
    connect = insta485.model.get_db()
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session['username']

    # If someone tries to access a user_url_slug
    # that does not exist in the database, then abort(404)
    user = connect.execute(
        "SELECT username, fullname FROM users WHERE username = ?",
        (user_url_slug,)
    ).fetchall()
    if len(user) == 0:
        flask.abort(404)

    follower = connect.execute(
        "SELECT username1 AS username FROM following WHERE username2 == ?",
        (user_url_slug,)
    ).fetchall()

    logname_following = connect.execute(
        "SELECT username2 AS username FROM following WHERE username1 == ?",
        (logname,)
    ).fetchall()

    for user in follower:
        if user in logname_following:
            user["logname_follows_username"] = True
            # headshots
            user["user_img_url"] = connect.execute(
                "SELECT filename FROM users WHERE username == ?",
                (user["username"],)
            ).fetchall()
        else:
            user["logname_follows_username"] = False
            # headshots
            user["user_img_url"] = connect.execute(
                "SELECT filename FROM users WHERE username == ?",
                (user["username"],)
            ).fetchall()
    content = {
        "logname": logname,
        "followers": follower,
        "user_url_slug": user_url_slug}
    return flask.render_template("followers.html", **content)


@insta485.app.route('/users/<user_url_slug>/following/', methods=['GET'])
def show_following(user_url_slug):
    """Help."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    logname = flask.session['username']
    connect = insta485.model.get_db()
    # If someone tries to access a user_url_slug
    # that does not exist in the database, then abort(404)
    user = connect.execute(
        "SELECT username, fullname FROM users WHERE username = ?",
        (user_url_slug,)
    ).fetchall()
    if len(user) == 0:
        flask.abort(404)

    following = connect.execute(
        "SELECT username2 AS username FROM following WHERE username1 == ?",
        (user_url_slug,)
    ).fetchall()

    logname_following = connect.execute(
        "SELECT username2 AS username FROM following WHERE username1 == ?",
        (logname,)
    ).fetchall()
    for user in following:
        if user in logname_following:
            user["logname_follows_username"] = True
            user["user_img_url"] = connect.execute(
                "SELECT filename FROM users WHERE username == ?",
                (user["username"],)
            ).fetchall()
        else:
            user["logname_follows_username"] = False
            user["user_img_url"] = connect.execute(
                "SELECT filename FROM users WHERE username == ?",
                (user["username"],)
            ).fetchall()

    content = {
        "logname": logname,
        "following": following,
        "user_url_slug": user_url_slug
    }
    return flask.render_template("following.html", **content)
