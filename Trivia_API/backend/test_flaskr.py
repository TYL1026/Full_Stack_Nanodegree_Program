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
        self.database_name = "trivia"
        self.database_path = "postgres://postgres:123qwe@localhost:5432/trivia"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])

    def test_422_get_questions_invalid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_delete_questions(self):
        res = self.client().delete("/questions/13")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["delete"])
    def test_422_delete_questions(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)
        self.assertEqual(data['error'], 422)

    def test_create_questions(self):
        res = self.client().post("/questions",json={'question':'123456',
                                                    'answer':'123456',
                                                    'difficulty':1,
                                                    'category':1,
                                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
    def test_422_create_questions(self):
        res = self.client().post("/questions",json={'question':'123456',
                                                    'difficulty':'1',
                                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data["success"],False)

    def test_search_questions(self):
        res = self.client().post("/questions/search",json={'searchTerm':'123'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"],True)
    def test_422_search_questions(self):
        res = self.client().post("/questions/search",json={'searchTer':'123'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"],False)


    def test_questions_by_categories(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
    def test_422_questions_by_categories(self):
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"],False)

    def test_quiz(self):
        res = self.client().post("/quizzes",json={"previous_questions": [],
                                                    "quiz_category": {'type': 'Science', 'id': '1'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
    def test_422_quiz(self):
        res = self.client().post("/quizzes",json={"previous_questions": [],
                                                    "quiz_category": {'type': 'Science', 'id': '10000000000'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
