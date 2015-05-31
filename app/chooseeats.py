import foursquare
from datetime import datetime
import csv, os
import pandas as pd
import numpy as np

# Set client & secret code
if os.uname()[0] == 'Darwin':
    redir = 'http://localhost:5000/auth'
    codepath = 'codes.csv'
else:
    redir = 'http://www.chooseeats.com/auth'
    codepath = '/home/nickof4/codes.csv'

with open(codepath, 'rb') as csvfile:
    codesf = csv.DictReader(csvfile)
    for row in codesf:
        codes = row

cid = codes['client']
csc = codes['secret']

# Make a auth class
class fourauther(object):
    def __init__(self):
        # Initiate client
        self.auther = foursquare.Foursquare(client_id = cid,
                                            client_secret = csc,
                                            redirect_uri = redir)

    # Make auth url
    def aurl(self):
        return self.auther.oauth.auth_url()

    # Exchange code for token
    def exch(self, code):
        return self.auther.oauth.get_token(str(code))

# Infograbber
class usrinfo(object):
    # initialize
    def __init__(self, token):
        # Initiate Client
        self.client = foursquare.Foursquare(client_id = cid,
                                            client_secret = csc,
                                            redirect_uri = redir,
                                            access_token = token)

    # Get Categories
    def getFoodCats(self):
        # Grab food categories
        fcats = self.client.venues.categories()['categories'][3]['categories']

        # Pull out id and name
        rtypes = []
        for cat in fcats:
            rtypes.append([cat['name'], cat['id']])
        rtypes = pd.DataFrame(rtypes, columns = ['rname', 'rid'])

        return rtypes

    # Get User info
    def getUserInfo(self):
        uinfo = self.client.users()['user']

        return uinfo

    # Get friends
    def getFriends(self):
        # Grab data
        friends = self.getUserInfo()['friends']['groups']

        # Loop and get
        reflist = []
        for group in friends:
            # Get friends in group
            flist = group['items']

            # Get friend info
            for f in flist:
                purl = '%s128x128%s' % (f['photo']['prefix'],
                                        f['photo']['suffix'])
                churl = '/results?fid=%s' % (f['id'])
                reflist.append([int(f['id']),
                                f['firstName'],
                                f['lastName'],
                                purl,
                                churl])

        # Convert to pandas and return
        cnames = ['id', 'firstname', 'lastname', 'photo', 'churl']
        flist = pd.DataFrame(reflist, columns = cnames)
        return flist

    # Get Checkins
    def getChecks(self):

        # Grab data
        checkins = self.client.users.checkins()['checkins']['items']

        # Venue data
        ventype = self.getFoodCats()

        # Take out info we want
        cattime = []
        for check in checkins:
            # Get category
            cat = check['venue']['categories'][0]['name']
            catid  = check['venue']['categories'][0]['id']

            cattime.append([check['createdAt'], cat, catid,
                            check['like'].conjugate()])

        # Convert to dataframe
        cnames = ['time', 'type', 'rid', 'like']
        cattime = pd.DataFrame(cattime, columns = cnames)

        # Only return food places
        cattime = cattime[cattime.rid.isin(ventype.rid)]

        # Summarise by food type
        cattime = cattime.groupby('type', as_index = False).agg({'like':np.mean,
                                                                'time':max})

        # Format and sort
        def difftime(oldtime):
            diff = datetime.now() - datetime.fromtimestamp(oldtime)
            return int(diff.days)

        def fortime(timest):
            newt = datetime.fromtimestamp(timest).strftime('%m-%d-%Y')
            return newt

        cattime['tsince'] = cattime.time.apply(difftime)
        cattime['lastti'] = cattime.time.apply(fortime)
        cattime = cattime.sort(['tsince', 'like'], ascending = [False, False])

        # Return
        return cattime

# Analysis class
class analyze(object):
    def __init__(self):
        pass

    # Time calcer
    def timeFinder(self, times):
        # Calculate
        tscore = times.mean(axis=1) * (times.max(axis=1) / times.min(axis=1))
        return tscore

    # Compare Histories
    def compHists(self, usr1, usr2):
        # Inner join to get only restaurants both have been to
        matched = usr1.merge(usr2, on = 'type')

        # Calculate mean time visited and like percentage
        matched['meantime'] = matched[['time_x', 'time_y']].mean(axis = 1)
        matched['meanlike'] = matched[['like_x', 'like_y']].mean(axis = 1)
        matched['recenyscr'] = self.timeFinder(matched[['time_x', 'time_y']])
        matched['reccoscr'] = matched.recenyscr * matched.meanlike

        # Sort by time then likes
        matched.sort('reccoscr')

        return matched
