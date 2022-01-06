import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        database_username = os.getenv('DBUSER')
        database_password = os.getenv('DBPASS')
        self.database_path = "postgres://{}:{}@{}/{}".format(database_username, database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "answer": "Accra",
            "category": 3,
            "difficulty": 3,
            "question": "What is the capital city of Ghana"
        }


    def tearDown(self):
        """Executed after reach test"""

        with self.app.app_context():
            self.db.drop_all()

        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get("/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_wrong_endpoint(self):
        res = self.client().get("/game_quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")


    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/2", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_delete_question(self):

        del_question = Question.query.order_by(Question.id.desc()).first()
        res = self.client().delete("/questions/{}".format(del_question.id) )
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == del_question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(question, None)

    def test_404_delete_question_not_found(self):
        res = self.client().delete("/questions/2700")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2700).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(question, None)




    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()