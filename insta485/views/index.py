"""
Insta485 index (main) view.

URLs include:
/

Le
"""
import flask
import insta485
import os
from insta485.views.utils import humanize_time


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'name' not in flask.session:
        return flask.redirect(flask.url_for('create'))
    # print(os.getcwd())
    questions_images = [i for i in os.listdir('insta485/static/images') if
                        not i.startswith('.')]
    # print(questions_images)
    return flask.render_template("index.html",
                                 **{"questions_images": questions_images})


