import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
      page = request.args.get("page", 1, type=int)
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
  
  '''
  @DONE
  
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @DONE
  
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  #CORS Headers
  
  @app.after_request
  def after_request(response):
        response.headers.add(
              'Access-Control-Allow-Headers', 
              'Content-Type, Authorization, True'
              )
        
        response.headers.add(
              'Access-Control-Allow-Methods', 
              'GET, POST, PATCH, DELETE, OPTIONS'
              )
        
        response.headers.add(
              'Access-Control-Allow-Origin',
              '*'
        )
        
        return response
     
      
  '''
  @DONE
  
  @TODO: Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
        
      try:
            categories = Category.query.order_by(Category.id).all()
            
            # Checks if the query return empty, then loads a 404 - not found
            if len(categories) == 0:
                  abort(404)
                  
            return jsonify({
            "success": True,
            "categories": {category.id: category.type for category in categories}
            })
            
      except:
            abort(422)


  '''
  @DONE
  
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
  @app.route('/questions', methods=['GET'])
  def get_questions():
      
      selection = Question.query.all()
      current_questions = paginate_questions(request, selection)
      
      if len(current_questions) == 0:
            abort(404)
      
      return jsonify({
        "success": True,
        "questions": current_questions,
        "total_questions": len(selection),
        "categories": {category.id:category.type for category in Category.query.all()},
        "current_category": "All"
      })
    

  '''
  @DONE
  
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      question = Question.query.get(question_id)
      
      try:
            if question is None:
                  abort(404)

            question.delete()
            
            selection = Question.query.all()
            
            # Reloads all questions after deleting the specified record
            current_questions = paginate_questions(request, selection)
            
            if len(current_questions) == 0:
                  abort(404)
            
            return jsonify({
            "success": True,
            "deleted": question_id
            })
      except:
            abort(422)
      

  '''
  @DONE
  
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()
      
      new_question = body.get("question", None)
      new_answer = body.get("answer", None)
      new_difficulty = body.get("difficulty", None)
      new_category = body.get("category", None)
      
      try:  
            # Checks data from input fields not to persist empty field in database
            if not new_question or not new_answer or not new_category or not new_difficulty:
                abort(422)    
                
            question = Question(
                  question = new_question, 
                  answer = new_answer,
                  category = new_category,
                  difficulty = new_difficulty)
            question.insert()
            
            return jsonify({
                  "success": True,
                  "created": question.id
            })
            
      except:
            abort(422)
      

  '''
  @DONE
  
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
      body = request.get_json()
      
      search = body.get("searchTerm", None)
      
      
      if search:
            selection = Question.query.order_by(Question.id).filter(
                        Question.question.ilike("%{}%".format(search))
                  )
      
            current_questions = paginate_questions(request, selection)

                  
      return jsonify(
            {
            "success": True,
            "questions": current_questions,
            "total_questions": len(current_questions),
            "current_category":"All"
            } 
      )
        
      

  '''
  @DONE
  
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def questions_by_category(id):
      category = Category.query.filter(Category.id == id).first()
      try:
            if category:
                  selection = Question.query.order_by(Question.id).filter(
                        Question.category == id).all()
                  
                  current_questions = paginate_questions(request, selection)
                  
            return jsonify({
                  "success": True,
                  "questions": current_questions,
                  "total_questions": len(selection),
                  "current_category": category.type
            })
      
      except:
            abort(404)


  '''
  @DONE
  
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
  def play_trivia():
      body = request.get_json()
      
      # Get the category selected by the user and 
      # all lists of previously answered question
      quiz_category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')
      
      try:
            # If user selected all category
            # returns random questions from database and 
            # check if they are not already listed as answered question
            
            # Else it returns random question based on selected category
            if quiz_category['id'] == 0:
                  questions = Question.query.filter(
                        Question.id.notin_(previous_questions)).all()
                  
            else:
                  questions = Question.query.filter(
                        Question.category == quiz_category['id'],
                        Question.id.notin_(previous_questions)).all()
                  
            next_question = random.choice(questions).format()
            
            return jsonify({
                  'success': True,
                  'question': next_question
            })
      except:
            abort(422)
            
       


  '''
  @DONE
  
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(400)
  def bad_request(error):
      return(
            jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request",
             }), 400
      )
  
  @app.errorhandler(404)
  def not_found(error):
      return(
            jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found",
             }), 404
      )
      
  @app.errorhandler(405)
  def not_allowed(error):
      return(
            jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed",
             }), 405
      )
      
  @app.errorhandler(422)
  def unprocessable(error):
      return(
            jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable",
             }), 422
      )

      
  @app.errorhandler(500)
  def internal_server_error(error):
      return(
            jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error",
             }), 500
      )
  
  return app