# from fastapi.testclient import TestClient
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from app.main import app
# from app import schemas,models
# from app.config import settings
# from app.database import get_db
# from app.database import Base
# from alembic import command

# # creating a separate db for testing 
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:passowrd123@localhost:5432/fastapi_test'
# # # Construct the database URL using settings from a configuration file
# # SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# # Create the SQLAlchemy engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # Create a session factory
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# models.Base.metadata.create_all(bind = engine)
# # Define a base class for declarative models
# Base = declarative_base()

# Define a function to get a database session

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from alembic import command


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    #print("my session fixture ran") for every text case the db s created seperatedly after runnning test the db is gonna drop all the data
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)










# client = TestClient(app)
# @pytest.fixture
# def session():
#     models.Base.metadata.drop_all(bind = engine)  
#     models.Base.metadata.create_all(bind = engine)
    
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture
# def client(session):
#     #runour code before we return our test
#     # models.Base.metadata.drop_all(bind = engine)  
#     # models.Base.metadata.create_all(bind = engine)
#     # command.upgrade("head") by using alembic
#     def override_get_db():
   
#        try:
#            yield session
#        finally:
#         session.close()
    
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)  #same as return but gives flexibily
#     #run our code after our test finsihes
#     #models.Base.metadata.drop_all(bind = engine)  #these line will delete all the tables after test runs

