from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateField

class SignUpForm(FlaskForm):
    """Sign Up form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UserFoodForm(FlaskForm):
    """User Food form"""

    ingredient = StringField('Ingredient', validators=[DataRequired()])
    description = StringField('Description')
    category = StringField('Category', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    image = StringField('Image')
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    expiration_date = DateField('Expiration Date', validators=[DataRequired()])
    

