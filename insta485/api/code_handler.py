"""Define all Error Handlers."""
import flask
import insta485


@insta485.app.errorhandler(400)
def handle_bad_request(error):
    """Handle bad request."""
    return flask.jsonify(**{
        "message": "Bad Request",
        "status_code": error.code
    }), error.code


@insta485.app.errorhandler(403)
def handle_forbidden(error):
    """Handle 403."""
    return flask.jsonify(**{
        "message": "Forbidden",
        "status_code": error.code
    }), error.code


@insta485.app.errorhandler(404)
def handle_not_found(error):
    """Handle 404."""
    return flask.jsonify(**{
        "message": "Not Found",
        "status_code": error.code
    }), error.code
