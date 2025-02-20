import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(env['DB_USER'], env['DB_PASSWORD'], env['HOST'], self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {'question': 'What is the capital of Nigeria', 'answer': 'Abuja', 'category': 3, 'difficulty': 3}

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
    
    def test_get_paginated_question_404(self):
        res = self.client().get('/question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.data))

    def test_get_categories_404(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(len(res.data))
    
    def test_delete_question(self):
        res = self.client().delete('/questions/25')
        self.assertEqual(res.status_code, 200) 
    
    def test_delete_question_400(self):
        res = self.client().delete('/questions/120')
        self.assertEqual(res.status_code, 400) 

    def test_delete_question_405(self):
        res = self.client().delete('/questions')
        self.assertEqual(res.status_code, 405) 

    
    def test_new_question(self):
        res = self.client().post('/questions', json = self.new_question)
        self.assertEqual(res.status_code, 200) 
    
    def test_new_question_405(self):
        res = self.client().post('/questions/1', json = self.new_question)
        self.assertEqual(res.status_code, 405) 
    
    def test_search_term(self):
        res = self.client().post('/questions/search', json = {'searchTerm': 'nigeria'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertTrue(len(data['questions']))
    
    def test_search_term_no_result(self):
        res = self.client().post('/questions/search', json = {'searchTerm': 'gsttg'})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], False)

    
    def test_question_based_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
    
    def test_question_based_category_404(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status, '404 NOT FOUND')
        self.assertEqual(data['success'], False)

    def test_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions":[], "quiz_category": {"id":0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_quizzes_404(self):
        res = self.client().post('/quizzes/1', json={"previous_questions":[], "quiz_category": {"id":0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()