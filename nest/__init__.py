from werkzeug.exceptions import BadRequest
from flask import Flask, render_template
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


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!' % e


@app.errorhandler(404)
def error404(error):
    return render_template("notfound.html", error=error), 404
