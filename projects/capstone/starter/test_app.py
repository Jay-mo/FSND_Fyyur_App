
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies
from dateutil.parser import parse


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        database_username = os.getenv('DBUSER')
        database_password = os.getenv('DBPASS')
        self.database_path = "postgresql://{}:{}@{}/{}".format(database_username, database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            new_movie = Movies("Transformers", parse("July 3, 2007"))
            self.db.session.add(new_movie)
            self.db.session.commit()

        self.test_movie = {
                        "title": "Sweet November",
                        "release_date": parse("February 16, 2001")
                    }

        self.test_actor = {
                        "name": "Keanu Reeves",
                        "age": "57",
                        "gender": "Male"
                    }

        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNWYzVhSkVMamIyS0ZjcTJZWVFtQiJ9.eyJpc3MiOiJodHRwczovL21vdmllLWFwcC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MjJhNDE2M2ExNzEyYTAwNjk5ZTk4Y2YiLCJhdWQiOiJtb3ZpZS1hcHAtZnNuZC1hcGkiLCJpYXQiOjE2NDcwMTczNTQsImV4cCI6MTY0NzAyNDU1NCwiYXpwIjoibUcwV25FOG1kbUlFaW9sYUkweXVycjgwTG83dkRjdUQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3IiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWUiLCJyZWFkOm1vdmllcyJdfQ.e0viLXQsQNzRfRrIcn1kQvd7t89YlIwPytkoNFALf49IQ0H8yDr-MI19vMQ21iT5vMCBfbZNLUyBYcsYWwe2kZg13TjFT7QcZZQVO_jHFzNRVSILqUUMYz0q6K7xSNTpQhBpVdSEIEstFPfeQLQTWNQEBKOO2xqRo7dGHiz7VLRTIzYNi3c3XRnnEZB574fEMvERw3CxdW3M_xG5HxbQuBI9xa-RsWWE2pN3QhwiMPhT8Tx6i-OhvwXnFp9DPSgnDU_JDsK3BCP93BHmSxmcOIoK9_BcRFnyaM-B1pXPNsFkJ8_noPMHdhd8df1pnr79gI9y8J2jpJoEh5h1YYAS0g"


    def tearDown(self):
        """Executed after reach test"""
        
        with self.app.app_context():
            self.db.drop_all()

        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_movies(self):
        res = self.client().get("/movies", headers={
                "Authorization":
                "Bearer {}".format(self.token)
            })
        print(res.data)

        # self.assertEqual(res.status_code, 200)
        # self.assertTrue(data['title'])
        # self.assertTrue(data['release_date'])

    # def test_404_wrong_endpoint(self):
    #     res = self.client().get("/game_quizzes")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "resource not found")


    # def test_get_paginated_questions(self):
    #     res = self.client().get("/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["categories"])
    #     self.assertTrue(len(data["questions"]))

    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get("/questions?page=100")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_create_new_question(self):
    #     res = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)

    # def test_405_if_question_creation_not_allowed(self):
    #     res = self.client().post("/questions/2", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "method not allowed")

    # def test_get_question_by_category(self):
    #     res = self.client().get("/categories/{}/questions".format(self.new_question["category"]))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["currentCategory"])
    #     self.assertTrue(data["questions"])
    
    # def test_404_get_question_by_category(self):
    #     res = self.client().get("/categories/{}/questions".format('25'))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data['message'], "resource not found")


    
    # def test_play_quiz(self):
    #     res = self.client().post("/quizzes", json=self.quiz_data)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["question"])


    # def test_422_play_quiz(self):
    #     res = self.client().post("/quizzes", json={})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")


    # def test_delete_question(self):

    #     del_question = Question.query.order_by(Question.id.desc()).first()
    #     res = self.client().delete("/questions/{}".format(del_question.id) )
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == del_question.id).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(question, None)

    # def test_404_delete_question_not_found(self):
    #     res = self.client().delete("/questions/2700")
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 2700).one_or_none()

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(question, None)




    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()