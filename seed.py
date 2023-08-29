from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import create_engine
import random
import datetime
from models import Base




faker = Faker()
engine = create_engine('postgresql://postgres:mysecretpassword@localhost/mydb')  

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def create_students(num_students=30):
    groups = session.query(Group).all()  
    for _ in range(num_students):
        student = Student(fullname=faker.name())
        student.group = random.choice(groups)  
        session.add(student)


def create_groups(num_groups=3):
    group_names = ['Group A', 'Group B', 'Group C']
    for name in group_names[:num_groups]:
        group = Group(name=name)
        session.add(group)

def create_teachers(num_teachers=3):
    for _ in range(num_teachers):
        teacher = Teacher(fullname=faker.name())
        session.add(teacher)

def create_subjects(num_subjects=8):
    teachers = session.query(Teacher).all()  
    subjects = ['Math', 'History', 'Physics', 'Chemistry', 'Biology', 'Literature', 'Geography', 'Music']
    for name in subjects[:num_subjects]:
        teacher = random.choice(teachers)  
        subject = Subject(name=name, teacher=teacher)
        session.add(subject)


def create_grades(num_grades=20):
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for _ in range(num_grades):
        student = random.choice(students)
        subject = random.choice(subjects)
        grade = Grade(student=student, subject=subject, grade=random.uniform(1, 10), date=faker.date_this_year())
        session.add(grade)


create_groups()
create_students()
create_teachers()
create_subjects()
create_grades()


session.commit()
