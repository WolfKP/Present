from flask import Blueprint, current_app, render_template, url_for, redirect, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message

from .extensions import db, bcrypt, login_manager, mail
from .forms import LoginForm, SignupForm, NewStudentForm, YourStudioForm, AttendanceSheetForm, AttendanceHistoryForm, YourDataForm, AccountDetailsForm
from .models import db, User, Student, Attendance

main= Blueprint("main", __name__)

@login_manager.user_loader
def load_user(id):

    return User.query.get(int(id))

@main.route("/", methods= ["GET", "POST"])
def login():

    form= LoginForm()

    if form.validate_on_submit():

        user= User.query.filter_by(email= form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user)

            return redirect(url_for("main.studio", 
                                    user_name= user.user_name))
        
        else:
            flash("Incorrect user name or password.", "failure")

    return render_template("login.html", form= form)

@main.route("/signup", methods= ["GET", "POST"])
def signup():

    form= SignupForm()

    if form.validate_on_submit():

        hashed_password= bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user= User(user_name= form.user_name.data, 
                   email= form.email.data, 
                   password= hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Account created.", "success")

        return redirect(url_for("main.login"))
    
    return render_template("signup.html", 
                           form= form)

@main.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("main.login"))

@main.route("/<user_name>/studio", methods= ["GET", "POST"])
@login_required
def studio(user_name):

    if current_user.user_name != user_name:

        flash("You don't have permission to access this page.", "failure")

        return redirect(url_for("main.login"))
    
    new_student_form= NewStudentForm()
    your_studio_form= YourStudioForm()
    current_students= Student.query.filter_by(user_id= current_user.id).all()
    studio_size= Student.query.filter_by(user_id= current_user.id).count()
    average_age= db.session.query(db.func.avg(Student.age)).filter_by(user_id= current_user.id).scalar()
    sex_makeup= db.session.query(Student.sex, db.func.count(Student.sex)).filter_by(user_id= current_user.id).group_by(Student.sex).all()

    return render_template("studio.html", 
                           user= current_user, 
                           new_student_form= new_student_form, 
                           your_studio_form= your_studio_form, 
                           current_students= current_students,
                           studio_size= studio_size, 
                           average_age= average_age, 
                           sex_makeup= sex_makeup)

@main.route("/your_studio", methods= ["POST"])
@login_required
def your_studio():

    form= YourStudioForm()

    student_ids= request.form.getlist("selected_students")

    if form.validate_on_submit():

        if form.mark_for_attendance.data:

            for student_id in student_ids:

                student= Student.query.get(student_id)
                student.marked= True

            db.session.commit()
            
            return redirect(url_for("main.studio", 
                                    user_name= current_user.user_name))
        
        else:

            for student_id in student_ids:

                student= Student.query.get(student_id)
                db.session.delete(student)

            db.session.commit()

            return redirect(url_for("main.studio", 
                                    user_name= current_user.user_name))

    return redirect(url_for("main.studio", 
                            user_name= current_user.user_name))

@main.route("/new_student", methods= ["POST"])
@login_required
def new_student():

    form= NewStudentForm()

    if form.validate_on_submit():

        name= form.name.data

        if not name:

            flash("Please enter a name.", "failure")

            return redirect(url_for("main.studio", 
                            user_name= current_user.user_name))

        student= Student(name= name, 
                         age= form.age.data, 
                         sex= form.sex.data, 
                         instrument= form.instrument.data,
                         start_date= form.start_date.data, 
                         end_date= form.end_date.data, 
                         user_id= current_user.id)
        db.session.add(student)
        db.session.commit()

    return redirect(url_for("main.studio", 
                            user_name= current_user.user_name))

@main.route("/<user_name>/attendance", methods= ["GET", "POST"])
@login_required
def attendance(user_name):

    if current_user.user_name != user_name:

        flash("You don't have permission to access this page.", "failure")

        return redirect(url_for("main.login"))
    
    attendance_sheet_form= AttendanceSheetForm()
    attendance_history_form= AttendanceHistoryForm()

    marked_students= Student.query.filter_by(user_id= current_user.id, marked= True).all()
    attendances= None

    if attendance_history_form.validate_on_submit():

        attendance_date= attendance_history_form.attendance_date.data

        if not attendance_date:

            flash("Please enter a date.", "failure")
                
            return redirect(url_for("main.attendance", 
                                    user_name= current_user.user_name))

        attendances= Attendance.query.filter_by(date= attendance_date, user_id= current_user.id).all()

    return render_template("attendance.html", 
                           user= current_user, 
                           attendance_sheet_form= attendance_sheet_form,
                           attendance_history_form= attendance_history_form, 
                           marked_students= marked_students,
                           attendances= attendances)

@main.route("/attendance_sheet", methods= ["POST"])
@login_required
def attendance_sheet():

    form= AttendanceSheetForm()

    selected_student_ids= request.form.getlist("selected_students")
    marked_student_ids= request.form.getlist("marked_students")

    if form.validate_on_submit():

        attendance_date= form.attendance_date.data
        recipient_email= form.recipient_email.data

        attendance_data= []

        if form.send.data: 

            if not attendance_date:

                flash("Please enter a date.", "failure")
                
                return redirect(url_for("main.attendance", 
                                        user_name= current_user.user_name))

            if not recipient_email:

                flash("Please enter a recipient's email.", "failure")

                return redirect(url_for("main.attendance", 
                                        user_name= current_user.user_name))

            for student_id in marked_student_ids:

                student= Student.query.filter_by(id= student_id).first()
                student_name= student.name
                attendance_status= request.form.get(f"attendance_status_{student_id}")

                attendance_data.append((student_name, attendance_status))

            attendance_data= "<br>".join([f"{name}: {status}" for name, status in attendance_data])

            attendance_record= Attendance(date= attendance_date,
                                          recipient_email= recipient_email,
                                          attendance_data= attendance_data,
                                          user_id= current_user.id)
            db.session.add(attendance_record)
            db.session.commit()

            message= Message(f"{current_user.user_name}'s Attendance", sender= current_app.config["MAIL_USERNAME"], recipients= [recipient_email, current_user.email]) 
            message.html= attendance_sheet_aux(attendance_date, attendance_data)

            with current_app.app_context():
                mail.send(message)

            flash("Email sent.", "success")

            return redirect(url_for("main.attendance", 
                                    user_name=current_user.user_name))

        else:

            for student_id in selected_student_ids:

                student= Student.query.filter_by(id= student_id).first()
                student.marked= False
            
            db.session.commit()

            return redirect(url_for("main.attendance", 
                                    user_name= current_user.user_name))
        
    else:
            return redirect(url_for("main.attendance", 
                                    user_name= current_user.user_name))

def attendance_sheet_aux(attendance_date, attendance_data):

    attendance_count= Student.query.filter_by(user_id= current_user.id, marked= True).count()

    message_body= f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: 'Courier New', Courier, monospace;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: linear-gradient(to bottom, darkslategray, steelblue); padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: papayawhip; border-radius: 6px; box-shadow: 0px 4px 8px rgba(0, 0, 0, .35);">
                            <tr>
                                <td style="font-size: 14px; padding: 20px;">
                                    <p style="margin: 0;">
                                    Hi,
                                    </p>
                                    <br>
                                    <p style="margin: 0;">
                                        Here is the attendance for <strong>{attendance_date}</strong>:
                                    </p>
                                    <br>
                                    <p style="margin: 0;">
                                        -- <strong><span style="color: red;">{attendance_count}</span></strong> --
                                    </p>
                                    <br>
                                    <p style="margin: 0;">
                                        {attendance_data}
                                    </p>
                                    <br>
                                    <p style="margin: 0;">
                                        Thank you,<br>
                                        {current_user.user_name}
                                    </p>
                                    <br>
                                    <p style="margin: 0;">
                                        This message was automated using <span style="color: steelblue; font-weight: bold;">Present</span>.
                                    </p>
                                    <p style="margin: 0;">
                                        Please direct replies to {current_user.email}.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    return message_body

@main.route("/<user_name>/user_profile", methods= ["GET", "POST"])
@login_required
def user_profile(user_name):

    if current_user.user_name != user_name:

        flash("You don't have permission to access this page.", "failure")

        return redirect(url_for("main.login"))
    
    your_data_form= YourDataForm()
    account_details_form= AccountDetailsForm()

    studio_size= Student.query.filter_by(user_id= current_user.id).count()
    attendance_history_size= Attendance.query.filter_by(user_id= current_user.id).count()

    return render_template("user-profile.html", 
                           user= current_user,
                           your_data_form= your_data_form,
                           account_details_form= account_details_form,
                           studio_size= studio_size,
                           attendance_history_size= attendance_history_size)

@main.route("/your_data", methods= ["POST"])
@login_required
def your_data():
    
    form= YourDataForm()

    if form.clear_studio.data:

        Student.query.filter_by(user_id= current_user.id).delete()
        db.session.commit()

    else:

        Attendance.query.filter_by(user_id= current_user.id).delete()
        db.session.commit()

    return redirect(url_for("main.user_profile", user_name= current_user.user_name))   

@main.route("/account_details", methods= ["POST"])
@login_required
def account_details():

    form= AccountDetailsForm()

    if form.validate_on_submit():

        new_user_name= form.user_name.data
        new_email= form.email.data
        new_password= form.password.data

        if new_user_name and User.query.filter_by(user_name= new_user_name).first():

            flash("That user name is taken. Please choose a different one.", "failure")
            
            return redirect(url_for("main.user_profile", 
                                user_name= current_user.user_name))
    
        if new_email and User.query.filter_by(email= new_email).first():
            
            flash("That email is taken. Please choose a different one.", "failure")
            
            return redirect(url_for("main.user_profile", 
                                    user_name= current_user.user_name))
    
        if new_user_name:

            current_user.user_name= new_user_name

            flash("User name updated.", "success")

        if new_email:

            current_user.email= new_email

            flash("Email updated.", "success")
    
        if new_password:

            hashed_password= bcrypt.generate_password_hash(new_password).decode("utf-8")
            current_user.password= hashed_password

            flash("Password updated.", "success")

        db.session.commit()

    return redirect(url_for("main.user_profile", 
                            user_name= current_user.user_name))
    
