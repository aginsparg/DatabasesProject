from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp, InputRequired, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Student, Classroom, Staff, Courses, Administrator, Teacher, Student_Attendance, Absences, Discipline, Emergency_Contact, Staff_Emergencycontact, Enrollment, Student_Emergencycontact
from wtforms.fields.html5 import DateField



Position = [(1, "administrator"),(2, "teacher"), (3, "librarian"),(4, "custodian"),(5, "office staff"),(6, "security team")]
Grade = [(9, "9th Grade"),(10, "10th Grade"),(11, "11th Grade"),(12, "12th Grade")]
discipline_reasons = [(1, "Disrespect to teacher"),(2, "Uniform Violation"),(3, "Consistant Tardiness"),(4, "Chronic Absences"),(5, "Other")]
absence_reasons = [(1,"Bar/Bas Mitzvah"),(2,"Wedding"),(3,"Other Simcha"),(4,"Sick"),(5,"Child Related"),(6, "Out of Town"),(7, "Personal")]
attendance_code = [(1, "Tardy Excused"),(2, "Tardy Unexcused"),(3, "Absent Excused"),(4, "Absent Unexcused"),(5, "Cut Class")]


classroom = Classroom.query.with_entities(Classroom.Room_Number) 
mychoices=[(row[0], row[0]) for row in classroom]
results=list()
for row in classroom:
    rowDict=row._asdict()
    results.append(rowDict)
classroomChoices = [(row['Room_Number'],row['Room_Number']) for row in results]

teacher=Staff.query.filter(Staff.Person_Type ==2).add_columns(Staff.SSN, Staff.LastName)
myChoices2 = [(row[0],row[1]) for row in teacher]  # change
results=list()			 
for row in teacher:
    rowDict=row._asdict()
    results.append(rowDict)
teacherChoices = [(row['SSN'],row['LastName']) for row in results]



student=Student.query.with_entities(Student.SSN, Student.LastName)
myChoices3 = [(row[0],row[1]) for row in student]  # change
results=list()			 
for row in student:
    rowDict=row._asdict()
    results.append(rowDict)
students = [(row['SSN'], row['LastName']) for row in results]




classs=Courses.query.with_entities(Courses.CourseID, Courses.Course_Name)
myChoices4 = [(row[0],row[1]) for row in classs]  # change
results=list()			 
for row in classs:
    rowDict=row._asdict()
    results.append(rowDict)
classes = [(row['CourseID'], row['Course_Name']) for row in results]


administrator=Staff.query.with_entities(Staff.SSN, Staff.LastName).filter(Staff.Person_Type==1)
myChoices6 = [(row[0],row[1]) for row in administrator]  # change
results=list()			 
for row in administrator:
    rowDict=row._asdict()
    results.append(rowDict)
administrators = [(row['SSN'], row['LastName']) for row in results]


staff=Staff.query.with_entities(Staff.SSN, Staff.LastName)
myChoices7 = [(row[0],row[1]) for row in staff]  # change
results=list()			 
for row in staff:
    rowDict=row._asdict()
    results.append(rowDict)
staffs = [(row['SSN'], row['LastName']) for row in results]







class NewStudentForm(FlaskForm):
    ssn= IntegerField("Student SSN", validators=[DataRequired(), NumberRange(max=999999999)])
    lname=StringField("Last Name", validators=[DataRequired()])
    fname=StringField("First Name", validators=[DataRequired()])
    address=StringField("Address", validators=[DataRequired()])
    city=StringField("City", validators=[DataRequired()])
    state=StringField("State Initials", validators=[DataRequired(), Length(max=2)])
    zip=IntegerField("Zip Code", validators=[DataRequired()])
    phone=StringField("Home Phone Number", validators=[DataRequired(), Length(max=11)])
    grade=SelectField("Grade Level", coerce=int, choices=Grade, validators=[DataRequired()])
    submit=SubmitField('Add New Student')	
    
    
    def validate_ssn(self, NewStudentForm):
        exists = db.session.query(Student).filter_by(SSN=self.ssn.data).scalar() is not None	#sqlalchemy
		
        if exists:
            raise ValidationError('That SSN already exists. Please double check that you inputted the numbers correctly.')	

			
			
class UpdateStudentForm(FlaskForm):
    ssn= HiddenField("")
    lname=StringField("Last Name", validators=[DataRequired()])
    fname=StringField("First Name", validators=[DataRequired()])
    address=StringField("Address", validators=[DataRequired()])
    city=StringField("City", validators=[DataRequired()])
    state=StringField("State Initials", validators=[DataRequired(), Length(max=2)])
    zip=IntegerField("Zip Code", validators=[DataRequired()])
    phone=StringField("Home Phone Number", validators=[DataRequired()])
    grade=SelectField("Grade Level", coerce=int, choices=Grade, validators=[DataRequired()])
    submit=SubmitField('Update Student')	


class NewStaffForm(FlaskForm):
    ssn= IntegerField("Staff SSN", validators=[DataRequired(), NumberRange(max=999999999)])
    lname=StringField("Last Name", validators=[DataRequired()])
    fname=StringField("First Name", validators=[DataRequired()])
    address=StringField("Address", validators=[DataRequired()])
    city=StringField("City", validators=[DataRequired()])
    state=StringField("State Initials", validators=[DataRequired(), Length(max=2)])
    zip=IntegerField("Zip Code", validators=[DataRequired()])
    phone=StringField("Home Phone Number", validators=[DataRequired(), Length(max=11)])
    type=SelectField("Position in School", coerce=int, choices=Position)
    salary=DecimalField("Salary", places=2, rounding=None, validators=[DataRequired(), NumberRange(max=999999)])
    submit=SubmitField('Add New Staff Member')	
    
    def validate_ssn(self, NewStaffForm):
        exists = Staff.query.get(self.ssn.data)
        if exists:
            raise ValidationError('That SSN already exists. Please double check that you inputted the numbers correctly.')			

class NewAdministratorForm(FlaskForm):
    office=IntegerField("Office Number", validators=[DataRequired(), NumberRange(min=100, max=9999)])
    degree=StringField("Degree", validators=[DataRequired()])
    submit=SubmitField('Add New Administrator')

	
class NewTeacherForm(FlaskForm):
    certification= StringField("Teaching Certification", validators=[DataRequired()])
    submit=SubmitField('Add New Teacher')
			
			
class NewContactForm(FlaskForm):
    ssn=HiddenField("")		
    contactID=IntegerField("Contact ID", validators=[DataRequired(), NumberRange(max=999999999)])
    lname=StringField("Last Name", validators=[DataRequired()])
    fname=StringField("First Name", validators=[DataRequired()])
    address=StringField("Address", validators=[DataRequired()])
    city=StringField("City", validators=[DataRequired()])
    state=StringField("State Initials", validators=[DataRequired(), Length(max=2)])
    zip=IntegerField("Zip Code", validators=[DataRequired()])
    phone=StringField("Home Phone Number", validators=[DataRequired(), Length(max=11)])
    submit=SubmitField('Add New Emergency Contact')
	
    def validate_contactID(self, NewContactForm):
        existsstudent= db.engine.execute("SELECT * FROM Student_Emergencycontact Where ContactID=(%s) AND SSN in(SELECT SSN From Student Where SSN=(%s))", (self.contactID.data, self.ssn.data))
        existsstaff= db.engine.execute("SELECT * FROM Staff_Emergencycontact Where ContactID=(%s) AND SSN in(SELECT SSN From Staff Where SSN=(%s))", (self.contactID.data, self.ssn.data))
			
        if any(existsstudent):
            raise ValidationError('That combination already exists. Please check that all your information is accurate.')	
        if any(existsstaff):
            raise ValidationError('That combination already exists. Please check that all your information is accurate.')	

class UpdateStaffForm(FlaskForm):
    ssn= HiddenField("")
    lname=StringField("Last Name", validators=[DataRequired()])
    fname=StringField("First Name", validators=[DataRequired()])
    address=StringField("Address", validators=[DataRequired()])
    city=StringField("City", validators=[DataRequired()])
    state=StringField("State Initials", validators=[DataRequired(), Length(max=2)])
    zip=IntegerField("Zip Code", validators=[DataRequired()])
    phone=StringField("Home Phone Number", validators=[DataRequired(), Length(max=11)])
    type=HiddenField("")
    salary=DecimalField("Salary", places=2, rounding=None, validators=[DataRequired()])
    submit=SubmitField('Update Staff')		
	
	
class UpdateAdministratorForm(FlaskForm):
    office=IntegerField("Office Number", validators=[DataRequired(), NumberRange(min=100, max=9999)])
    submit=SubmitField('Update  ')
    
			
class NewCourseForm(FlaskForm):
    course=IntegerField("Course ID", validators=[DataRequired(), NumberRange(min=10000, max=99999)])
    cname=StringField("Course Name", validators=[DataRequired()])
    grade=SelectField("Grade Level", coerce=int, choices=Grade, validators=[DataRequired()])
    teacher=SelectField("Teacher", coerce=int, choices= teacherChoices, validators=[DataRequired()])
    classroom=SelectField("Classroom Room Number", coerce=int, choices=classroomChoices, validators=[DataRequired()])
    submit=SubmitField("Add Course")
	
    def validate_course(self, NewCourseForm):
        exists = Courses.query.filter_by(CourseID=self.course.data).scalar() is not None
		
        if exists:
            raise ValidationError('That Course ID already exists. Please type in a different one.')
		
			
class EnrollForm(FlaskForm):
    ssn=SelectField("Student", coerce=int, choices=students, validators=[DataRequired()])		
    classid=SelectField("Course", coerce=int, choices=classes, validators=[DataRequired()])
    submit=SubmitField("Add Student to Class")
	
    def validate_ssn(self, EnrollForm):
        exists = Enrollment.query.filter_by(StudentSSN=self.ssn.data, ClassID=self.classid.data).with_entities(Enrollment.StudentSSN)	
        if any(exists):
            raise ValidationError('That student is already enrolled in that class. Please choose a different class, or a different student.')
    
    def validate_classid(self, EnrollForm):
        studentgrade = Student.query.filter_by(SSN=self.ssn.data).with_entities(Student.Grade_Level)	
        classgrade=Courses.query.filter_by(CourseID=self.classid.data).with_entities(Courses.Grade_Level)
        if studentgrade[0]!= classgrade[0]:
             raise ValidationError('That student is not in the appropriate grade for that class. Please choose a different class, or a different student.')
			
class GradeForm(FlaskForm):
    ssn=SelectField("Student", coerce=int, choices=students, validators=[DataRequired()])
    classid=SelectField("Course", coerce=int, choices=classes, validators=[DataRequired()])
    grade=DecimalField("Student's Grade", validators=[DataRequired(), NumberRange(min=0, max=150)])
    submit=SubmitField("Add Grade")
	
    def validate_ssn(self, GradeForm):
        notexists = Enrollment.query.filter_by(StudentSSN=self.ssn.data, ClassID=self.classid.data).scalar() is None	
		
        if notexists:
            raise ValidationError('That student is not in that class. Either enroll the student first or choose a different class, or a different student.')

	
class DisciplineForm(FlaskForm):
    assn=SelectField("Administrator", coerce=int, choices=administrators, validators=[DataRequired()])
    sssn=SelectField("Student", coerce=int, choices=students, validators=[DataRequired()])
    date=DateField("Date of Discipline", format='%Y-%m-%d', validators=[DataRequired()])
    reason=SelectField("Reason", coerce=int, choices=discipline_reasons, validators=[DataRequired()])
    submit=SubmitField("Add Discipline Log")   	
    
    def validate_ssn(self, DisciplineForm):
        exists = Discipline.query.filter_by(AdministratorSSN=self.assn.data, StudentSSN=self.sssn.data, Date=self.date.data).scalar() is not None	
		
        if exists:
            raise ValidationError('That combination already exists. Please check that all your information is accurate.')
	
		
class AbsenceForm(FlaskForm):	
    ssn=SelectField("Staff", coerce=int, choices=staffs, validators=[DataRequired()])
    date=DateField("Date of Absence", format='%Y-%m-%d', validators=[DataRequired()])
    reason=SelectField("Reason", coerce=int, choices=absence_reasons, validators=[DataRequired()])
    submit=SubmitField("Add Absence")
	
    def validate_ssn(self, AbsenceForm):
        exists = Absences.query.filter_by(Staff_SSN=self.ssn.data, Date=self.date.data).scalar() is not None	
		
        if exists:
            raise ValidationError('That combination already exists. Please check that all your information is accurate.')



class AttendanceForm(FlaskForm):
    ssn=SelectField("Student", coerce=int, choices=students, validators=[DataRequired()])
    classid=SelectField("Class", coerce=int, choices=classes, validators=[DataRequired()])
    date=DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    code=SelectField("Reason", coerce=int, choices=attendance_code, validators=[DataRequired()])
    submit=SubmitField("Add Student Attendance")
	
    def validate_ssn(self, AttendanceForm):
        exists = Student_Attendance.query.filter_by(StudentSSN=self.ssn.data, ClassID=self.classid.data, Date=self.date.data).scalar() is not None	
		
        if exists:
            raise ValidationError('That combination already exists. Please check that all your information is accurate.')
			
    def validate_ssn(self, AttendanceForm):
        notexists = Enrollment.query.filter_by(StudentSSN=self.ssn.data, ClassID=self.classid.data).scalar() is None	
		
        if notexists:
            raise ValidationError('That student is not in that class. Either enroll the student first or choose a different class, or a different student.')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')