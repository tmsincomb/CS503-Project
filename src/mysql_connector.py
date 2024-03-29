from flask_table import Table, Col
from sqlalchemy import create_engine, inspect, Table, Column, exc
from collections import defaultdict
import pandas as pd

class MysqlConnector:

    def __init__(self, app, db_url=None):
        if not db_url:
            db_url = 'mysql+mysqlconnector://root:water@localhost/SAureus'
        self.engine = create_engine(db_url)

    def get(self, query: str) -> pd.DataFrame:
        try:
            df = pd.read_sql(query, self.engine)
            return 1, df
        except exc.SQLAlchemyError as e:
            return 0, e

    def post(self, command: str) -> pd.DataFrame:
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            resp = connection.execute(command)
            trans.commit()
            connection.close()
            return 1, resp
        except exc.SQLAlchemyError as e:
            # print(exc.SQLAlchemyError)
            trans.rollback()
            connection.close()
            return 0, e

    def descibe_database(self):
        inspector = inspect(self.engine)
        database = []
        for tablename in inspector.get_table_names():
            table = pd.DataFrame(inspector.get_columns(tablename))
            database.append((tablename, table))
        return database

    def get_table(self, tablename):
        inspector = inspect(self.engine)
        return pd.DataFrame(inspector.get_columns(tablename))

    def update_table(self, table, tablename):
        resp = table.to_sql(tablename, self.engine, if_exists="replace")
        return resp
