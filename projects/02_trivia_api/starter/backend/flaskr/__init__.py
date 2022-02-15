import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(questions,page):
  start = ( page - 1 )  * QUESTIONS_PER_PAGE

  end = page * QUESTIONS_PER_PAGE

  return questions[start:end]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors= CORS(app, resources={r"/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
      response.headers.add("Access-Control-Allow-Headers",
                      "Content-Type, authorization, true")
      
      response.headers.add("Access-Control-Allow-Methods",
                      'GET, POST, PATCH, DELETE, OPTIONS')


      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_all_categories():
    categories = Category.query.order_by(Category.id).all()

    category_names = { category.id: category.type for category in categories }

    return jsonify({
      'success': True,
      'categories': category_names
    })
    


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.
  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_paginated_questions():

  
    page_number = request.args.get('page', default=1, type=int)

    all_questions = Question.query.order_by(Question.id).all()

    paginated_questions = paginate(all_questions,page_number)

    if len(paginated_questions) == 0:
      abort(404)

    categories = Category.query.order_by(Category.id).all()

    category_names = { category.id: category.type for category in categories }

    return jsonify({
      'success': True,
      'questions': [ question.format() for question in paginated_questions ],
      'categories': category_names,
      'current_category': None

    })
    

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):

    delete_question = Question.query.filter(Question.id == question_id).one_or_none()

    if delete_question is None:
      abort(404)


    try:
   
      delete_question.delete()

      return jsonify({
        "success": True
      })
    except: 
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def post_question():

    body = request.get_json()
    new_question =   body.get('question', None)
    new_answer =     body.get('answer',None)
    new_difficulty = body.get('difficulty', None)
    new_category =   body.get('category', None)

    try:

      new_question = Question(
        question=new_question,
        answer=new_answer,
        difficulty=new_difficulty,
        category=new_category
    )

      new_question.insert()
      

      return jsonify({
        'success': True
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=["POST"])
  def post_search_questions():
    body = request.get_json()

    search_term = body.get('searchTerm', None)

    if search_term is None:
      abort(400)

    try:
      question_results = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()

      return jsonify({
        'success': True,
        'questions': [ question.format() for question in question_results ],
        'totalQuestions': len(question_results),
        'currentCategory': None
      })
    except:
      abort(422)



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def get_category_questions(category_id):
    try:
      question_list = Question.query.filter(Question.category == category_id).all()
      current_category = Category.query.get(category_id).type

      return jsonify({
        'success': True,
        'questions': [ question.format() for question in question_list ],
        'totalQuestions': len(question_list),
        'currentCategory': current_category
      })
    except:
      abort(404)

    



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def post_play_quiz():

    try:
      body = request.get_json()

      previous_questions = body.get("previous_questions", None)
      # print(previous_questions)
      quiz_category = body.get("quiz_category", None)
      # print(quiz_category)

      if quiz_category['id'] == 0:
        questions_for_category = Question.query.all()

      else:
        questions_for_category = Question.query.filter(Question.category==quiz_category['id']).all()

      possible_next_questions = [ question for question in questions_for_category if question.id not in previous_questions]
      
      if possible_next_questions:
        next_question = random.choice(possible_next_questions)

        return jsonify({
          "success": True,
          "question": next_question.format()
        })
      else:
        next_question = None
        return jsonify({
          "success": True,
          "question": None
        })
    except:
      abort(422)


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return ( jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404)

  @app.errorhandler(400)
  def bad_request(error):
    return ( jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400)

  @app.errorhandler(422)
  def unprocessable(error):
      return ( jsonify({
        "success": False, 
        "error": 422, 
        "message": "unprocessable"
        }),422,
      )

  @app.errorhandler(405)
  def method_not_allowed(error):
      return ( jsonify({
        "success": False, 
        "error": 405, 
        "message": "method not allowed"
        }),405,
      )
  
  return app

    