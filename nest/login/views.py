from authomatic.adapters import WerkzeugAdapter
from flask import render_template, redirect, url_for, \
    make_response, request, session, current_app, flash
from flask_login import login_required, logout_user, login_user
from . import login_manager, login
from nest.models import db, User


@login_manager.user_loader
def load_user(user_id):
    """
    Retrieves a use from database
    Args:
        user_id: ID of user to retrieve

    Returns: User

    """
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template('forbidden.html')


@login.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been disconnected!")
    return redirect(url_for('home.index'))


@login.route('/login', methods=['GET', 'POST'])
def login():
    response = make_response()
    result = current_app.authomatic.login(
        WerkzeugAdapter(request, response),
        provider_name='google',
        session=session,
        session_saver=lambda: current_app.save_session(session, response)
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
                            picture=result.user.picture,
                            first_name=result.user.first_name)
                db.session.add(user)
                db.session.commit()
            login_user(user, remember=True)

        # The rest happens inside the template.
        flash("Welcome %s!" % result.user.name)
        return redirect(url_for('home.index'))

    # Don't forget to return the response.
    return response
