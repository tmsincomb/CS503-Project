from sqlalchemy import create_engine

# Default driver used
engine = create_engine('{dialect}://{user}:{pass}@{host}:{port}/{database}')
# Driver specific
engine = create_engine('{dialect}+{driver}://{user}:{pass}@{host}:{port}/{database}')
# PostgreSQL
engine = create_engine('postgresql://{user}:{pass}@{host}:{port}/{database}')
# MySQL
engine = create_engine('mysql://{user}:{pass}@{host}:{port}/{database}')
# MySQL versions 8+
engine = create_engine('mysql+mysqlconnector://{user}:{pass}@{host}:{port}/{database}')
