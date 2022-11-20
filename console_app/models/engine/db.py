from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.basemodel import BaseModel

class DBStorage():
  __engine=None
  __session=None

  def __init__(self):
    self.__engine = create_engine("mysql+mysqldb://keja_admin:keja001@localhost/Keja_TestDB")
