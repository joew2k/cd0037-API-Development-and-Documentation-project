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
        self.database_path = "postgresql://{}:{}@{}/{}".format('jose','Odom232#','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {'question': 'What is the capital of Nigeria', 'answer': 'Abuja', 'categroy': 3, 'difficulty': 3}

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
    def test_get_paginated_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.data))
        #self.assertEqual(data['success'], True)


    
    def test_delete_question(self):
        res = self.client().delete('/questions/19')
        self.assertEqual(res.status, '200 OK') 
    
    def test_new_question(self):
        res = self.client().post('/questions', json = self.new_question)
        self.assertEqual(res.status, '200 OK') 
    
    def test_search_term(self):
        res = self.client().post('/questions', json = {'search': 'nigeria'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['search_questions']), 10)
    
    def test_question_based_category(self):
        res = self.client().get('/categories/2')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
    

    def test_question_quize(self):
        res = self.client().get('/questions/2/2')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()