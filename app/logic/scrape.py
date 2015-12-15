import foursquare
from datetime import datetime
import os
import pandas as pd
import numpy as np
from config import FSCL, FSST

if os.uname()[0] == 'Darwin':
    redir = 'http://localhost:5000/auth'
else:
    redir = 'http://www.chooseeats.com/auth'


class UsrInfo(object):
    # Initialize
    def __init__(self, token):
        # Initiate Client
        self.client = foursquare.Foursquare(client_id=FSCL,
                                            client_secret=FSST,
                                            redirect_uri=redir,
                                            access_token=token)

    # Get Categories
    def get_foodcats(self):
        """
        Grabs list of restaurant categories from FourSquare.
        """
        # Grab food categories
        fcats = self.client.venues.categories()['categories'][3]['categories']

        # Pull out id and name
        rtypes = []
        for cat in fcats:
            rtypes.append([cat['name'], cat['id']])
        rtypes = pd.DataFrame(rtypes, columns=['rname', 'rid'])

        return rtypes

    # Get User info
    def get_userinfo(self):
        """
        Gets User information from Foursquare.
        """
        uinfo = self.client.users()['user']

        return uinfo

    # Get friends
    def get_friends(self):
        """
        Get list of current users friends.
        """
        # Grab data
        friends = self.get_userinfo()['friends']['groups']

        # Loop and get
        reflist = []
        for group in friends:
            # Get friends in group
            flist = group['items']

            # Get friend info
            for f in flist:
                purl = '%s128x128%s' % (f['photo']['prefix'],
                                        f['photo']['suffix'])
                churl = '/results/friend/%s' % (f['id'])
                reflist.append([int(f['id']),
                                f['firstName'],
                                f['lastName'],
                                purl,
                                churl])

        # Convert to pandas and return
        cnames = ['id', 'firstname', 'lastname', 'photo', 'churl']
        flist = pd.DataFrame(reflist, columns=cnames).sort('lastname')
        return flist

    # Get Checkins
    def get_checksins(self):

        # Grab data
        checkins = self.client.users.checkins()['checkins']['items']

        # Venue data
        ventype = self.get_foodcats()

        # Take out info we want
        cattime = []
        for check in checkins:
            # Get category
            cat = check['venue']['categories'][0]['name']
            catid = check['venue']['categories'][0]['id']

            cattime.append([check['createdAt'], cat, catid,
                            check['like'].conjugate()])

        # Convert to dataframe
        cnames = ['time', 'type', 'rid', 'like']
        cattime = pd.DataFrame(cattime, columns=cnames)

        # Only return food places
        cattime = cattime[cattime.rid.isin(ventype.rid)]

        # Summarise by food type
        cattime = cattime.groupby('type', as_index=False).agg({'like': np.mean,
                                                               'time': max})

        # Format and sort
        def difftime(oldtime):
            diff = datetime.now() - datetime.fromtimestamp(oldtime)
            return int(diff.days)

        def fortime(timest):
            newt = datetime.fromtimestamp(timest).strftime('%m-%d-%Y')
            return newt

        cattime['tsince'] = cattime.time.apply(difftime)
        cattime['lastti'] = cattime.time.apply(fortime)
        cattime = cattime.sort(['tsince', 'like'], ascending=[False, False])

        # Return
        return cattime
