from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PG_LOGIN = ''
PG_PASSWORD = ''
PG_PORT = ''
PG_HOST = ''
DB_NAME = ''

engine = create_engine(f"postgresql://{PG_LOGIN}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}")
Session = sessionmaker(engine)
db = Session()