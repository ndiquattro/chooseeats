# API Imports
import chooseeats
from auth import ahelper

# Flask Imports
from flask import render_template, flash, redirect, request, session
from app import app, db, models


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Check if this person has authed
    if 'userid' in session:
        # Look up user info
        curusr = models.User.query.filter_by(userid=session['userid']).first()

        # Pull out info we want
        fname = '{} {}'.format(curusr.firstname, curusr.lastname)
        nickname = curusr.firstname

        # Return Template
        return render_template('index.html',
                               title='Home',
                               user=nickname,
                               fulnm=fname)
    else:
        # Send auth URL
        auther = ahelper.FourAuther()
        aurl = auther.aurl()

        return render_template('index.html',
                               title='Home',
                               authurl=aurl)


@app.route('/friends')
def friends():
    # look up logged in user
    curusr = models.User.query.filter_by(userid=session['userid']).first()

    # Get list of auth'd IDs
    authids = []
    uids = db.session.query(models.User.userid)
    for u in uids:
        authids.append(u[0])

    # Find friends
    usr1 = chooseeats.usrinfo(curusr.token)
    finfo = usr1.getFriends()

    # Keep friends who have authed
    finfo = finfo[finfo['id'].isin(authids)]

    return render_template('friends.html',
                           title='Friends',
                           user=session['firstname'],
                           fulnm=session['fullname'],
                           flist=finfo)








@app.route('/about')
def about():
    # Check if this person has authed
    if 'userid' in session:
        aurl = None
    else:
        auther = chooseeats.fourauther()
        aurl = auther.aurl()
        user = None
        fname = None
        nickname = None
    return render_template('about.html',
                           authurl=aurl)
