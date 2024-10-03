from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine()

# Create a declarative base
Base = declarative_base()


class CollegeDetails(Base):
    __table__ = "college_details"

    id = Column(Integer, primary_key=True)  # college code
    college_name = Column(String(255), unique=True, nullable=False)
    route = Column(String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"<CollegeDetails(id='{self.id}', college_name='{self.college_name}', route='{self.route}')>"


class Messengers(Base):
    __table__ = "messengers"

    id = Column(Integer, primary_key=True)  # generic id auto incrementing
    name = Column(String(255), nullable=False)
    post = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Messengers(id='{self.id}', name='{self.name}', post='{self.post}')>"


class Courses(Base):
    __table__ = "courses"

    id = Column(Integer, primary_key=True)
    course_name = Column(String(255), nullable=False)
    college_id
