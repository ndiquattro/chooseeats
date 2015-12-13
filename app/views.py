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
        curusr = models.User.query.filter_by(userid=session['userid']).first()
        try:
            fname = '{} {}'.format(curusr.firstname, curusr.lastname)
            nickname = curusr.firstname
            session['fullname'] = fname
            session['firstname'] = nickname
        except:
            session.clear()
            return redirect('/index')
        aurl = None
    else:
        auther = ahelper.FourAuther()
        aurl = auther.aurl()
        user = None
        fname = None
        nickname = None

    return render_template('index.html',
                           title='Home',
                           user=nickname,
                           fulnm=fname,
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


@app.route('/results')
def results():
    # Get user info
    curusr = models.User.query.filter_by(userid=session['userid']).first()
    usr2 = None

    # Calculate values
    usr1 = chooseeats.usrinfo(curusr.token)
    rtab = usr1.getChecks()

    # Check if we're comparing or going solo
    friend = request.args.get('fid', '')
    if friend:
        # Get friend info
        fusr = models.User.query.filter_by(userid=friend).first()
        usr2 = fusr.firstname
        frinfo = chooseeats.usrinfo(fusr.token)
        finfo = frinfo.getChecks()

        # Compare results
        analyzer = chooseeats.analyze()
        rtab = analyzer.compHists(rtab, finfo)

    # Return table
    return render_template('results.html',
                           title='Results',
                           user=session['firstname'],
                           fulnm=session['fullname'],
                           user2=usr2,
                           data=rtab)





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
