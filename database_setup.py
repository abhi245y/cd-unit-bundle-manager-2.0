from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Table,
    ForeignKey,
    Enum,
    JSON,
    Boolean,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import yaml
import os
import sys


def get_config_directory():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


config_directory = get_config_directory()
config_file_path = os.path.join(config_directory, "config.yaml")

if not os.path.exists(config_file_path):
    default_config = {
        "db_username": "root",
        "db_pass": "password",
        "db_link": "localhost:3306",
        "db_name": "database",
        "GROQ_API_KEY": "API_KEY",
    }
    with open(config_file_path, "w") as file:
        yaml.dump(default_config, file, indent=4)
    print(f"Created new config file at: {config_file_path}")
    print(
        "Please edit this file with your actual configuration before running the application again."
    )
    sys.exit(0)

with open(config_file_path, "r") as file:
    configurations = yaml.safe_load(file)

print(f"Config file path: {config_file_path}")
print(f"Configurations: {configurations}")

db_string = f"mysql://{configurations['db_username']}:{configurations['db_pass']}@{configurations['db_link']}/{configurations['db_name']}"
engine = create_engine(db_string)

Base = declarative_base()


class CollegeType(enum.Enum):
    ARTS_AND_SCIENCE = "Art and Science"
    TRAINING = "Training"
    ENGINEERING = "Engineering"
    MUSIC = "Music"
    MANAGEMENT = "Management"
    LAW = "Law"
    DEPARTMENT = "Department"
    OTHER = "Others"


# Association table for the many-to-many relationship between Courses and Colleges
course_college_association = Table(
    "course_college",
    Base.metadata,
    Column("course_code", Integer, ForeignKey("courses.code")),
    Column("college_code", Integer, ForeignKey("colleges.code")),
)


class College(Base):
    __tablename__ = "colleges"
    code = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    route = Column(String(10), nullable=True)
    college_type = Column(Enum(CollegeType), nullable=True)
    courses = relationship(
        "Course", secondary=course_college_association, back_populates="colleges"
    )
    bundles = relationship("Bundle", back_populates="college")

    def __repr__(self):
        return (
            f"<College(code='{self.code}', name='{self.name}', route='{self.route}')>"
        )


class Course(Base):
    __tablename__ = "courses"
    code = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    colleges = relationship(
        "College", secondary=course_college_association, back_populates="courses"
    )

    def __repr__(self):
        return f"<Course(code='{self.code}', name='{self.name}')>"


class Messengers(Base):
    __tablename__ = "messengers"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    post = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Messengers(id='{self.id}', name='{self.name}', post='{self.post}')>"


class OtherData(Base):
    __tablename__ = "otherdata"
    id = Column(Integer, primary_key=True)
    routes = Column(JSON)
    qp_series = Column(JSON)

    def __repr__(self):
        return f"<OtherData(routes='{self.routes}', qp_series='{self.qp_series}')>"


class Bundle(Base):
    __tablename__ = "bundles"

    id = Column(String(42), nullable=False, primary_key=True)
    date_of_entry = Column(Date, nullable=False)
    qp_series = Column(String(1), nullable=False)
    qp_code = Column(String(100), nullable=False)
    college_code = Column(Integer, ForeignKey("colleges.code"), nullable=False)
    is_nill = Column(Boolean, default=False, nullable=False)
    messenger_name = Column(String(255), nullable=False)
    received_date = Column(Date, nullable=False)
    remarks = Column(String(255), default="")

    college = relationship("College", back_populates="bundles")

    def __repr__(self):
        return (
            f"<Bundle(id='{self.id}', date_of_entry='{self.date_of_entry}', "
            f"qp_code='{self.qp_code}', college_code='{self.college_code}', "
            f"messenger_name='{self.messenger_name}', is_nill='{self.is_nill}, ')"
            f"messenger_name='{self.messenger_name}, received_date='{self.received_date}, remarks='{self.remarks}'>"
        )


# Create the tables in the database
Base.metadata.create_all(engine)
