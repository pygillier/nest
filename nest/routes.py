from flask import render_template, flash, redirect
from flask import url_for, request, make_response, session
from flask_login import login_required, logout_user, login_user
from werkzeug.utils import secure_filename
from authomatic.adapters import WerkzeugAdapter
from . import app, boto_flask, authomatic
from .models import db, User
from .utils import allowed_file


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            boto_flask.clients['s3'].put_object(
                ACL='public-read',
                Bucket=app.config['S3_BUCKET'],
                Key=filename,
                Body=file,
            )
            flash("Your file has been uploaded successfully!")
            return redirect(url_for('list_uploaded_files'))


@app.route('/delete/<name>')
def delete_file(name):
    boto_flask.clients['s3'].delete_object(
        Bucket=app.config['S3_BUCKET'],
        Key=name
    )
    flash("File %s was deleted" % name)
    return redirect(url_for('list_uploaded_files'))


@app.route('/uploads')
@login_required
def list_uploaded_files():
    contents = boto_flask.clients['s3'].list_objects_v2(
        Bucket=app.config['S3_BUCKET']
    )
    return render_template('uploaded.html', contents=contents)


@app.route('/login', methods=['GET', 'POST'])
def login():
    response = make_response()
    result = authomatic.login(
        WerkzeugAdapter(request, response),
        provider_name='google',
        session=session,
        session_saver=lambda: app.save_session(session, response)
    )

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            user = User.query.filter_by(email=result.user.email).first()
            if user is None:
                user = User(email=result.user.email,
                            username=result.user.email.split('@')[0],
                            picture=result.user.picture)
                db.session.add(user)
                db.session.commit()
            login_user(user, remember=True)

        # The rest happens inside the template.
        flash("Welcome %s!" % result.user.name)
        return redirect(url_for('index'))

    # Don't forget to return the response.
    return response


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
