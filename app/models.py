from datetime import date, datetime

import pytz
from flask_login import UserMixin

from .extensions import db

class User(db.Model, UserMixin):

    id= db.Column(db.Integer, primary_key= True)
    user_name= db.Column(db.String(80), nullable= False, unique= True)
    email= db.Column(db.String(80), nullable= False, unique= True)
    password= db.Column(db.String(80), nullable= False, unique= True)
    date= db.Column(db.Date, default= date.today)

    def __repr__(self):

        return f"<user {self.user_name}>"
    
class Student(db.Model):

    id= db.Column(db.Integer, primary_key= True)

    name= db.Column(db.String(80), nullable= False)
    age= db.Column(db.Integer)
    sex= db.Column(db.String(80))
    instrument= db.Column(db.String(80))
    start_date= db.Column(db.Date)
    end_date= db.Column(db.Date)

    marked= db.Column(db.Boolean, default= False)

    user_id= db.Column(db.Integer, db.ForeignKey("user.id"), nullable= False)
    user= db.relationship("User", backref= db.backref("students", lazy= True))

    def __repr__(self):
        return f"<student {self.name}>"
    
class Attendance(db.Model):

    id= db.Column(db.Integer, primary_key= True)

    date= db.Column(db.Date, nullable= False)
    recipient_email= db.Column(db.String(80), nullable= False)
    attendance_data= db.Column(db.Text, nullable= False)
    date_and_time_sent= db.Column(db.DateTime, nullable= False, default= lambda: datetime.now(pytz.timezone("US/Eastern")))

    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    user= db.relationship('User', backref= db.backref('attendances', lazy= True))

    def __repr__(self):
        return f"<attendance sent on {self.date_and_time_sent} by user {self.user.user_name}>"