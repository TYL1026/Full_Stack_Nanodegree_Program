import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Category,setup_db,Question
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formated_categories = {category.id:category.type for category in categories}
    return jsonify({
      'success':True,
      'categories':formated_categories
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
  def get_questions():
    try:
      questions = Question.query.order_by(Question.id).all()
      if len(questions) == 0:
        abort(404)
      current_questions = pagination_questions(request,questions)
      if len(current_questions) == 0:
        abort(404)
      formated_questions = [question.format() for question in current_questions]
      categories = Category.query.all()
      formated_categories = {category.id:category.type for category in categories}
      return jsonify({
        'success':True,
        'questions':formated_questions,
        'total_questions':len(questions),
        'categories':formated_categories,
        'currentCategory':None
      })
    except:
      abort(422)

  def pagination_questions(request,questions):
    try:
      page = request.args.get('page')
      start = (int(page)-1)*10
      end = start+10
      current_questions = questions[start:end]
      return current_questions
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    try:
      question = Question.query.filter_by(id=question_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()
      return jsonify({
        'success':True,
        'delete':question_id
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
  @app.route('/questions',methods=['POST'])
  def create_questions():
    try:
      questions = request.get_json()
      question = questions.get('question')
      answer = questions.get('answer')
      difficulty = questions.get('difficulty')
      category = questions.get('category')
      if question is None or answer is None:
        abort(404)
      new_question = Question(question=question,answer=answer,
                              difficulty=difficulty,category=category)
      new_question.insert()
      return jsonify({
        'success':True,
        'created':new_question.id
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
  @app.route('/questions/search',methods=['POST'])
  def search_questions():
    try:
      search = request.get_json()
      term = search.get('searchTerm')
      if term is None:
        abort(404)
      results = Question.query.filter(Question.question.ilike('%{}%'.format(term))).all()
      formatted_result = [result.format() for result in results]
      return jsonify({
        'success':True,
        'questions':formatted_result,
        'totalQuestions':len(results),
        'currentCategory':None
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
  @app.route('/categories/<int:id>/questions')
  def questions_by_categories(id):
    try:
      if id > 10:
        abort(404)
      questions = Question.query.filter_by(category=id).all()
      formated_questions = [question.format() for question in questions]
      return jsonify({
        'success':True,
        'questions':formated_questions,
        'totalQuestions':len(questions),
        'currentCategory': id
      })
    except:
      abort(422)
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
  @app.route('/quizzes',methods=['POST'])
  def quizzes():
    try:
      quiz = request.get_json()
      previous_questions = quiz.get('previous_questions')
      quiz_category = quiz.get('quiz_category')
      unasked = []
      if quiz_category['id'] == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.filter_by(category=quiz_category['id']).all()
      if questions is None :
        abort(404)
      for question in questions:
        if question.id not in previous_questions:
          unasked.append(question.format())
      result = random.choice(unasked)
      previous_questions.append(result)
      return jsonify({
        'success':True,
        'previousQuestions':previous_questions,
        'question':result
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
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  return app

    