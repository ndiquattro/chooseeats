from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class userForm(Form):
    userid = StringField('userID', validators=[DataRequired()])
