import os
from sqlalchemy import ForeignKey, Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json
from datetime import date


database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    '''binds a flask application and a SQLAlchemy service'''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    '''drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''this will initialize the database with some test records.'''
    new_movie = (Movie(
        title = 'Arthur\'s first Movie',
        release_date = date.today()
        ))

    new_actor = (Actor(
        name = 'Arthur',
        gender = 'Male',
        age = 25,
        movie_id = 1
        ))



    new_movie.insert()
    db.session.commit()
    new_actor.insert()
    db.session.commit()



class Actor(db.Model):  
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)

    def __init__(self, name, gender, age, movie_id):
        self.name = name
        self.gender = gender
        self.age = age
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name' : self.name,
        'gender': self.gender,
        'age': self.age,
        'movie_id': self.movie_id
        }

#----------------------------------------------------------------------------#
# Movies Model 
#----------------------------------------------------------------------------#

class Movie(db.Model):  
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = relationship('Actor', backref="movie", lazy=True)

    def __init__(self, title, release_date) :
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title' : self.title,
        'release_date': self.release_date,
        'actors': list(map(lambda actor: actor.format(), self.actors))
        }