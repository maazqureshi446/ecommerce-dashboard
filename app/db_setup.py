import os

from app.add_dummy_data import add_dummy_data
from models import Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
print(DATABASE_URL)

engine = create_engine(f"{DATABASE_URL}", pool_pre_ping=True)

if not database_exists(engine.url):
    print('Creating Database...')
    create_database(engine.url)

    print('Creating Tables...')
    Base.metadata.create_all(bind=engine)

    print('Adding Database...')
    add_dummy_data()

else:
    print('Dropping Existing Database...')
    drop_database(engine.url)

    print('Creating Database...')
    create_database(engine.url)

    print('Creating Tables...')
    Base.metadata.create_all(bind=engine)

    print('Adding Database...')
    add_dummy_data()

