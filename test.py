from flask import Flask
from sqlalchemy import create_engine, inspect, Table, Column
import pandas as pd

db_url = 'mysql+mysqlconnector://root:water@localhost/CS503'
engine = create_engine(db_url)
conn = engine.connect()
inspector = inspect(engine)

# Get table information
for tablename in inspector.get_table_names():
    # df = pd.DataFrame(inspector.get_columns(tablename))
    # print(list(df.name))
    print('tablename')
    columns = inspector.get_columns(tablename)
    for column in columns:
        print(column['name'], column['type'])
