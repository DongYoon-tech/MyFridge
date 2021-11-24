from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateField, EmailField

class SignUpForm(FlaskForm):
    """Sign Up form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UserFoodForm(FlaskForm):
    """User Food form"""

    ingredient = StringField('Ingredient', validators=[DataRequired()])
    description = StringField('Description')
    # category = StringField('Category', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image = StringField('Image URL')
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    expiration_date = DateField('Expiration Date', validators=[DataRequired()])
    alarm_date = DateField('Alert Date', validators=[DataRequired()])

