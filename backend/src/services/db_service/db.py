from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url)
session = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    except:
        yield None
    finally:
        db.close()
