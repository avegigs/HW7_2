from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Group, Teacher, Subject
from sqlalchemy import cast, Numeric

engine = create_engine('postgresql://postgres:mysecretpassword@localhost/mydb')

Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    query = (
        session.query(Student.fullname, cast(
            func.avg(Grade.grade), Numeric(10, 2)).label('avg_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(cast(func.avg(Grade.grade), Numeric(10, 2)).desc())
        .limit(5)
    )
    return query.all()


def select_2(subject_name):
    query = (
        session.query(Student.fullname, func.avg(
            Grade.grade).label('avg_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
    )
    return query.first()


def select_3(subject_name):
    query = (
        session.query(Group.name, func.avg(Grade.grade).label('avg_grade'))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .order_by(Group.name)
    )
    return query.all()


def select_4():
    query = (
        session.query(func.avg(Grade.grade).label('avg_grade'))
    )
    return query.first()


def select_5(teacher_name):
    query = (
        session.query(Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.fullname == teacher_name)
    )
    return query.all()


def select_6(group_name):
    query = (
        session.query(Student.fullname)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .all()
    )
    return [student[0] for student in query]


def select_7(group_name, subject_name):
    query = (
        session.query(Student.fullname, Grade.grade)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
    )
    return query.all()


def select_8(teacher_name):
    query = (
        session.query(func.avg(Grade.grade).label('avg_grade'))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.fullname == teacher_name)
    )
    return query.scalar()


def select_9(student_fullname):
    query = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.fullname == student_fullname)
        .group_by(Subject.name)
    )
    return query.all()


def select_10(student_fullname, teacher_fullname):
    query = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.fullname == student_fullname)
        .filter(Teacher.fullname == teacher_fullname)
        .group_by(Subject.name)
    )
    return query.all()


if __name__ == "__main__":
    results = {
        "select_1": select_1(),
        "select_2": select_2("Chemistry"),
        "select_3": select_3("Physics"),
        "select_4": select_4(),
        "select_5": select_5("Tyler Smith"),
        "select_6": select_6("Group B"),
        "select_7": select_7("Group B", "Physics"),
        "select_8": select_8("Tyler Smith"),
        "select_9": select_9("Alexis Vargas"),
        "select_10": select_10("Aaron Martin", "Tyler Smith"),
        
    }

    for query_name, result in results.items():
        with open(f"{query_name}.txt", "w") as f:
            if isinstance(result, float):
                f.write(str(result) + "\n")
            else:
                for row in result:
                    f.write(str(row) + "\n")
