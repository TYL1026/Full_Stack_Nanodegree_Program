import os
from flask import Flask, request, abort, jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movies,setup_db,Actors,db_drop_and_create_all
import json
from auth import AuthError, requires_auth
def create_app(test_config=None):
  # create and configure the app
	app = Flask(__name__)
	CORS(app)
	setup_db(app)
	# db_drop_and_create_all()
##GET
	##get all actors
	@app.route('/actors')

	def get_actors():
		return jsonify({
			'success': True,
			'actors': [actor.format() for actor in Actors.query.all()]
		})

	##get all movies
	@app.route('/movies')
	@requires_auth('get:movies')
	def get_movies(payload):
		return jsonify({
			'success': True,
			'movies': [movie.format() for movie in Movies.query.all()]
		})
##POST
	##post new movies
	@app.route('/movies', methods=['POST'])
	@requires_auth('post:movies')
	def post_movies(payload):
		try:
			new = request.get_json()
			title = new.get('title')
			release_date = new.get('release_date')
			new_movie = Movies(title=title,release_date=release_date)
			new_movie.insert()
			return jsonify({
				'success': True,
				'new_movie': new_movie.format()
			}),200
		except:
			return jsonify({
					"success": False,
					"error": 422,
					"message": "bad request"
					})
	##post new actors
	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actors')
	def post_actors(payload):
		try:
			new = request.get_json()
			name = new.get('name')
			age = new.get('age')
			gender = new.get('gender')
			if name == None:
				return jsonify({
					"success": False,
					"error": 404,
					"message": "resource not found"
					})
			new_actor = Actors(name=name,age=age,gender=gender)
			new_actor.insert()
			return jsonify({
				'success': True,
				'new_actor': new_actor.format()
			}),200
		except:
			return jsonify({
					"success": False,
					"error": 422,
					"message": "bad request"
					})

##PATCH
	##patch new movies
	@app.route('/movies/<int:id>', methods=['PATCH'])
	@requires_auth('patch:movies')
	def patch_movies(payload,id):
		try:
			new = request.get_json()
			movie = Movies.query.filter(Movies.id == id).one_or_none()
			if not movie:
				return jsonify({
					"success": False,
					"error": 404,
					"message": "resource not found"
					})
			movie.title = new.get('title')
			movie.release_date = new.get('release_date')
			movie.update()
			return jsonify({
				'success': True,
				'new_movie': movie.format()
			})
		except:
			return jsonify({
					"success": False,
					"error": 422,
					"message": "bad request"
					})
	##patch new movies
	@app.route('/actors/<int:id>', methods=['PATCH'])
	@requires_auth('patch:actors')
	def patch_actors(payload,id):
		try:
			new = request.get_json()
			actor = Actors.query.filter(Actors.id == id).one_or_none()
			if not actor:
				return jsonify({
					"success": False,
					"error": 404,
					"message": "resource not found"
					})
			actor.name = new.get('name')
			actor.age = new.get('age')
			actor.gender = new.get('gender')
			actor.update()
			return jsonify({
				'success': True,
				'new_actor': actor.format()
			}),200
		except:
			return jsonify({
					"success": False,
					"error": 422,
					"message": "bad request"
					})
##DELETE
	##delete movies
	@app.route('/movies/<int:id>', methods=['DELETE'])
	@requires_auth('delete:movies')
	def delete_movies(payload,id):
		movie = Movies.query.filter(Movies.id == id).one_or_none()
		if movie == None:
			return jsonify({
					"success": False,
					"error": 404,
					"message": "resource not found"
					}),404
		try:
			movie.delete()
			return jsonify({
				'success': True
				})
		except:
			return jsonify({
					"success": False,
					"error": 422,
					"message": "bad request"
					})
	# return appa
	##delete actors
	@app.route('/actors/<int:id>', methods=['DELETE'])
	@requires_auth('delete:actors')
	def delete_actors(payload,id):
		actor = Actors.query.filter(Actors.id == id).one_or_none()
		if actor == None:
			return jsonify({
					"success": False,
					"error": 404,
					"message": "resource2313 not found"
					}),404
		try:
			actor.delete()
			return jsonify({
				'success': True
				})
		except:
			return jsonify({
					"success": False,
					"error": 422,
					"message": "bad request"
					}),422
	return app
##ERROR

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
		"success": False,
		"error": 404,
		"message": "resource not found"
		}), 404
	@app.errorhandler(422)
	def bad_request(error):
		return jsonify({
		"success": False,
		"error": 422,
		"message": "bad request"
		}), 422
	return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)