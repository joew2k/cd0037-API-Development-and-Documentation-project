
import json
import sys
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from  sqlalchemy.sql.expression import func, select

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Helper pagination fundction
def pagination_questions(request, selection):
    page = request.args.get('page', 1, type = int) 
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def pagination_categories(request, selection):
    page = request.args.get('page', 1, type = int) 
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_categories = questions[start:end]
    return current_categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response) :
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
        ) 
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTIONS'
            )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def categories():
        selection = Category.query.all()
        current_categories = pagination_categories(request, selection)
        if len(current_categories) == 0:
            abort(404)
        return jsonify(
            {
            'success': True,
            'category': current_categories,
            'total_categories': len(current_categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def questions():
        selection = Question.query.all()
        current_questions = pagination_categories(request, selection)
        if len(current_questions) == 0:
            abort(404)
        return jsonify(
            {
            'success': True,
            'category': current_questions,
            'total_questions': len(Question.query.all())
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods = ['DELETE'])
    def remove_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = pagination_questions(request, selection)
            return jsonify({
                'success':True,
                'deleted_id': question.id,
                'questions': current_questions,
                'total_questions_NOW': len(Question.query.all())
            })
        except:
            return abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods = ['POST'])
    def add_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('categories', None)
        search = body.get('search', None)
        question = Question(question = question, answer= answer, difficulty= difficulty, category= category)
        try:
            if search:
                selection = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search))
                )
                current_questions = pagination_questions(request, selection)
                return jsonify({
                    'success': True,
                    'search_questions': current_questions,
                    'total_search': len(current_questions)
                })
            else:
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = pagination_questions(request, selection)
                return jsonify({
                'success': True,
                'new_question_id': question.id,
                'question': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            return abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # @app.route('/questions', methods = ['POST'])
    # def search_question():
    #     body = request.get_json()
    #     search = body.get('search', None)

    #     try:
    #         if search:
    #             selection = Question.query.filter(
    #                 Question.question.ilike('%{}%').format(search)
    #             )
    #             current_questions = pagination_questions(request, selection)
    #             return jsonify({
    #                 'success': True,
    #                 'search_questions': current_questions,
    #                 'total_search': len(current_questions)
    #             })
    #         else:
    #             return abort(404)
    #     except:
    #         abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/questions/<int:categories>')
    def question_categories(categories):
        selection = Question.query.filter(Question.category==categories).all()
        current_questions = pagination_questions(request, selection)
        return jsonify({
            'success': True,
            'total_question':len(selection),
            'questions': current_questions
            
        })
        

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/questions/<int:category>/<int:pre_question_id>')
    def random_questions(category, pre_question_id):
        selection = Question.query.filter(
            Question.category==category).filter(Question.id != pre_question_id).order_by(func.random()).limit(1)
        current_question = pagination_questions(request, selection)
        return jsonify({
            'success': True,
            'question': current_question
        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message':'This page does not exist'
            }), 404

    @app.errorhandler(422)
    def Unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message':'Unprocessable'
            }), 422


    return app

