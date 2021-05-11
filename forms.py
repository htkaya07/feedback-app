from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from wtforms.fields.html5 import EmailField

class FeedBackForm(FlaskForm):
    title=StringField(
        "Title",
        validators=[InputRequired()],)
    content=StringField(
        "Content", 
        validators=[InputRequired()],)
    

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)],)
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)],)
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)],)
    email=EmailField("Email address",validators=[InputRequired(), Email(), Length(max=50)],)
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)],)
    
    



class SignInForm(FlaskForm):
    
    email=EmailField("Email address",validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
    

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
