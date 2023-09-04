from tkinter import Text
from . import db 
from flask_login import UserMixin 
<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, PickleType, Date
=======
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, PickleType, Date, UniqueConstraint
>>>>>>> Stashed changes
from sqlalchemy.orm import relationship
from datetime import date

class User(db.Model, UserMixin):                                
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    first_name = Column(String(150))
    last_name= Column(String(150))
    date_of_birth = Column(Date)
    gender = Column(String(150), nullable=False)
    account_type = Column(String(20), nullable=False)
    profile_picture = Column(String(100), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': account_type
    }

    def __init__(self, email, password, gender, account_type):
        self.email = email
        self.password = password
        self.gender = gender
        self.account_type = account_type

class Client(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    nutritionist_id = Column(Integer, ForeignKey('nutritionist.id'))
    nutritionist = relationship('Nutritionist', back_populates='clients', foreign_keys=[nutritionist_id])
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    goal = Column(String(50), nullable=True)
    desired_weight = Column(Float, nullable=True)
    desired_date = Column(Date)

<<<<<<< Updated upstream
    notifications = relationship('Notification', back_populates='client')
=======
    breakfast_calories = Column(Integer, nullable=True)
    lunch_calories = Column(Integer, nullable=True)
    dinner_calories = Column(Integer, nullable=True)
    snack_calories = Column(Integer, nullable=True)

    notifications = relationship('Notification', back_populates='client')
    my_plan = relationship('MyPlan', uselist=False, back_populates='client')
    weight_records = relationship('ClientWeight', backref='client', lazy=True)
>>>>>>> Stashed changes

    __mapper_args__ = {
        'polymorphic_identity': 'client'
    }

    def __init__(self, nutritionist_id=None, height=None, weight=None, goal=None, desired_weight=None, desired_date=None, **kwargs):
        super().__init__(**kwargs)
        self.nutritionist_id = nutritionist_id
        self.height = height
        self.weight = weight
        self.bmi = None
        self.goal = goal
        self.desired_weight = desired_weight
        self.desired_date = desired_date

<<<<<<< Updated upstream
=======
class ClientWeight(db.Model):
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    recorded_weight = Column(Float(precision=1), nullable=False)
    weight_date = Column(Date, nullable=False, default=date.today)

>>>>>>> Stashed changes
class Afflictions(db.Model):
    id = Column(Integer, primary_key = True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    affliction_name = Column(String(30), nullable=False)

class Medication(db.Model):
    id = Column(Integer, primary_key = True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    medication_name = Column(String(30), nullable=False)

class AllergiesIntolerances(db.Model):
    id = Column(Integer, primary_key = True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    allergy_name = Column(String(30), nullable=False)

class Recommendation(db.Model):
    id = Column(Integer, primary_key=True)
    nutritionist_id = Column(Integer, ForeignKey('nutritionist.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    rec_category = Column(String, nullable=False)
    content = Column(Text, nullable=False)

class Nutritionist(User): 
  id = Column(Integer, ForeignKey('user.id'), primary_key=True)
  address = Column(String(500))
  city = Column(String(500))
  country = Column(String(500))
  phone_number = Column(String(15))
  description = Column(Text)

  clients = relationship('Client', back_populates='nutritionist', foreign_keys=[Client.nutritionist_id])
  notifications = relationship('Notification', back_populates='nutritionist')

  __mapper_args__ = {
        'polymorphic_identity': 'nutritionist'
  }

  def __init__(self, address=None, city=None, country=None, phone_number=None, description=None, **kwargs):
        super().__init__(**kwargs)
        self.address = address
        self.city = city
        self.country = country
        self.phone_number = phone_number
        self.description = description

class Experience(db.Model):
    id = Column(Integer, primary_key = True)
    nutritionist_id = Column(Integer, ForeignKey('nutritionist.id'), nullable=False)
    job = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    job_description = Column(Text, nullable=False)
    job_start_year = Column(Integer, nullable=False)
    job_end_year = Column(Integer, nullable=False)

class Education(db.Model):
    id = Column(Integer, primary_key=True)
    nutritionist_id = Column(Integer, ForeignKey('nutritionist.id'), nullable=False)
    school = Column(String(100), nullable=False)
    degree = Column(String(100), nullable=False)
    field_of_study = Column(String(100), nullable=False)
    education_start_year = Column(Integer, nullable=False)
    education_end_year = Column(Integer, nullable=False)

class RelatedInterests(db.Model):
    id = Column(Integer, primary_key=True)
    nutritionist_id = Column(Integer, ForeignKey('nutritionist.id'), nullable=False)
    interest = Column(String(100), nullable=False)
    interest_description = Column(Text, nullable=False)

class Notification(db.Model):
    id = Column(Integer, primary_key=True)
    message = Column(String(255), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'))
    nutritionist_id = Column(Integer, ForeignKey('nutritionist.id'))
    status = Column(String(20), nullable=False)  # 'pending', 'accepted', 'declined'
    #created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship('Client', back_populates='notifications', foreign_keys=[client_id])
    nutritionist = relationship('Nutritionist', back_populates='notifications', foreign_keys=[nutritionist_id])

class Recipe(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    recipe_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
<<<<<<< Updated upstream
    ingredients = db.relationship('RecipeIngredients', backref='recipe', lazy=True)

    def __init__(self, title, recipe_type, description):
        self.title = title
        self.recipe_type = recipe_type
        self.description = description
=======
    ingredients = relationship('RecipeIngredients', backref='recipe', lazy=True)
    recipe_picture = Column(String(255), default='static/recipe_pictures/default.jpg')

    total_calories = Column(Integer, nullable=True)
    total_proteins = Column(Integer, nullable=True)
    total_carbs = Column(Integer, nullable=True)
    total_fats = Column(Integer, nullable=True)

    def __init__(self, title, recipe_type, description, total_calories, total_proteins, total_carbs, total_fats):
        self.title = title
        self.recipe_type = recipe_type
        self.description = description
        self.total_calories = total_calories
        self.total_proteins = total_proteins
        self.total_carbs = total_carbs
        self.total_fats = total_fats

>>>>>>> Stashed changes

class Ingredient(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=True)
    proteins = Column(Integer, nullable=True)
    carbs = Column(Integer, nullable=True)
    fats = Column(Integer, nullable=True)

    def __init__(self, name, category, calories, proteins, carbs, fats):
        self.name = name
        self.category = category
        self.calories = calories
        self.proteins = proteins
        self.carbs = carbs
        self.fats = fats

class RecipeIngredients(db.Model):
<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    measurement = db.Column(db.String, nullable=False)

    def __init__(self, recipe_id, ingredient_id, amount, measurement):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.amount = amount
        self.measurement = measurement

=======
    recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    ingredient_name = Column(Text, ForeignKey('ingredient.name'), nullable=False)
    amount = Column(Integer, nullable=False)
    measurement = Column(String(50), nullable=False)

    def __init__(self, recipe_id, ingredient_id, ingredient_name, amount, measurement):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.ingredient_name = ingredient_name
        self.amount = amount
        self.measurement = measurement

class RecommendedRecipe(db.Model):
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)

    # Define relationships
    client = relationship('Client', backref=db.backref('recommended_recipes', lazy=True))
    recipe = relationship('Recipe', backref=db.backref('recommendations', lazy=True))

    def __init__(self, client_id, recipe_id):
        self.client_id = client_id
        self.recipe_id = recipe_id

class MyPlan(db.Model):
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    meal_date = Column(Date)
    meal_name = Column(String(30))

    client = relationship('Client', back_populates='my_plan')
    recipe = relationship('Recipe', backref='recipe', lazy=True)

>>>>>>> Stashed changes
