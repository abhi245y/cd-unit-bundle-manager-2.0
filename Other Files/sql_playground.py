from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import College, engine, Messengers, OtherData, Bundle
import json
from datetime import date

# Create a configured "Session" class
engine = create_engine()

Session = sessionmaker(bind=engine)

# Create a session
session = Session()

sample_bundle_1 = Bundle(
    date_of_entry=date.today(),
    qp_series="S",
    qp_code="5076",
    college_code=(
        session.query(College)
        .filter(College.name == "Christian College Kattakada Thiruvananthapuram")
        .first()
        .code
    ),
    is_nill=False,
    messenger_name="Vinesh",
    received_date=date.today(),
    remarks="Received in good condition",
)

sample_bundle_2 = Bundle(
    date_of_entry=date.today(),
    qp_series="T",
    qp_code="5076",
    college_code=(
        session.query(College)
        .filter(College.name == "Christian College Kattakada Thiruvananthapuram")
        .first()
        .code
    ),
    is_nill=False,
    messenger_name="Vinesh",
    received_date=date.today(),
    remarks="Received in good condition",
)

session.add_all([sample_bundle_1, sample_bundle_2])

# routes = ["Local 1", "Local 2", "MC 1", "MC 2", "NH 1", "NH 2"]
# qp_series = ["P", "Q", "R", "S", "T"]

# otherdata = OtherData(routes=routes, qp_series=qp_series)

# session.add(otherdata)
# colleges = (
#     session.query(College)
#     .filter(College.route == "Local 1")
#     .filter(College.college_type == "Engineering")
#     .all()
# )
#


# messengers = session.query(Messengers).all()

# # Print the colleges
# for college in colleges:
#     print(college.name)

# for messenger in messengers:
#     print(messenger.name)


# # Query to get the colleges where name Like 'dept%'
# query = session.query(College).filter(College.name.like("dep%"))

# # Update the college_type for the results produced by the query
# for college in query:
#     college.college_type = "DEPARTMENT"

# List of messengers to be inserted


# Add all messengers to the session
# session.add_all(messengers)

# Commit the changes
session.commit()

# Close the session
session.close()
