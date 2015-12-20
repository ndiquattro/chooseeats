from flask import (Blueprint, redirect, session, url_for, render_template,
                   request)
from ..logic import scrape, analysis
from ..database import models

# Register blueprint
results = Blueprint('results', __name__, url_prefix='/results')


@results.route('/')
def solo_results():
    # Check if user is authed
    if 'userid' in session:
        # Get user info
        curusr = models.User.lookup_user(session['userid'])
        fulnm = '{} {}'.format(curusr.firstname, curusr.lastname)

        # Calculate values
        usr1 = scrape.UsrInfo(curusr.token)
        rtab, uchecks = usr1.get_checksins()

        # Return table
        return render_template('results.html',
                               title='Results',
                               user=curusr.firstname,
                               uchecks=uchecks.to_json(orient='records'),
                               fulnm=fulnm,
                               data=rtab.to_json(orient='records'))
    else:
        redirect(url_for('home.index'))


@results.route('/friend/<int:fid>/')
def together_results(fid):
    if 'userid' in session:
        # Get current user info
        curusr = models.User.lookup_user(session['userid'])
        fulnm = '{} {}'.format(curusr.firstname, curusr.lastname)

        # Calculate values
        usr1 = scrape.UsrInfo(curusr.token)
        rtab, uchecks = usr1.get_checksins()
        print uchecks

        # Get friend info
        fusr = models.User.lookup_user(fid)
        frinfo = scrape.UsrInfo(fusr.token)
        finfo, fchecks = frinfo.get_checksins()

        # Compare results
        analyzer = analysis.Analyze()
        rtab = analyzer.comp_hists(rtab, finfo)

        # Return
        return render_template('results2.html',
                               title='Results',
                               user=curusr.firstname,
                               uchecks=uchecks.to_json(orient='records'),
                               fulnm=fulnm,
                               user2=fusr.firstname,
                               fid=fid,
                               fchecks=fchecks.to_json(orient='records'),
                               data=rtab.to_json(orient='records'))
    else:
        redirect(url_for('home.index'))
