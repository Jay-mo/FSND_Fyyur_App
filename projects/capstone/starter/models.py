import os
from platform import release
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json

database_name = os.getenv("DBNAME")
database_user = os.getenv("DBUSER")
database_password = os.getenv("DBPASS")
database_server = "localhost:5432"

database_path = "postgresql://{}:{}@{}/{}".format(database_user,database_password,database_server,database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


actor_movie = db.Table("actor_movie",
                    Column("movie_id",Integer,ForeignKey('movies.id')),
                    Column("actor_id",Integer, ForeignKey('actors.id')) )

class Movies(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)

    def __init__(self, title, release_date):
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

    def __repr__(self) -> str:
        return "<Movie {}>".format(self.title)

    def format(self):
        return {
            'title': self.title,
            'release_date': self.release_date
        }



class Actors(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movies = relationship('Movies',secondary=actor_movie, backref="actors")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Actor {}>".format(self.name)

    def format(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


# class Association(db.Model):
#     __tablename__ = 'association'
#     id = Column(Integer, primary_key=True)
#     movie_id = Column(Integer,ForeignKey('movies.id'))
#     actor_id = Column(Integer, ForeignKey('actors.id'))
#     movie = relationship('Movies',backref="actors")
#     actor = relationship('Actors', backref="movies")

