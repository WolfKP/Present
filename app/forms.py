from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional

from .models import User

class LoginForm(FlaskForm):

    email= StringField("Email", validators= [DataRequired(),  Email()])
    password= PasswordField("Password", validators= [DataRequired()])

    submit= SubmitField("Submit")

class SignupForm(FlaskForm):

    user_name= StringField("User Name", validators= [DataRequired()])
    email= StringField("Email", validators= [DataRequired(), Email()])
    password= PasswordField("Password", validators= [DataRequired()])
    confirm_password= PasswordField("Confirm Password", validators= [DataRequired(), EqualTo("password")])
    submit= SubmitField("Submit")

    def validate_user_name(self, user_name):

        user= User.query.filter_by(user_name= user_name.data).first()

        if user:
            raise ValidationError("That user name is taken. Please choose a different one.")

    def validate_email(self, email):

        user= User.query.filter_by(email= email.data).first()

        if user:
            raise ValidationError("That email is taken. Please choose a different one.")
        
class NewStudentForm(FlaskForm):

    name= StringField("Name", validators=[Optional()])
    age= IntegerField("Age", validators=[Optional()])
    sex= StringField("Sex", validators=[Optional()])
    instrument= StringField("Instrument", validators=[Optional()])
    start_date= DateField("Start Date", validators=[Optional()])
    end_date= DateField("End Date", validators=[Optional()])

    add= SubmitField("Add")

class YourStudioForm(FlaskForm):

    mark_for_attendance= SubmitField("Mark for Attendance")
    delete= SubmitField("Delete")

class AttendanceSheetForm(FlaskForm):

    attendance_date= DateField("Attendance Date", validators=[Optional()])
    recipient_email= StringField("Recipient's Email", validators=[Optional(), Email()])
    send= SubmitField("Send")
    remove= SubmitField("Remove")

class AttendanceHistoryForm(FlaskForm):

    attendance_date= DateField("Attendance Date", validators=[Optional()])
    search= SubmitField("Search")

class YourDataForm(FlaskForm):

    clear_studio= SubmitField("Clear")
    clear_attendance_history= SubmitField("Clear")

class AccountDetailsForm(FlaskForm):

    user_name= StringField("New User Name", validators= [Optional()])
    email= StringField("New Email", validators= [Optional(), Email()])
    password= PasswordField("New Password", validators= [Optional(), EqualTo("confirm_password")])
    confirm_password= PasswordField("Confirm New Password", validators= [Optional(), EqualTo("password")])
    update= SubmitField("Update")