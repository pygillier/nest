from flask import current_app


def allowed_file(filename):
    with current_app.app_context():
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() \
               in current_app.config['ALLOWED_EXTENSIONS']
