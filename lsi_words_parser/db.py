from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:fn3kMls1@localhost:5432/postgres")
Session = sessionmaker(engine)
db = Session()