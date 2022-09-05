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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','Laprincenoble97','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            "question": "Which subject studies living and non-living things?",
            "answer": "Biology",
            "difficulty": "1",
            "category": "1"
        }
        
        self.wrong_question = {
            "question": "Which subject studies living and non-living things?",
            "answer": "Biology",
            "difficulty": "hard",
            "category": "science"
        }

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
    def test_get_all_categories(self):
        endpoint = self.client().get('/categories')
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        
    def test_get_paginated_questions(self):
        endpoint = self.client().get('/questions')
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_404_question_from_invalid_page_number(self):
        endpoint = self.client().get("/questions?page=1000")
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_create_new_question(self):
        endpoint = self.client().post('/questions', json=self.new_question)
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        
    def test_422_create_question_with_wrong_input(self):
        # Will test to add questions with wron inputs from form
        endpoint = self.client().post('/questions', json=self.wrong_question)
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable')
    
    def test_delete_question(self):
        endpoint = self.client().delete('/questions/20')
        data = json.loads(endpoint.data)
        # Query the same id of deleted question; used to confirm if actually deleted
        question = Question.query.filter(Question.id == 20).one_or_none()
        self.assertEqual(endpoint.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 20)
        self.assertEqual(question, None)
    
    def test_422_delete_with_invalid_question_id(self):
        endpoint = self.client().delete('/questions/100')
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")
    
    def test_search_questions_with_results(self):
        endpoint = self.client().post('/questions/search', json = {"searchTerm": "american"})
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)
        
    def test_search_questions_without_results(self):
        endpoint = self.client().post('/questions/search', json = {"searchTerm": "devil"})
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
        
    def test_get_question_by_category(self):
        endpoint = self.client().get('/categories/1/questions')
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'Science')
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 3)
        
        
    def test_404_get_question_by_invalid_category(self):
        endpoint = self.client().get('/categories/20/questions')
        data = json.loads(endpoint.data)
        self.assertEqual(endpoint.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()