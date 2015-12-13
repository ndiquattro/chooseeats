# Flask Imports
from flask import flash, redirect, request, session
from . import auth
import ahelper


@auth.route('/')
def authuser():
    # Auth User
    fsauther = ahelper.FourAuther()
    uinfo = fsauther.auth(request.args.get('code'))

    # Save session
    session['userid'] = uinfo['id']

    # Make alert
    fullname = '{} {}'.format(uinfo['firstName'], uinfo['lastName'])
    flash('Thanks! You have been authenticated as %s' % fullname)

    return redirect('/index')


@auth.route('/logout')
def logout():

    # Remove session cookie
    session.clear()

    # Redirect to home
    return redirect('/index')
