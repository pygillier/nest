from flask import Flask
import os
from authomatic import Authomatic
from flask_boto3 import Boto3

app = Flask(__name__)
app.config.from_object(os.environ['app.settings'])

boto_flask = Boto3()
authomatic = Authomatic(
    app.config['AUTHOMATIC'],
    secret=app.secret_key,
    report_errors=app.debug
)

import nest.routes # noqa
