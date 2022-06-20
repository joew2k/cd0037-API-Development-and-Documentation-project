
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from  sqlalchemy.sql.expression import func

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

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)
  
    @app.after_request
    def after_request(response) :
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
        ) 
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTIONS'
            )
        return response

    @app.route('/categories')
    def categories():
        categories ={}
        selection = Category.query.all()
        #current_categories = pagination_categories(request, selection)
        if len(selection) == 0:
            abort(404)
        for category in selection:
            categories[category.id]= category.type
            
        return jsonify(
           {'categories':categories}
                    )

    @app.route('/questions')
    def questions():
        categories = {}
        categories_query = Category.query.all()
        for category in categories_query:
            categories[category.id] = category.type
        selection = Question.query.all()
        current_questions = pagination_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        return jsonify(
            {
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categories
        })

 
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

    @app.route('/questions', methods = ['POST'])
    def add_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        search = body.get("searchTerm", None)
        print(search)
        
        try:
            if search:
                selection = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search))
                )
                current_questions = pagination_questions(request, selection)
                print(current_questions)
                if len(current_questions) == 0:
                    return {
                        'questions': [{'question':'Question is not Available'}]
                    }
                return {
                    "questions": current_questions,
                    "totalQuestions": len(Question.query.all())
                        }
            else:
                question = Question(question = question, answer= answer, difficulty= difficulty, category= category)
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = pagination_questions(request, selection)

                return jsonify({
                'success': True,
                'new_question_id': question.id,
                'questions': current_questions,
                'totalQuestions': len(Question.query.all())
            })
        except:
            return abort(404)
        
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

    @app.route('/categories/<int:category_id>/questions')
    def question_categories(category_id):
        category_query = Category.query.filter(Category.id==category_id).all()
        category_list = []
        for category in category_query:
            category_list.append(category.type)
        print(category_list[0])
        selection = Question.query.filter(Question.category==category_id).all()
        current_questions = pagination_questions(request, selection)
        return jsonify({
            'success': True,
            'totalQuestions':len(selection),
            'questions': current_questions,
            'currentCategory':category_list[0]    
        })
        
    @app.route('/quizzes', methods = ['POST'])
    def random_questions():
        body = request.get_json('play-category')
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')['id']
        quiz_category_catgory = body.get('quiz_category')['type']
        print(previous_questions)

        if quiz_category==0:
            selection = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1)
            current_question = pagination_questions(request, selection)
            print(current_question)
        else:
            selection = Question.query.filter(Question.category==quiz_category and ~Question.id.in_(previous_questions)).order_by(func.random()).limit(1)
            current_question = pagination_questions(request, selection)
            print(current_question)
        return {
                "question": {
                "id": current_question[0]['id'],
                "question": current_question[0]['question'],
                "answer": current_question[0]['answer'],
                "difficulty": current_question[0]['category'],
                "category": current_question[0]['difficulty']
                }
}

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message':'bad_rquest'
            }), 400

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

