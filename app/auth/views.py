# Flask Imports
from flask import flash, redirect, request, session
from app import app, db, models
import ahelper


@app.route('/')
def auth():
    # Auth User
    fsauther = ahelper.FourAuther()
    uinfo = fsauther.auth(request.args.get('code'))

    # Save session
    session['userid'] = uinfo['id']

    # Make alert
    fullname = '{} {}'.format(uinfo['firstName'], uinfo['lastName'])
    flash('Thanks! You have been autenticated as %s' % fullname)

    return redirect('/index')


@app.route('/deauth')
def deauth():
    # Grab userid
    usrid = session['userid']

    # Delete from database
    curusr = models.User.query.filter_by(userid=usrid).first()
    db.session.delete(curusr)
    db.session.commit()

    # Remove session cookie
    session.clear()

    # Redirect to home
    return redirect('/index')
