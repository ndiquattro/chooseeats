# Flask Imports
from flask import Blueprint, flash, redirect, request, session, url_for
from ..logic import authing

# Initiate Blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/')
def authuser():
    # Auth User
    fsauther = authing.FourAuther()
    uinfo = fsauther.auth(request.args.get('code'))

    # Save session
    session.permanent = True
    session['userid'] = uinfo['id']

    # Make alert
    fullname = '{} {}'.format(uinfo['firstName'], uinfo['lastName'])
    flash('Thanks! You have been authenticated as %s' % fullname)

    return redirect(url_for('home.index'))


@auth.route('/logout')
def logout():

    # Remove session cookie
    session.clear()

    # Redirect to home
    return redirect(url_for('home.index'))
