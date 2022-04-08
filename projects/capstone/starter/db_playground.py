
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    # actors = relationship('Association', backref='movie')


class Actors(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    gender = Column(String)
    name = Column(String)
    # movies = relationship('Association', backref='actor')


class Association(Base):
    __tablename__ = 'association'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer,ForeignKey('movies.id'))
    actor_id = Column(Integer, ForeignKey('actors.id'))
    movie = relationship('Movies',backref="actors")
    actor = relationship('Actors', backref="movies")