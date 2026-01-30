import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

password = os.getenv("MYSQL_ROOT_PASSWORD", "root123")

DATABASE_URL = f"mysql+pymysql://root:{password}@mysql/temp"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
