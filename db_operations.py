from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from database_setup import engine, Course,course_college_association, College, Messengers, OtherData, Bundle
from datetime import date
from sqlalchemy import and_, or_
from sqlalchemy.dialects import mysql
from sqlalchemy import text
from pprint import pprint
import ai_search

class DbOps:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.close_session()

    def close_session(self):
        if self.session:
            self.session.close()

    def db_operation(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.session.commit()
                return result
            except SQLAlchemyError as e:
                self.session.rollback()
                print(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper

    @db_operation
    def getCollegesByRoute(self, route_name):
        return self.session.query(College).filter(College.route == route_name).filter(College.college_type != "DEPARTMENT").order_by(College.name.asc()).all()

    @db_operation
    def getCollegeNameByCode(self, code):
        return self.session.query(College).filter(College.code == code).first()

    @db_operation
    def getCollegeByName(self, name):
        return self.session.query(College).filter(College.name == name).first()

    @db_operation
    def getAllColleges(self):
        return self.session.query(College).order_by(College.name.asc(), College.college_type.asc(), College.route.asc()).all()

    @db_operation
    def getCoursesByCollegeCode(self, college_code):
        return self.session.query(Course).join(course_college_association).filter(
                course_college_association.c.college_code == college_code
            ).order_by(Course.name.asc()).all()

    @db_operation
    def getAllCourses(self):
        return self.session.query(Course).order_by(Course.name.asc()).all()

    @db_operation
    def isBundlePresent(self, query):
        bundle_count = (
            self.session.query(Bundle)
            .filter(Bundle.qp_series == query["qpSeries"])
            .filter(Bundle.qp_code == query["qpCode"])
            .filter(Bundle.is_nill == query["isNil"])
            .filter(Bundle.received_date == query["receivedDate"])
            .filter(Bundle.messenger_name == query["messenger"])
            .filter(Bundle.college_code == self.getCollegeByName(query["collegeName"]).code)
            .count()
        )
        return bundle_count > 0

    @db_operation
    def saveBundlesToDb(self, finalData):
        success_count = 0
        error_messages = []

        for data in finalData:
            try:
                new_bundle = Bundle(
                    id=data['id'],
                    date_of_entry=date.today(),
                    qp_series=data["qpSeries"],
                    qp_code=data["qpCode"],
                    college_code=(self.getCollegeByName(data["collegeName"]).code),
                    is_nill=data["isNil"],
                    messenger_name=data["messenger"],
                    received_date=data["receivedDate"],
                    remarks=data["remarks"],
                )
                self.session.add(new_bundle)
                self.session.flush()
                success_count += 1
            except SQLAlchemyError as e:
                error_message = f"Error saving bundle (ID: {data['id']}): {str(e)}"
                error_messages.append(error_message)
                print(error_message)

        if success_count == len(finalData):
            return True, "All bundles saved successfully."
        elif success_count > 0:
            return True, f"Saved {success_count} out of {len(finalData)} bundles. Errors: {'; '.join(error_messages)}"
        else:
            return False, f"Failed to save any bundles. Errors: {'; '.join(error_messages)}"

    @db_operation
    def getMessengers(self):
        return self.session.query(Messengers).options(selectinload('*')).all()

    @db_operation
    def getOtherData(self):
        return self.session.query(OtherData).all()

    @db_operation
    def serachColleges(self, include_course,include_college_type,include_route,
        selected_course,selected_college_type,selected_route):

        conditions = []
        if include_college_type:
            conditions.append(and_(College.college_type == selected_college_type.name))

        if include_route:
            conditions.append(and_(College.route == selected_route))

        query = self.session.query(College).filter(and_(*conditions)).order_by(College.name.asc(), College.college_type.asc())
        statement = query.statement
        sql = statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
        pprint(f"SQL Query: {str(sql)}")
        return query.all()

    @db_operation
    def searchBundles(self, entryDate, received_date, received_date_check, date_of_entry_check):
        query = self.session.query(Bundle)
        if received_date_check and date_of_entry_check:
            query = query.filter(and_(Bundle.received_date == received_date, Bundle.date_of_entry == entryDate))
        elif received_date_check:
            query = query.filter(Bundle.received_date == received_date)
        elif date_of_entry_check:
            query = query.filter(Bundle.date_of_entry == entryDate)
        return query.all()

    @db_operation
    def adv_search(self, messenger=None, qp_code_input=None, college_code=None, date_of_entry=None, received_date=None, received_date_check=False, date_of_entry_check=False):
        conditions = []

        if messenger:
            conditions.append(Bundle.messenger_name == messenger)

        if qp_code_input:
            try:
                qp_series, qp_code = qp_code_input.split(" ", 1)
                conditions.append(and_(Bundle.qp_series == qp_series, Bundle.qp_code == qp_code))
            except ValueError:
                raise ValueError("QP Code input must be in the format 'Series Code' (e.g., 'T 5467').")

        if college_code:
            conditions.append(Bundle.college_code == college_code)

        if received_date_check and date_of_entry_check:
            conditions.append(and_(Bundle.received_date == received_date, Bundle.date_of_entry == date_of_entry))
        elif received_date_check:
            conditions.append(Bundle.received_date == received_date)
        elif date_of_entry_check:
            conditions.append(Bundle.date_of_entry == date_of_entry)

        if not conditions:
            raise ValueError("At least one filter must be provided.")

        query = self.session.query(Bundle).filter(or_(*conditions)).order_by(Bundle.id.asc())

        statement = query.statement
        sql = statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
        pprint(f"SQL Query: {str(sql)}")

        return query.all()

    @db_operation
    def save_changes_to_db(self, new_data):
        for bundle_id, changes in new_data.items():
            bundle = self.session.query(Bundle).filter(Bundle.id == bundle_id).first()
            if bundle:
                for column, new_value in changes.items():
                    if column == 0:
                        bundle.received_date = new_value
                    elif column == 1:
                        bundle.qp_series = new_value
                    elif column == 2:
                        bundle.qp_code = new_value
                    elif column == 3:
                        bundle.is_nill = bool(new_value)
                    elif column == 4:
                        bundle.date_of_entry = new_value
                    elif column == 5:
                        bundle.messenger_name = new_value
                    elif column == 6:
                        college = self.getCollegeByName(name=new_value)
                        if college:
                            bundle.college_code = college.code
                    elif column == 7:
                        bundle.remarks = new_value

    @db_operation
    def delete_bundle(self, bundle_id):
        if bundle_id:
            self.session.query(Bundle).filter(Bundle.id == bundle_id).delete()

    @db_operation
    def execute_custom(self, user_query):
        try:
            query = ai_search.generate_sql_query(user_input=user_query)
            return self.session.query(Bundle).from_statement(text(query)).all()
        except Exception as e:
            print(f"Error in execute_custom: {str(e)}")
            return None

    def close(self):
        self.close_session()
