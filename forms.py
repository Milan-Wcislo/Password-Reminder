from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AddPassword(FlaskForm):
    website_name = StringField('Website Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    website_password = PasswordField('Website Password', validators=[DataRequired()])
    submit = SubmitField('Add Password')


class EditPassword(FlaskForm):
    website_name = StringField('Website Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    old_website_password = StringField('Old Website Password', validators=[DataRequired()], render_kw={'disabled': True})
    website_password = PasswordField('New Website Password', validators=[DataRequired()])
    submit = SubmitField('Edit Password')
