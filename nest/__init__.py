from flask import Flask
import os
from .login import login
from authomatic import Authomatic
from flask_boto3 import Boto3
from .models import db

app = Flask(__name__)
app.config.from_object(os.environ['app.settings'])

authomatic = Authomatic(
    app.config['AUTHOMATIC'],
    secret=app.secret_key,
    report_errors=app.debug
)

boto_flask = Boto3(app)
db.init_app(app)

# Load login blueprint
app.register_blueprint(login)

with app.app_context():
    app.logger.info("Loading database schema")
    db.create_all()

import nest.routes  # noqa
