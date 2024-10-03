import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database_setup import engine, College, Course


# Create a session
Session = sessionmaker(bind=engine)
session = Session()
def add_colleges_from_json(file_path):
    with open(file_path, 'r') as file:
        colleges_data = json.load(file)['colleges']

    for college_data in colleges_data:
        college = College(code=college_data['code'], name=college_data['name'], route='TBD')

        for course_data in college_data['courses']:
            course = session.query(Course).filter_by(code=course_data['code']).first()
            if not course:
                course = Course(code=course_data['code'], name=course_data['name'])
            college.courses.append(course)

        session.add(college)

    session.commit()

def add_courses_from_json(file_path):
    with open(file_path, 'r') as file:
        courses_data = json.load(file)['courses']

    for course_data in courses_data:
        course = session.query(Course).filter_by(code=course_data['code']).first()
        if not course:
            course = Course(code=course_data['code'], name=course_data['name'])

        for college_data in course_data['college']:
            college = session.query(College).filter_by(code=college_data['code']).first()
            if not college:
                college = College(code=college_data['code'], name=college_data['name'])
            course.colleges.append(college)

        session.add(course)

    session.commit()
# Add data from JSON files
add_colleges_from_json('college_data_cleaned_list.json')
add_courses_from_json('all_courses_cleaned_list.json')

# Close the session
session.close()

print("Database populated successfully!")
