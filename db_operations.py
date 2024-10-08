from sqlalchemy.orm import sessionmaker
from database_setup import engine, College, Messengers, OtherData, Bundle
from datetime import date
from sqlalchemy import and_, or_
from sqlalchemy.dialects import mysql
from sqlalchemy import text
from pprint import pprint
import ai_search
# import logging

# # Set up logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class DbOps:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def getCollegesByRoute(self, route_name):
        colleges = self.session.query(College).filter(College.route == route_name).filter(College.college_type!="DEPARTMENT").order_by(College.name.asc()).all()
        return colleges

    def getCollegeNameByCode(self, code):
        colleges = self.session.query(College).filter(College.code == code).first()
        return colleges

    def getCollegeByName(self, name):
        college = self.session.query(College).filter(College.name == name).first()
        return college

    def isBundlePresent(self, query):
        # pprint(query, self.getCollegeByName(query["collegeName"]).code)
        bundle_count = (
            self.session.query(Bundle)
            .filter(Bundle.qp_series == query["qpSeries"])
            .filter(Bundle.qp_code == query["qpCode"])
            .filter(Bundle.is_nill == query["isNil"])
            .filter(Bundle.received_date == query["receivedDate"])
            .filter(Bundle.messenger_name == query["messenger"])
            .filter(
                Bundle.college_code == self.getCollegeByName(query["collegeName"]).code
            )
            .count()
        )
        # pprint(bundle_count)
        # return False
        if bundle_count == 0 or bundle_count is None:
            return False
        else:
            return True

    def saveBundlesToDb(self, finalData):
        # pprint(finalData)
        for data in finalData:
            self.session.add(
                Bundle(
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
            )
        self.session.commit()
        return True, ""

    # try:

    # except Exception as e:
    #     pprint(f"Error In Saving Data {e}")
    #     return False, e

    def getMessengers(self):
        messengers = self.session.query(Messengers).all()
        return messengers

    def getOtherData(self):
        otherDatas = self.session.query(OtherData).all()
        return otherDatas

    def searchBundles(self, entryDate, received_date, received_date_check,
        date_of_entry_check):

        if received_date_check and date_of_entry_check:
            return(self.session.query(Bundle).filter(and_(Bundle.received_date == received_date,
                Bundle.date_of_entry == entryDate)))
        elif received_date_check:
            return (self.session.query(Bundle).filter(Bundle.received_date == received_date))
        elif date_of_entry_check:
            return (self.session.query(Bundle).filter(Bundle.date_of_entry == entryDate))

    def adv_search(
        self,
        messenger=None,
        qp_code_input=None,
        college_code=None,
        date_of_entry=None,
        received_date=None,
        received_date_check=False,
        date_of_entry_check=False
    ):
        """
        Perform an advanced search on the Bundle table based on various filters.

        :param session: SQLAlchemy session to query the database
        :param messenger: Name of the messenger (optional)
        :param qp_code_input: String input of qp_code (e.g., 'T 5467') (optional)
        :param college_code: Integer college code (optional)
        :param date_of_entry: Date when the entry was made (optional)
        :param received_date: Date the bundle was received (optional)
        :return: List of matching Bundle objects
        """

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

        query = self.session.query(Bundle)

        query = query.filter(or_(*conditions)).order_by(Bundle.id.asc())

        # Get the query statement
        statement = query.statement
        # Compile the statement into SQL, including parameters
        sql = statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})

        sql_string = str(sql)

        # Print the SQL query and parameters
        pprint("SQL Query:")
        pprint(sql_string)


        res = query.all()
        # pprint(res)
        return res

    def save_changes_to_db(self, new_data):
        """
        Save only the changed rows to the MySQL database.
        """
        for bundle_id, changes in new_data.items():
            bundle = self.session.query(Bundle).filter(Bundle.id == bundle_id).first()

            if bundle:
                for column, new_value in changes.items():
                    if column == 0:  # received_date
                        bundle.received_date = new_value
                    elif column == 1:  # qp_series
                        bundle.qp_series = new_value
                    elif column == 2:  # qp_code
                        bundle.qp_code = new_value
                    elif column == 3:  # is_nill (Boolean)
                        bundle.is_nill = bool(new_value)
                    elif column == 4:  # date_of_entry
                        bundle.date_of_entry = new_value
                    elif column == 5:  # messenger_name
                        bundle.messenger_name = new_value
                    elif column == 6:  # college_name (convert to college_code)
                        college = self.getCollegeByName(name=new_value).code
                        if college:
                            bundle.college_code = college.code
                    elif column == 7:  # remarks
                        bundle.remarks = new_value

                self.session.commit()

    def delete_bundle(self, bundle_id):
        if bundle_id:
            self.session.query(Bundle).filter(Bundle.id == bundle_id).delete()
            self.session.commit()

    def execute_custom(self, user_query):
        try:
            query = ai_search.generate_sql_query(user_input=user_query)
            return self.session.query(Bundle).from_statement(text(query)).all()
        except Exception as e:
            return None
