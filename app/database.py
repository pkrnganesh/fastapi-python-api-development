from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Construct the database URL using settings from a configuration file
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative models
Base = declarative_base()

# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:   
  
#      try:
#         conn = psycopg2.connect(host = '',database = 'fastapi',user='',password='',cursor_factory=RealDictCursor)   # here we have column also while retreiving the  data so in order get it we need to import a pacakage realdictcursor
#         cursor = conn.cursor()
#         print("database connection was succesfull!")
#         break
#      except Exception as error :
#         print("connection to database is failed")
#         print("Error: ",error)
#         time.sleep(2)