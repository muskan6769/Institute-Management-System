from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,length,EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),length(min=2,max=50)])
    rollNo = StringField('EnRollNo',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    semester = IntegerField('Semester',validators=[DataRequired()])
    programme = StringField('Programme',validators=[DataRequired()])
    branch = StringField('Branch',validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class StudLoginForm(FlaskForm):
    rollNo = StringField('EnrollNo',validators=[DataRequired(),length(min=2,max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LogIn')

class FacLoginForm(FlaskForm):
    facCode = StringField('Faculty Code',validators=[DataRequired(),length(min=2,max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LogIn')




