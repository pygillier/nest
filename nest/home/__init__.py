from flask import Blueprint
from flask_boto3 import Boto3

home = Blueprint(
    'home',
    __name__,
    template_folder='templates',
    static_folder='static'
)

boto = Boto3()


@home.record_once
def on_load(state):
    boto.init_app(state.app)

from . import views  # noqa