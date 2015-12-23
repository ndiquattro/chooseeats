import foursquare
import scrape
from ..database import models
from flask import current_app as capp


# Auther Class
class FourAuther(object):
    """
    Class for authenticating with Foursquare.
    """
    def __init__(self):
        # Initiate client
        self.auther = foursquare.Foursquare(client_id=capp.config['FSCL'],
                                            client_secret=capp.config['FSST'],
                                            redirect_uri=capp.config['REDIR'])

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
        infograb = scrape.UsrInfo(token)
        uinfo = infograb.get_userinfo()

        # Check if we've already authed before
        curusr = models.User.lookup_user(uinfo['id'])
        if not curusr:
            # Add user info
            uinfod = {'firstname': uinfo['firstName'],
                      'lastname': uinfo['lastName'],
                      'userid': uinfo['id'],
                      'token': token}

            models.User.add_user(uinfod)

        return uinfo
