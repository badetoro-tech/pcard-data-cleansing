import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

# MSSQL Database conn string
engine_string = f'mssql+pyodbc://{config.DATABASE_SERVER}/{config.DATABASE_NAME}?driver=SQL+Server+Native+Client+11.0'
engine = create_engine(engine_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
