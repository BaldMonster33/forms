"""REST API for posts."""
import flask
import insta485
from insta485.api.utils import authentication
import os

@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_n_post():
    """Get n posts."""
    # args = flask.request.args
    # path = flask.request.path
    # if args:
    #     url = f"{path}?{flask.request.query_string.decode('utf-8')}"
    # else:
    #     url = f"{path}"
    # size = args.get('size', 10, int)
    # page = args.get('page', 0, int)
    # if size < 0 or page < 0:
    #     flask.abort(400)
    # connection = insta485.model.get_db()
    # if flask.request.authorization:
    #     username = flask.request.authorization["username"]
    #     authentication(username, flask.request.authorization["password"],
    #                    connection)
    # elif 'username' in flask.session:
    #     username = flask.session["username"]
    # else:
    #     flask.abort(403)
    #
    # # First find largest postid.
    #
    # # Add database info to context check logged in user followed them
    # cul_fol = [i["username2"] for i in connection.execute(
    #     "SELECT username2 FROM following WHERE username1 = ?", (username,)
    # ).fetchall()]
    # cul_fol.append(username)
    # high_postid = connection.execute(
    #     "SELECT MAX(postid) FROM posts "
    #     f"WHERE owner IN ({','.join('?' * len(cul_fol))}) ", cul_fol
    # ).fetchone()["MAX(postid)"]
    # postid_lte = args.get('postid_lte', high_postid, int)
    # cur_post = connection.execute(
    #     "SELECT postid "
    #     "FROM posts "
    #     f"WHERE owner IN ({','.join('?' * len(cul_fol))}) "
    #     f"AND postid <= {postid_lte} "
    #     "ORDER BY created DESC, postid DESC ", cul_fol
    # )
    # # sample_create_time = cur_post.fetchall()[0]["created"]
    # # arrow.get(sample_create_time)
    # # return arrow.get(sample_create_time).humanize()
    # all_posts = cur_post.fetchall()
    # all_posts = all_posts[page * size:(page + 1) * size]
    # len_all_posts = len(all_posts)
    # res = [{"postid": i["postid"],
    #         "url": f"/api/v1/posts/{i['postid']}/"} for i
    #        in all_posts]
    # if len_all_posts < size:
    #     nexts = ""
    # else:
    #     nexts = f"/api/v1/posts/?size={size}&page={page+1}"\
    #             + f"&postid_lte={postid_lte}"
    """Display / route."""
    if 'name' not in flask.session:
        return flask.redirect(flask.url_for('create'))
    # print(os.getcwd())
    questions_images = [i for i in os.listdir('insta485/static/images') if
                        not i.startswith('.')]
    # print(questions_images)

    return flask.jsonify(**{"questions_images": questions_images, "url": "/api/v1/posts/"})

# @insta485.app.route('/api/v1/posts/<int:postid_url_slug>/', methods=['GET'])
# def get_post(postid_url_slug):
#     """Return post on postid."""
#     connection = insta485.model.get_db()
#     # Auth
#     if flask.request.authorization:
#         username = flask.request.authorization["username"]
#         authentication(username, flask.request.authorization["password"],
#                        connection)
#     elif 'username' in flask.session:
#         username = flask.session["username"]
#     else:
#         flask.abort(403)
#
#     post = connection.execute(
#         "SELECT filename, owner, created, postid "
#         "FROM posts "
#         "WHERE postid = ?",
#         (postid_url_slug,)
#     ).fetchone()
#     if not post:
#         return flask.abort(404)
#     # post["created"] = humanize_time(post["created"])
#     owner = post["owner"]
#
#     comments = connection.execute(
#         "SELECT owner, text, commentid "
#         "FROM comments "
#         "WHERE postid = ? "
#         "ORDER BY created, postid ",
#         (postid_url_slug,)
#     ).fetchall()
#     for comment in comments:
#         comment_owner = comment["owner"]
#         comment["lognameOwnsThis"] = (comment_owner == username)
#         comment["ownerShowUrl"] = f"/users/{comment_owner}/"
#         comment["url"] = f"/api/v1/comments/{comment['commentid']}/"
#
#     post["comments"] = comments
#
#     owner_img_url = connection.execute(
#         "SELECT filename "
#         "FROM users "
#         "WHERE username = ?",
#         (owner,)
#     ).fetchone()['filename']
#     img_url = post.pop("filename")
#     post["imgUrl"] = f"/uploads/{img_url}"
#     post["ownerImgUrl"] = f"/uploads/{owner_img_url}"
#
#     all_likes = connection.execute(
#         "SELECT likeid, owner "
#         "FROM likes "
#         "WHERE postid = ?",
#         (post["postid"],)
#     ).fetchall()
#     if all_likes:
#         num_likes = len(all_likes)
#         logname_likes_this = owner == username
#     else:
#         num_likes = 0
#         logname_likes_this = False
#     likes = {"lognameLikesThis": logname_likes_this, "numLikes": num_likes}
#     if owner == username:
#         owner_like = connection.execute("SELECT likeid "
#                                         "FROM likes "
#                                         "WHERE postid = ? AND owner = ?",
#                                         (post["postid"], owner)
#                                         ).fetchone()
#         if owner_like:
#             likes["url"] = f"/api/v1/likes/{owner_like['likeid']}/"
#         else:
#             likes["url"] = None
#     else:
#         likes["url"] = None
#     post["likes"] = likes
#     post["ownerShowUrl"] = f"/users/{owner}/"
#     post["postShowUrl"] = f"/posts/{postid_url_slug}/"
#     post["postid"] = postid_url_slug
#     post["url"] = flask.request.path
#     # post["logname_likes_post"] = bool(len(connection.execute(
#     #     "SELECT likeid "
#     #     "FROM likes "
#     #     "WHERE postid = ? AND owner = ?",
#     #     (postid_url_slug, username)
#     # ).fetchall()))
#     return flask.jsonify(**post)
