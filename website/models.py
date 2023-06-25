from tkinter import Text
from . import db 
from flask_login import UserMixin 
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, PickleType
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):                                
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    first_name = Column(String(150))
    last_name= Column(String(150))
    age = Column(Integer)
    gender = Column(String(150), nullable=False)
    account_type = Column(String(20), nullable=False)
    profile_picture = Column(String(100), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': account_type
    }

class Client(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    nutritionist_id = Column(Integer, ForeignKey('nutritionist.id'))
    nutritionist = relationship('Nutritionist', back_populates='clients', foreign_keys=[nutritionist_id])
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'client'
    }

class Nutritionist(User): 
  id = Column(Integer, ForeignKey('user.id'), primary_key=True)
  clients = relationship('Client', back_populates='nutritionist', foreign_keys=[Client.nutritionist_id])

  __mapper_args__ = {
        'polymorphic_identity': 'nutritionist'
  }

class Recipe(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    recipe_type = Column(String(50), nullable=False)
    ingredients = Column(PickleType, nullable=False)
    description = Column(Text, nullable=False)

class Ingredient(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    afflictions = Column(String(100), nullable=True)
