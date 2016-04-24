import sys
import os
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = "ct_user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__="ct_category"
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    items = relationship("Items", back_populates="category")
    user_id = Column(Integer, ForeignKey('ct_user.id'))
    user = relationship(User)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Items(Base):
    __tablename__="ct_items"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer,ForeignKey('ct_category.id'))
    category = relationship("Category", back_populates="items", uselist=False)
    user_id = Column(Integer, ForeignKey('ct_user.id'))
    user = relationship(User)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category_id': self.category_id,
        }

if __name__ == '__main__':
    # When no username is provided by the connection, the username defaults to user logged in the os
    engine = create_engine("postgresql:///catalogdb")
    Base.metadata.create_all(engine)