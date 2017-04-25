from flask import Blueprint
from flask_login import LoginManager
from authomatic import Authomatic


login_manager = LoginManager()
login = Blueprint(
    'login',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@login.record_once
def on_load(state):
    login_manager.init_app(state.app)
    state.app.authomatic = Authomatic(
        state.app.config['AUTHOMATIC'],
        secret=state.app.secret_key
    )


from . import views  # noqa
