from flask import render_template
from . import login_manager
from nest.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template('forbidden.html')
