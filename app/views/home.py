from flask import Blueprint, render_template, redirect, session
from app import db
from ..logic import authing, scrape
from ..database import models

# Register blueprint
home = Blueprint('home', __name__)


@home.route('/')
@home.route('/index')
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
        auther = authing.FourAuther()
        aurl = auther.aurl()

        return render_template('index.html',
                               title='Home',
                               authurl=aurl)


@home.route('/friends')
def friends():
    # Check if authed
    if 'userid' in session:
        # Look up user
        curusr = models.User.query.filter_by(userid=session['userid']).first()
        fname = '{} {}'.format(curusr.firstname, curusr.lastname)

        # Get list of auth'd IDs
        authids = []
        uids = db.session.query(models.User.userid)
        for u in uids:
            authids.append(u[0])

        # Find friends
        usr1 = scrape.UsrInfo(curusr.token)
        finfo = usr1.get_friends()

        # Keep friends who have authed
        finfo = finfo[finfo['id'].isin(authids)]

        return render_template('friends.html',
                               title='Friends',
                               user=curusr.firstname,
                               fulnm=fname,
                               flist=finfo)
    else:
        redirect('/')


@home.route('/about')
def about():
    # Check if this person has authed
    if 'userid' in session:
        return render_template('about.html')
    else:
        auther = authing.FourAuther()
        aurl = auther.aurl()

        return render_template('about.html',
                               authurl=aurl)
