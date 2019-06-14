import os
import secrets
from PIL import Image
from flask_mysqldb import MySQL
from mysql.connector import Error
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewStudentForm, UpdateStudentForm, NewStaffForm, NewAdministratorForm, NewTeacherForm, NewContactForm, UpdateStaffForm, UpdateAdministratorForm, NewCourseForm, EnrollForm, GradeForm, DisciplineForm, AbsenceForm, AttendanceForm
from flaskDemo.models import User, Staff, Administrator, Teacher, Absences, Classroom, Courses, Discipline, Enrollment, Student, Student_Attendance, Emergency_Contact, Staff_Emergencycontact, Student_Emergencycontact
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy.sql import and_, or_


def students():
 student=Student.query.with_entities(Student.SSN, Student.LastName)
 myChoices3 = [(row[0],row[1]) for row in student]  # change
 results=list()			 
 for row in student:
    rowDict=row._asdict()
    results.append(rowDict)
 students = [(row['SSN'], row['LastName']) for row in results]
 return students
 

def classes(): 
 classs=Courses.query.with_entities(Courses.CourseID, Courses.Course_Name)
 myChoices4 = [(row[0],row[1]) for row in classs]  # change
 results=list()			 
 for row in classs:
    rowDict=row._asdict()
    results.append(rowDict)
 classes2 = [(row['CourseID'], row['Course_Name']) for row in results]
 return classes2

def teachers():
 teacher=Staff.query.filter(Staff.Person_Type ==2).add_columns(Staff.SSN, Staff.LastName)
 myChoices2 = [(row[0],row[1]) for row in teacher]  # change
 results=list()			 
 for row in teacher:
    rowDict=row._asdict()
    results.append(rowDict)
 teacherChoices = [(row['SSN'],row['LastName']) for row in results]
 return teacherChoices

def administrators():
 administrator=Staff.query.with_entities(Staff.SSN, Staff.LastName).filter(Staff.Person_Type==1)
 myChoices6 = [(row[0],row[1]) for row in administrator]  # change
 results=list()			 
 for row in administrator:
    rowDict=row._asdict()
    results.append(rowDict)
 administrators2 = [(row['SSN'], row['LastName']) for row in results]
 return administrators2

def staffs():
 staff=Staff.query.with_entities(Staff.SSN, Staff.LastName)
 myChoices7 = [(row[0],row[1]) for row in staff]  # change
 results=list()			 
 for row in staff:
    rowDict=row._asdict()
    results.append(rowDict)
 staffs2 = [(row['SSN'], row['LastName']) for row in results]
 return staffs2







@app.route("/")
@app.route("/home")
def home():
    
    courses9 = db.engine.execute("SELECT Grade_Level, Course_Name FROM courses WHERE Grade_Level=9")
    courses10 = db.engine.execute("SELECT Grade_Level, Course_Name FROM courses WHERE Grade_Level=10")
    courses11 = db.engine.execute("SELECT Grade_Level, Course_Name FROM courses WHERE Grade_Level=11")
    courses12 = db.engine.execute("SELECT Grade_Level, Course_Name FROM courses WHERE Grade_Level=12")	
    return render_template('highschool_home.html', title='Home',courses9=courses9, courses10=courses10, courses11=courses11, courses12=courses12)
	
	
        
@app.route("/student", methods=['GET','POST'])
@login_required
def student():
    students = Student.query.add_columns(Student.SSN, Student.LastName, Student.FirstName).all()
    return render_template('highschool_student.html', students=students, now=datetime.utcnow())
	
	
@app.route("/student/<SSN>/student_options", methods=['GET','POST'])
@login_required
def student_options(SSN):
   student = Student.query.get_or_404(SSN)
   return render_template('highschool_student_options.html', student=student, now=datetime.utcnow())


@app.route("/student/new_student", methods=['GET','POST'])
@login_required
def new_student():
    form = NewStudentForm()
    
    if form.validate_on_submit():
        student_new = Student(SSN=form.ssn.data, LastName=form.lname.data, FirstName=form.fname.data, Address=form.address.data, City=form.city.data, State=form.state.data, Zip_Code=form.zip.data, Phone_Number=form.phone.data, Grade_Level=form.grade.data, GPA=0.0)
        db.session.add(student_new)
        db.session.commit()
        flash('You have added a new student!', 'success')
        return redirect(url_for('student'))
    return render_template('highschool_newstudent.html', title="New Student", form=form, legend = "New Student") 	

	
@app.route("/student/<SSN>/update_student", methods=['GET','POST'])
@login_required
def update_student(SSN):
    student = Student.query.get_or_404(SSN)

    form = UpdateStudentForm()
    
    if form.validate_on_submit():
        student.SSN=form.ssn.data
        student.LastName=form.lname.data
        student.FirstName=form.fname.data
        student.Address=form.address.data
        student.City=form.city.data
        student.State=form.state.data
        student.Zip_Code=form.zip.data
        student.Phone_Number=form.phone.data
        student.Grade_Level=form.grade.data
        db.session.commit()
        flash('You have updated a student!', 'success')
        return redirect(url_for('student'))
    elif request.method=='GET':
        form.ssn.data=student.SSN
        form.lname.data=student.LastName
        form.fname.data=student.FirstName
        form.address.data=student.Address
        form.city.data=student.City
        form.state.data=student.State
        form.zip.data=student.Zip_Code
        form.phone.data=student.Phone_Number
        form.grade.data=student.Grade_Level
    return render_template('highschool_updatestudent.html', title="Update Student", form=form, legend = "Update Student") 


@app.route("/student/<SSN>/remove_student", methods=['POST'])
@login_required
def remove_student(SSN):
    deleting = Student.query.get_or_404([SSN])
    db.session.delete(deleting)
    db.session.commit()
    flash('The student has been deleted from the database.', 'success')
    return redirect(url_for('student'))

	
@app.route("/staff", methods=['GET','POST'])
@login_required
def staff():
    staff = Staff.query.add_columns(Staff.SSN, Staff.LastName, Staff.FirstName, Staff.Person_Type).all()
    return render_template('highschool_staff.html', staff=staff, now=datetime.utcnow())
	
	
@app.route("/staff/<SSN>/staff_options", methods=['GET','POST'])
@login_required
def staff_options(SSN):
   staff = Staff.query.get_or_404(SSN)
   return render_template('highschool_staff_options.html', staff=staff, now=datetime.utcnow())


@app.route("/staff/new_staff", methods=['GET','POST'])
@login_required
def new_staff():
    form = NewStaffForm()
    
    if form.validate_on_submit():
        staff_new = Staff(SSN=form.ssn.data, LastName=form.lname.data, FirstName=form.fname.data, Address=form.address.data, City=form.city.data, State=form.state.data, Zip_Code=form.zip.data, Phone_Number=form.phone.data, Person_Type=form.type.data, Salary=form.salary.data)
        db.session.add(staff_new)
        db.session.commit()
        if form.type.data != 1 and form.type.data != 2:
            flash('You have added a new member of your staff.', 'success')
            return redirect(url_for('staff'))
        elif form.type.data == 1:
            return redirect(url_for('new_administrator', SSN=form.ssn.data))
        elif form.type.data == 2:
            return redirect(url_for('new_teacher', SSN=form.ssn.data))
    return render_template('highschool_newstaff.html', title="New Staff", form=form, legend = "New Staff") 	

	
@app.route("/staff/new_staff/<SSN>/new_administrator", methods=['GET','POST'])
@login_required
def new_administrator(SSN):
    administrator=Staff.query.get_or_404(SSN)
    form=NewAdministratorForm()
	
    if form.validate_on_submit():
        administrator_new=Administrator(SSN = administrator.SSN, Office_Number = form.office.data, Degree=form.degree.data)
        db.session.add(administrator_new)
        db.session.commit()
        flash('You have added a new administrator to your staff.', 'success')
        return redirect(url_for('staff'))
    return render_template('highschool_newadministrator.html', title="New Administrator", form=form, legend = "New Administrator")

		
@app.route("/staff/new_staff/<SSN>/new_teacher", methods=['GET','POST'])
@login_required
def new_teacher(SSN):
    teacher=Staff.query.get_or_404(SSN)	
    form=NewTeacherForm()

    if form.validate_on_submit():
        teacher_new=Teacher(SSN = teacher.SSN, Certification = form.certification.data)
        db.session.add(teacher_new)
        db.session.commit()
        flash('You have added a new teacher to your staff.', 'success')
        return redirect(url_for('staff'))
    return render_template('highschool_newteacher.html', title="New Teacher", form=form, legend = "New Teacher")
			
			
			
@app.route("/staff/<SSN>/remove_staff", methods=['POST'])
@login_required
def remove_staff(SSN):
    deleting = Staff.query.get_or_404([SSN])
    db.session.delete(deleting)
    db.session.commit()
    flash('The staff has been deleted from the database.', 'success')
    return redirect(url_for('staff'))
	
	
@app.route("/newcontact/<SSN>", methods=['GET','POST'])
@login_required
def new_contact(SSN):
    
    student = Student.query.filter_by(SSN=SSN).scalar() is not None
    staff=Staff.query.filter_by(SSN=SSN).scalar() is not None
    form = NewContactForm()
    			
    if form.validate_on_submit():
        exists = Emergency_Contact.query.filter_by(ContactID=form.contactID.data).scalar() is not None	
        if exists==False:
            contact1=Emergency_Contact(ContactID=form.contactID.data, Last_Name=form.lname.data, First_Name=form.fname.data, Address=form.address.data, City=form.city.data, State=form.state.data, Zip_Code=form.zip.data, Phone_Number=form.phone.data)		
            db.session.add(contact1)
            db.session.commit()
        if student==True:
            contact = Student_Emergencycontact(SSN=form.ssn.data, ContactID=form.contactID.data)
            db.session.add(contact)
            db.session.commit()
        elif staff==True:
            contact2 = Staff_Emergencycontact(SSN=form.ssn.data, ContactID=form.contactID.data)
            db.session.add(contact2)
            db.session.commit()
        flash('You have added a new emergency contact.', 'success')
        return redirect(url_for('home'))
    elif request.method=='GET':
        form.ssn.data=SSN
    return render_template('highschool_newcontact.html', title="New Emergency Contact", form=form, legend = "New Emergency Contact") 	
	

@app.route("/displays_options/display_contacts", methods=['GET','POST'])
@login_required
def display_contacts():
    contactstudent=Student.query.join(Student_Emergencycontact,Student.SSN == Student_Emergencycontact.SSN) \
               .add_columns(Student.LastName, Student.FirstName) \
               .join(Emergency_Contact, Emergency_Contact.ContactID == Student_Emergencycontact.ContactID) \
               .add_columns(Emergency_Contact.Last_Name, Emergency_Contact.First_Name, Emergency_Contact.Phone_Number) \
               .order_by(Student.LastName.asc()) # This row :)
    
    contactstaff=Staff.query.join(Staff_Emergencycontact,Staff.SSN == Staff_Emergencycontact.SSN) \
               .add_columns(Staff.LastName, Staff.FirstName) \
               .join(Emergency_Contact, Emergency_Contact.ContactID == Staff_Emergencycontact.ContactID) \
               .add_columns(Emergency_Contact.Last_Name, Emergency_Contact.First_Name, Emergency_Contact.Phone_Number) \
               .order_by(Staff.LastName.asc()) # This row :)
    return render_template('highschool_displaycontact.html', title='Emergency Contacts', contactstudent=contactstudent, contactstaff=contactstaff, legend = 'Emergency Contacts')

	
@app.route("/staff/<SSN>/update_staff", methods=['GET','POST'])
@login_required
def update_staff(SSN):
    staff = Staff.query.get_or_404(SSN)

    form = UpdateStaffForm()
    
    if form.validate_on_submit():
        staff.SSN=form.ssn.data
        staff.LastName=form.lname.data
        staff.FirstName=form.fname.data
        staff.Address=form.address.data
        staff.City=form.city.data
        staff.State=form.state.data
        staff.Zip_Code=form.zip.data
        staff.Phone_Number=form.phone.data
        staff.Person_Type=form.type.data
        staff.Salary=form.salary.data
        db.session.commit()
        if staff.Person_Type != 1:
            flash('You have updated a staff member.', 'success')
            return redirect(url_for('staff'))
        elif staff.Person_Type == 1:
            return redirect(url_for('update_administrator', SSN=form.ssn.data))
    elif request.method=='GET':
        form.ssn.data=staff.SSN
        form.lname.data=staff.LastName
        form.fname.data=staff.FirstName
        form.address.data=staff.Address
        form.city.data=staff.City
        form.state.data=staff.State
        form.zip.data=staff.Zip_Code
        form.phone.data=staff.Phone_Number
        form.type.data=staff.Person_Type
        form.salary.data=staff.Salary
    return render_template('highschool_updatestaff.html', title="Update Staff", form=form, legend = "Update Staff") 

	
@app.route("/staff/update_staff/<SSN>/update_administrator", methods=['GET','POST'])
@login_required
def update_administrator(SSN):
    administrator=Administrator.query.get_or_404(SSN)
    form=UpdateAdministratorForm()
	
    if form.validate_on_submit():
        administrator.Office_Number=form.office.data
        db.session.commit()
        flash('You have updated an administrator','success')
        return redirect(url_for('staff'))
    elif request.method=='GET':
        form.office.data=administrator.Office_Number
    return render_template('highschool_updateadministrator.html', title="Update Administrator", form=form, legend="Update Administrator")
			

@app.route("/courses")
@login_required
def courses():
   courses = Courses.query.add_columns(Courses.CourseID, Courses.Course_Name, Courses.Grade_Level)
   return render_template('highschool_courses.html', courses=courses, now=datetime.utcnow())


@app.route("/newcourses", methods=['GET','POST'])
@login_required
def new_courses():
    form = NewCourseForm()
    form.teacher.choices=teachers()
		
    if form.validate_on_submit():
        course_new = Courses(CourseID=form.course.data, Course_Name=form.cname.data, Grade_Level=form.grade.data, Teacher_SSN=form.teacher.data, Classroom_Number=form.classroom.data)
        db.session.add(course_new)
        db.session.commit()
        flash('You have added a new course.', 'success')
        return redirect(url_for('courses'))
    
    return render_template('highschool_newcourse.html', title="New Course", form=form, legend = "New Course") 
   

   
@app.route("/student/<SSN>/enroll", methods=['GET', 'POST'])
@login_required
def enroll(SSN):
    form = EnrollForm()
    form.ssn.choices=students()
    form.classid.choices=classes()

    if form.validate_on_submit():
        enroll = Enrollment(StudentSSN=form.ssn.data, ClassID=form.classid.data, Grade=0.0)
        db.session.add(enroll)
        db.session.commit()
        flash('You have added a student to a class.', 'success')
        return redirect(url_for('student'))
    
    return render_template('highschool_enroll.html', title='Place Student in Class',
                           form=form, legend='Place Student in Class')

					   
@app.route("/student/<SSN>/inputgrade", methods=['GET','POST'])
@login_required
def input_grade(SSN):
    grade = Enrollment.query.filter_by(StudentSSN=SSN).first()
    if grade==None:
        flash('You must first enroll to input grades', 'danger')
        return redirect(url_for('enroll', SSN=SSN))
    form = GradeForm()
    form.ssn.choices=students()
    form.classid.choices=classes()
    
    if form.validate_on_submit():
        inputgrade=db.engine.execute("UPDATE enrollment SET Grade = %s WHERE StudentSSN=(%s) AND ClassID=(%s)", (form.grade.data, form.ssn.data, form.classid.data))
    #	grade.StudentSSN=form.ssn.data
     #	 grade.ClassID=form.classid.data
      #	  grade.Grade=form.grade.data		
       # db.session.commit()
        flash('You have updated a student\'s grades.', 'success')
        return redirect(url_for('student'))
    elif request.method =='GET':
        form.grade.data=grade.Grade
    return render_template('highschool_grades.html', title='Assign Student Grade', form=form, legend='Assign Student Grade')
	
	
@app.route("/student/<SSN>/discipline", methods=['GET','POST'])
@login_required
def discipline(SSN):
    form = DisciplineForm()
    form.sssn.choices=students()
    form.assn.choices=administrators()   
    if form.validate_on_submit():
        discipline = Discipline(AdministratorSSN=form.assn.data, StudentSSN=form.sssn.data, Date=form.date.data, Reason_Code=form.reason.data)
        db.session.add(discipline)
        db.session.commit()
        flash('You have added a to the discipline log.', 'success')
        return redirect(url_for('student'))
    
    return render_template('highschool_discipline.html', title="New Discipline", form=form, legend = "New Discipline") 
	
	
@app.route("/staff/reportstaffabsence", methods=['GET', 'POST'])
@login_required
def report_staff_absence():
    form = AbsenceForm()
    form.ssn.choices=staffs()    
    
    if form.validate_on_submit():
        staff_absences = Absences(Staff_SSN=form.ssn.data, Date=form.date.data, Reason_Code=form.reason.data)
        db.session.add(staff_absences)
        db.session.commit()
        flash('You have logged a staff\'s absence.', 'success')
        return redirect(url_for('staff'))
    
    return render_template('highschool_staffabsence.html', title="Staff Absence", form=form, legend = "Staff Absence")     
						   


@app.route("/displays_options", methods=['GET','POST'])
@login_required
def displays_options():
    return render_template('highschool_displaysoptions.html', now=datetime.utcnow())


@app.route("/displays_options/view_classes", methods=['GET','POST'])
@login_required
def view_classes():
    classes=Student.query.join(Enrollment,Student.SSN == Enrollment.StudentSSN) \
               .add_columns(Student.LastName, Student.FirstName, Student.Grade_Level, Enrollment.Grade) \
               .join(Courses, Enrollment.ClassID == Courses.CourseID) \
               .add_columns(Courses.Course_Name) \
               .order_by(Student.Grade_Level.asc()) \
               .order_by(Student.LastName.asc())			   # This row :)
    
    return render_template('highschool_displayclasses.html', title='Classes', classes=classes, legend='Classes')

	
	
@app.route("/displays_options/display_attendance", methods=['GET','POST'])
@login_required
def display_attendance():
    attendancestudent=Student.query.join(Student_Attendance,Student.SSN == Student_Attendance.StudentSSN) \
               .add_columns(Student.LastName, Student.FirstName, Student_Attendance.Date, Student_Attendance.Attendance_Code) \
               .join(Courses, Student_Attendance.ClassID == Courses.CourseID) \
               .add_columns(Courses.Course_Name) \
               .order_by(Student.LastName.asc()) # This row :)
			   
    attendancestaff=db.engine.execute("SELECT Staff.LastName, Staff.FirstName, Absences.Date, Absences.Reason_Code FROM staff, absences WHERE staff.SSN=absences.Staff_SSN ORDER BY Staff.LastName")
    
    return render_template('highschool_displayattendance.html', title='Attendance', attendancestudent=attendancestudent, attendancestaff=attendancestaff, legend='Attendance')
	
	
@app.route("/displays_options/student_GPA", methods=['GET','POST'])
@login_required
def student_GPA():
    GPA=db.engine.execute("SELECT StudentSSN, AVG(Grade) FROM enrollment GROUP BY StudentSSN")

    for g in GPA:
        studentgrade=Student.query.get_or_404(g[0])
        if g[1] > 100:
            grades = 4.3
        elif g['AVG(Grade)'] > 93:
            grades=4.0
        elif g['AVG(Grade)'] > 90:
            grades=3.7
        elif g['AVG(Grade)'] > 87:
            grades=3.3
        elif g['AVG(Grade)'] > 83:
            grades=3.0
        elif g['AVG(Grade)'] > 80:
            grades=2.7
        elif g['AVG(Grade)'] > 77:
            grades=2.3
        elif g['AVG(Grade)'] > 73:
            grades=2.0
        elif g['AVG(Grade)'] > 70:
            grades=1.7
        elif g['AVG(Grade)'] > 67:
            grades=1.3	
        elif g['AVG(Grade)'] > 63:
            grades=1.0
        elif g['AVG(Grade)'] > 60:
            grades=0.7
        elif g['AVG(Grade)'] > 0:
            grades=0.0			
        studentgrade.GPA=grades		
        db.session.commit()
		
    regulargpa=Student.query.add_columns(Student.LastName, Student.FirstName, Student.Grade_Level, Student.GPA) \
               .filter(and_(Student.GPA <= 4, Student.GPA >= 2.0)).order_by(Student.LastName.asc()) # This row :)	
    
    flaggedgpa=db.engine.execute("SELECT LastName, FirstName, Grade_Level, GPA FROM Student WHERE GPA>4 OR GPA<=1.7 ORDER BY LastName")	
    		
    return render_template('highschool_displaygpa.html', title='Display GPA', regulargpa=regulargpa, flaggedgpa=flaggedgpa, legend='GPA Display')
 
			   
@app.route("/student/student_attendance", methods=['GET','POST'])
@login_required
def student_attendance():
    form = AttendanceForm()
    form.ssn.choices=students()
    form.classid.choices=classes()   

    if form.validate_on_submit():
        attendance = Student_Attendance(StudentSSN=form.ssn.data, ClassID=form.classid.data, Date=form.date.data, Attendance_Code=form.code.data)
        db.session.add(attendance)
        db.session.commit()
        flash('You have logged a student\'s absence.', 'success')
        return redirect(url_for('home'))
    return render_template('highschool_studentattendance.html', title="Student Absence", form=form, legend = "Student Absence")  

   
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))




@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


