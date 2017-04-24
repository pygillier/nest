from flask_script import Manager
from nest import app, boto_flask
from nest.login import login_manager
from nest.models import db


def init_app():
    login_manager.init_app(app)
    boto_flask.init_app(app)
    db.init_app(app)


if __name__ == '__main__':
    init_app()
    with app.app_context():
        db.create_all()
    manager = Manager(app)
    manager.run()
