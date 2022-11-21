from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.basemodel import BaseModel, Base

class DBStorage():
  __engine=None
  __session=None

  def __init__(self):
    self.__engine = create_engine("mysql+mysqldb://keja_admin:keja001@localhost/Keja_TestDB", echo=True, pool_pre_ping=True)

  
  def new(self, obj):
    self.__session.add(obj)

  def save(self, obj):
    self.__session.commit()
  
  def delete(self, obj=None):
    if obj:
      self.__session.delete(obj)

  def reload(self):
    Base.metadata.create_all(self.__engine)
    session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    self.__session=scoped_session(session_factory)