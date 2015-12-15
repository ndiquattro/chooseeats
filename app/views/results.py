from flask import (Blueprint, redirect, request, session, url_for,
                   render_template)
from ..logic import scrape
from ..database import models

# Register blueprint
results = Blueprint('results', __name__, url_prefix='/results')


@results.route('/')
def solo_results():
    # Check if user is authed
    if 'userid' in session:
        # Get user info
        curusr = models.User.query.filter_by(userid=session['userid']).first()
        fulnm = '{} {}'.format(curusr.firstname, curusr.lastname)

        # Calculate values
        usr1 = scrape.UsrInfo(curusr.token)
        rtab = usr1.get_checksins()

        # Return table
        return render_template('results.html',
                               title='Results',
                               user=curusr.firstname,
                               fulnm=fulnm,
                               data=rtab)
    else:
        redirect(url_for('index'))


@results.route('/friend')
def together_results():
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