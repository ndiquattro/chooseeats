import os
import foursquare
from app import chooseeats
from app import db, models

from config import FSST, FSCL

if os.uname()[0] == 'Darwin':
    redir = 'http://localhost:5000/auth'
else:
    redir = 'http://www.chooseeats.com/auth'


# Auther Class
class FourAuther(object):
    """
    Class for authenticating with Foursquare.
    """
    def __init__(self):
        # Initiate client
        self.auther = foursquare.Foursquare(client_id=FSCL,
                                            client_secret=FSST,
                                            redirect_uri=redir)

    def aurl(self):
        """
        Generates Authentication URL.
        """

        return self.auther.oauth.auth_url()

    def auth(self, code):
        """
        Auths with Foursquare and creates user
        """
        # Get token for user
        token = self.auther.oauth.get_token(str(code))

        # Get info we want to save
        infograb = chooseeats.usrinfo(token)
        uinfo = infograb.getUserInfo()

        # Check if we've already authed before
        curusr = models.User.query.filter_by(userid=uinfo['id']).first()
        if not curusr:
            newu = models.User(firstname=uinfo['firstName'],
                               lastname=uinfo['lastName'],
                               userid=uinfo['id'],
                               token=token)
            db.session.add(newu)
            db.session.commit()

        return uinfo
