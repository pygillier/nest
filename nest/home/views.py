from flask import render_template, redirect, request,\
    flash, current_app, url_for
from werkzeug.utils import secure_filename

from . import boto, home
from .utils import allowed_file
from flask_login import login_required


@home.route('/')
@login_required
def index():
    return render_template("index.html")


@home.route('/upload', methods=['GET', 'POST'])
@login_required
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
            boto.clients['s3'].put_object(
                ACL='public-read',
                Bucket=current_app.config['S3_BUCKET'],
                Key=filename,
                Body=file,
            )
            flash("Your file has been uploaded successfully!")
            return redirect(url_for('home.list_uploaded_files'))
        else:
            flash("This type of file is forbidden.")
            return redirect(request.url)
    else:
        return render_template('index.html')


@home.route('/delete/<name>')
@login_required
def delete_file(name):
    boto.clients['s3'].delete_object(
        Bucket=current_app.config['S3_BUCKET'],
        Key=name
    )
    flash("File %s was deleted" % name)
    return redirect(url_for('home.list_uploaded_files'))


@home.route('/uploads')
@login_required
def list_uploaded_files():
    contents = boto.clients['s3'].list_objects_v2(
        Bucket=current_app.config['S3_BUCKET']
    )
    return render_template('uploaded.html', contents=contents)
