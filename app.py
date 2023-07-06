import os
from flask import Flask, request, abort, jsonify, redirect
from models import setup_db, Actor, Movie
from flask_cors import CORS

from auth import AuthError, requires_auth, API_AUDIENCE, AUTH0_DOMAIN, get_token_auth_header


ENTRIES_PER_PAGE=10
CLIENT_ID='m1RP1nN8mRlUBRG5UtL9kwVmEU1YkETs'

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    CORS(app)
    # CORS Headers - Setting access control allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    def get_error_message(error, default):
      try:
          return error.description['message']
      except:
          return default
    
    def paginate_results(request, selection):
        '''Paginates and formats database queries

        Parameters:
        * <HTTP object> request, that may contain a "page" value
        * <database selection> selection of objects, queried from database
        
        Returns:
        * <list> list of dictionaries of objects, max. 10 objects

        '''
        # Get page from request. If not given, default to 1
        page = request.args.get('page', 1, type=int)
        
        # Calculate start and end slicing
        start =  (page - 1) * ENTRIES_PER_PAGE
        end = start + ENTRIES_PER_PAGE

        # Format selection into list of dicts and return sliced
        objects_formatted = [object_name.format() for object_name in selection]
        return objects_formatted[start:end]
    
    '''
    LOGIN AND LOGOUT ENDPOINTS TO CHANGE ROLES
    '''
    @app.route('/login')
    def login():
        return redirect('https://' + AUTH0_DOMAIN + '/authorize?audience=' + API_AUDIENCE + '&response_type=token&client_id=' + CLIENT_ID + '&redirect_uri=' + request.host_url + 'login-results')
    # Here we're using the /callback route.
    @app.route('/login-results')
    def callback_handling():
        auth = get_token_auth_header()
        print(auth)
        return "Logged in"    
    @app.route('/logout')
    def logout():
        return redirect('https://' + AUTH0_DOMAIN + '/v2/logout?audience=' + API_AUDIENCE + '&client_id=' + CLIENT_ID + '&returnTo=' + request.host_url + 'logout-results')    
    @app.route('/logout-results')
    def loggedout():
        return "Logged out"   

    """
    FINISHED LOGIN
    """
    
    
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        paginate_actors = paginate_results(request, actors)
        
        if len(paginate_actors) == 0 :
            abort (404, {"message" : "No actors found!"})
        
        return jsonify({
            'success': True,
            'actors': paginate_actors
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        
        if not body:
            abort(400, {"message" : "No valid JSON body!"})

        
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get ('gender', 'Other')
        movie = body.get ('movie_id', None)

        if not name:
            abort(422, {'message': 'no name provided.'})
        
        if not movie:
            abort(422, {'message': 'no movie provided.'})   
                    
        
        if not age:
            abort(422, {'message': 'no age provided.'})
        
        actor = Actor(name = name, age = age, gender = gender, movie_id=movie)
        actor.insert()
        
        return jsonify({
            'success': True,
            'created' : actor.id
        })
     
            
    @app.route('/actors/<actor_id>', methods = ['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        body = request.get_json()
        if not body:
            abort(400, {"message" : "No valid JSON body!"})
        if not actor_id:
            abort(400, {"message" : "No actor id provided!"})
        
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        
        if not actor:
            abort(404, {'message': "Actor not found on DB!"})

        actor.name = body.get('name', actor.name)
        actor.age = body.get('age', actor.age)
        actor.gender = body.get('gender', actor.gender)
        actor.movie_id = body.get('movie_id', actor.movie_id)

        actor.update()
        
        return jsonify({
            'success': True,
            'updated': actor.id,
            'actor' : [actor.format()]
            })
    
    @app.route('/actors/<actor_id>', methods = ['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):

        if not actor_id:
            abort(400, {"message" : "No actor id provided!"})
        
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
 
        if not actor:
            abort(404, {'message': 'Actor not found in database.'.format(actor_id)})
            
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })
    
    #----------------------------------------------------------------------------#
    # Endpoint /movies GET/POST/DELETE/PATCH
    #----------------------------------------------------------------------------#
    
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        paginate = paginate_results(request, movies)
        
        if len(paginate) == 0:
            abort(404, {'message': 'no movies found in database.'})
            
        return jsonify({
            'success': True,
            'movies': paginate
        })
    
    @app.route('/movies', methods = ['POST'])
    @requires_auth('post:movies')    
    def create_movie(payload):
        body = request.get_json()
        
        title = body.get('title', None)
        date = body.get('release_date', None)
        
        if not title or not date:
            abort(422, {'message':'Missing information'})
        
        movie = Movie(title=title, release_date=date)
        
        movie.insert()
        
        return jsonify({
            'success': True,
            'created':movie.id
        })
        
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(payload, movie_id):
        body = request.get_json()
        
        if not movie_id:
            abort(400, {'message': 'please append an movie id to the request url.'})

        if not body:
            abort(400, {'message': 'request does not contain a valid JSON body.'})
        
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        
        if not movie:
            abort(404, {"message": "Movie not found in database."})
        
        title = body.get('title', movie.title)
        date = body.get('release_date', movie.release_date)
        
        movie.title = title
        movie.release_date = date
        
        movie.update()
        
        return jsonify({
            'success': True,
            'edited':movie.id,
            'movie': [movie.format()]
        })
        
    @app.route('/movies/<movie_id>', methods = ['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        
        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        if not movie:
            abort(404, {"message": "Movie not found in database."})
        
        movie.delete()
        
        return jsonify({
            'success':True,
            'deleted': movie_id
        })       
    
 ## ERROR HANDLERS
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": get_error_message(error,"unprocessable")
                        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": get_error_message(error, "bad request")
                        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": get_error_message(error, "resource not found")
                        }), 404

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError): 
        return jsonify({
                        "success": False, 
                        "error": AuthError.status_code,
                        "message": AuthError.error['description']
                        }), AuthError.status_code

    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()