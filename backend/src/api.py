import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth
from errors.errors import error_404, error_422, error_400, error_405, error_500, error_authError

app = Flask(__name__)
setup_db(app)
CORS(app, resources={'/': {'origins': '*'}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# https://tnmayer.eu.auth0.com/authorize?audience=fsnd_coffee_shop&response_type=token&client_id=OTyexCMUnINd1UgH3oAmZR7EhpM4R9uU&redirect_uri=http://127.0.0.1:8080/login-results

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
@app.route('/')
def api_greeting():
    return jsonify({'message':'Hello, World!'})

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET'])
def get_drinks():
    selection = Drink.query.order_by(Drink.id).all()

    if len(selection) == 0:
        abort(404)
    
    all_items = [item.short() for item in selection]

    return jsonify({
        'success': True,
        'n_drinks': len(selection),
        "drinks": all_items
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    print(jwt)
    selection = Drink.query.order_by(Drink.id).all()

    if len(selection) == 0:
        abort(404)
    
    all_items = [item.long() for item in selection]

    return jsonify({
        'success': True,
        'n_drinks': len(selection),
        "drinks": all_items
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_question(jwt):
    body = request.get_json()
    new_title = body['title']
    new_recipe = body['recipe']

    try:
        print(new_title)
        print(new_recipe)

        if isinstance(new_recipe, dict):
            new_recipe = [new_recipe]
        
        # convert recipe to string
        new_recipe = json.dumps(new_recipe)

        if ((new_title is None) or (new_recipe is None) or\
                (new_title == '') or (new_recipe == '')):
            abort(404)
        
        drink = Drink(title=new_title, recipe=new_recipe)
        drink.insert()

    except:
        abort(422)

    return jsonify({
        'success': True, 
        'drinks': [drink.long()]
    })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling
'''
Example error handling for unprocessable entity
'''
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
error_404(app)
error_422(app)
error_400(app)
error_405(app)
error_500(app)
error_authError(app, AuthError)

if __name__ == '__main__':
    # def create_app(test_config=None):
    port = int(os.environ.get('PORT', 8080))
    # app.run(ssl_context='adhoc', debug=True, use_debugger=False, host='127.0.0.1', port=port, use_reloader=True)
    app.run(debug=True, use_debugger=False, host='127.0.0.1', port=port, use_reloader=True)
