from flask import Flask
import os
from .login import login
from .home import home
from .models import db

app = Flask(__name__)
app.config.from_object(os.environ['app.settings'])


db.init_app(app)

# Load login blueprint
app.register_blueprint(login)
app.register_blueprint(home)

with app.app_context():
    app.logger.info("Loading database schema")
    db.create_all()
