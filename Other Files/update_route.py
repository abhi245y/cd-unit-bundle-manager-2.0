import os
import pickle
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from database_setup import engine, College, Course

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

PROGRESS_FILE = "./progress.pkl"


def save_progress(updated_colleges):
    """Save the list of updated college codes to a file."""
    with open(PROGRESS_FILE, "wb") as f:
        pickle.dump(updated_colleges, f)


def load_progress():
    """Load the list of updated college codes from the file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "rb") as f:
            return pickle.load(f)
    return set()


def update_college_routes(old_route):
    updated_colleges = load_progress()

    try:
        # Create a new session
        session = Session()

        # Query for colleges where route is 'TBD'
        colleges_to_update = (
            session.query(College).filter(College.route == old_route).all()
        )

        if not colleges_to_update:
            print("No colleges found with route =", old_route)
            return

        total_length = len(colleges_to_update)
        # # Update each college individually
        for college in colleges_to_update:
            # if college.code in updated_colleges:
            #     print(college.name, college.route)
            #     total_length = total_length - 1
            #     continue  # Skip colleges that have been updated

            print(
                f"\nCurrent route for college {college.code} ({college.name}): {college.route}"
            )
            print(f"\n{total_length} Colleges Remaining")
            new_route = input(
                f"Enter the new route for \n {college.code} ({college.name}): "
            )
            if new_route not in [
                "Local 1",
                "Local 2",
                "MC 1",
                "MC 2",
                "NH 1",
                "NH 2",
                "TBD",
                "p",
                "pause",
            ]:
                print("\n Invalid Route, Please try again")
                new_route = input(
                    f"Enter the new route for \n {college.code} ({college.name}): "
                )
            total_length = total_length - 1
            if new_route.lower() == "pause" or new_route.lower() == "p":
                session.commit()
                save_progress(updated_colleges)
                print("Progress saved. Exiting...")
                return
            college.route = new_route
            # updated_colleges.add(college.code)

        # Commit the changes
        session.commit()
        print(f"Updated {len(updated_colleges)} colleges.")

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
        # os.remove(PROGRESS_FILE)


if __name__ == "__main__":
    # Define the old route to search for
    old_route = "TBD"

    # Update the colleges
    update_college_routes(old_route)
