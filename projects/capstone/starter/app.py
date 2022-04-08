from crypt import methods
from distutils.log import error
import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, db, Actors, Movies
from dateutil.parser import parse
from auth_lib import require_auth, get_token_auth_header

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


  @app.route("/")
  @require_auth("read:actor")
  def hello_world(payload):
    return jsonify(payload)


  @app.route("/movies")
  @require_auth("read:movies")
  def get_movies():
    all_movies = Movies.query.all()

    data = [ movie.format() for movie in all_movies ]

    # print(data)

    

    # return jsonify(all_movies)
    return jsonify(data)


  @app.route("/actors")
  @require_auth("read:actors")
  def get_actors():
    all_actors = Actors.query.all()

    data = [actor.format() for actor in all_actors]

    print(data)

    # return jsonify(all_actors)
    return jsonify(data)



  @app.route("/movies", methods=["POST"])
  @require_auth("post:movie")
  def post_movies():
    request_body = request.json

    
    title = request_body["title"]
    release_date = parse(request_body["release_date"])
    new_movie = Movies(title=title, release_date=release_date)

    print(new_movie.release_date)


    try:
      new_movie.insert()

      return jsonify("Success")

    except:
      return jsonify("No success")



  @app.route("/actors", methods=["POST"])
  @require_auth("post:actor")
  def post_actors():
    request_body = request.json

    
    name = request_body["name"]
    age = request_body["age"]
    gender = request_body["gender"]
    new_actor = Actors(name,age,gender)

    


    try:
      new_actor.insert()

      return jsonify("Success")

    except:
      return jsonify("No success")




  @app.route("/movies/<int:movie_id>", methods=["DELETE"])
  @require_auth("delete:movies")
  def delete_movies(movie_id):

    movie_to_delete = db.session.query(Movies).filter(Movies.id == movie_id).first()

      
    print(movie_to_delete)

    try:
      movie_to_delete.delete()

      return jsonify("Success, deleted {}".format(movie_to_delete.id))

    except:
      return jsonify("No success")

    
      
    
      


  @app.route("/movies/<int:movie_id>", methods=["PATCH"])
  @require_auth("modify:movies")
  def patch_movies(movie_id):
    movie_to_patch = db.session.query(Movies).filter(Movies.id == movie_id).first()
    request_body = request.json
    title = request_body["title"]
    release_date = parse(request_body["release_date"])

    # print(movie_to_patch)

    try:
      
      movie_to_patch.title = title
      movie_to_patch.release_date = release_date

      movie_to_patch.update()

      return jsonify("Success, updated {}".format(movie_to_patch.id))

    except:
      return jsonify("No success")


  @app.route("/actors/<int:actor_id>", methods=["DELETE"])
  @require_auth("delete:actor")
  def delete_actors(actor_id):

    
    actor_to_delete = db.session.query(Actors).filter(Actors.id == actor_id).first()

    
    # print(actor_to_delete)

    try:
      actor_to_delete.delete()

      return jsonify("Success, deleted {}".format(actor_to_delete.id))

    except:
      return jsonify("No success")
    



  @app.route("/actors/<int:actor_id>", methods=["PATCH"])
  @require_auth("modify:actor")
  def patch_actors(actor_id):
    actor_to_patch = db.session.query(Actors).filter(Actors.id == actor_id).first()
    request_body = request.json
    


    name = request_body["name"]
    age = request_body["age"]
    gender = request_body["gender"]
    new_actor = Actors(name,age,gender)

    # print(actor_to_patch)

    try:
      
      actor_to_patch.name = name
      actor_to_patch.age = age
      actor_to_patch.gender = gender

      actor_to_patch.update()

      return jsonify("Success, updated {}".format(actor_to_patch.id))

    except:
      return jsonify("No success")


  return app

APP = create_app()

migrate = Migrate(APP,db)









if __name__ == '__main__':

  APP.run(host='0.0.0.0', port=8080, debug=True)





