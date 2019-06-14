from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Staff(db.Model):
    __table__ = db.Model.metadata.tables['staff']
    
class Administrator(db.Model):
    __table__ = db.Model.metadata.tables['administrator']

class Teacher(db.Model):
    __table__ = db.Model.metadata.tables['teacher']
    
class Absences(db.Model):
    __table__ = db.Model.metadata.tables['absences']
	
class Classroom(db.Model):
    __table__ = db.Model.metadata.tables['classroom']
	
class Courses(db.Model):
    __table__ = db.Model.metadata.tables['courses']
	
class Discipline(db.Model):
    __table__ = db.Model.metadata.tables['discipline']
	
class Enrollment(db.Model):
    __table__ = db.Model.metadata.tables['enrollment']

class Student(db.Model):
    __table__ = db.Model.metadata.tables['student']
	
class Student_Attendance(db.Model):
    __table__ = db.Model.metadata.tables['student_attendance']

class Emergency_Contact(db.Model):
    __table__ = db.Model.metadata.tables['emergency_contact']

class Staff_Emergencycontact(db.Model):
    __table__ = db.Model.metadata.tables['staff_emergencycontact']

class Student_Emergencycontact(db.Model):
    __table__ = db.Model.metadata.tables['student_emergencycontact']	