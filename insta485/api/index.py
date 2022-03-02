"""REST API for index page."""
import flask
import insta485


@insta485.app.route('/api/v1/', methods=['GET'])
def get_index():
    """Return API resource URLs."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)

@insta485.app.route('/record/', methods = ['POST', 'GET'])
def records():
    """Handle answers and get """
    jsons = flask.request.json
    if jsons:
        qn, qi, choice = jsons.get('qn'), jsons.get('qi'), jsons.get('choice')
        user = flask.session["name"]
        # return "success", 200
        # return flask.render_template("index.html")
        context = {
            "comments": "/api/v1/comments/",
            "likes": "/api/v1/likes/",
            "posts": "/api/v1/posts/",
            "url": "/api/v1/"
        }
        connection = insta485.model.get_db()
        connection.execute(
            "INSERT INTO answers(questionnumber, questionid, owner, answer) "
            "VALUES (?,?,?,?) ",
            (qn, qi, user, choice)
        )
    else:
        return "", 404
    # print(flask.session["name"])
    return "", 200