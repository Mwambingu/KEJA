from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.basemodel import BaseModel, Base
from models.tenants import Tenant
from models.landlord import Landlord
from models.apartment import Apartment
from models.house import House

classes = {
  "Tenant": Tenant,
  "Landlord": Landlord,
  "Apartment": Apartment,
  "House": House
}

class DBStorage():
  __engine=None
  __session=None

  def __init__(self):
    self.__engine = create_engine("mysql+mysqldb://keja_admin:keja001@localhost/Keja_TestDB", echo=True, pool_pre_ping=True)
  
  def new(self, obj):
    self.__session.add(obj)

  def save(self):
    self.__session.commit()
  
  def list_all(self, obj=None):
    obj_list = []
    if obj:
      obj_list = self.__session.query(classes[obj]).all()
    else:
      for value in classes.values():
        obj_list += self.__session.query(value).all()
    return obj_list
  
  def delete(self, obj=None):
    if obj:
      self.__session.delete(obj)

  def reload(self):
    Base.metadata.create_all(self.__engine)
    session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    self.__session=scoped_session(session_factory)