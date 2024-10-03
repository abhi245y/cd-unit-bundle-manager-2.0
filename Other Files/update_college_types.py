from sqlalchemy.orm import sessionmaker
from database_setup import College, CollegeType, engine
import json

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def update_college_types(college_types_dict):
    for college_type, college_codes in college_types_dict.items():
        for code in college_codes:
            college = session.query(College).filter_by(code=code).first()
            if college:
                college.college_type = CollegeType[
                    college_type.upper().replace(" ", "_")
                ]
            else:
                print(f"College with code {code} not found")

    session.commit()
    print("College types updated successfully")


# Example usage
college_types = {
    "Arts and Science": [],  # replace with actual college codes
    "Training": [],
    "Engineering": [],
    "Music": [],
    "Management": [],
    "Law": [],
}


def populate_college_types(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    college_type = data["college_type"]
    colleges = data["colleges"]

    for college in colleges:
        code = college["code"]
        college_types_to_add = college_types[college_type]
        college_types_to_add.append(code)


populate_college_types("College_Data/Arts.json")
populate_college_types("College_Data/Management.json")
populate_college_types("College_Data/Engineering.json")
populate_college_types("College_Data/Music.json")
populate_college_types("College_Data/Law.json")
populate_college_types("College_Data/Training.json")
print(college_types)

input("Proceed to Updating")
update_college_types(college_types)

# Don't forget to close the session when you're done
session.close()
