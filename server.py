from flask import Flask, request, Response, jsonify
import json
import sqlite3
from db import leaderboard, insert_challenges, update_challenges, insert_challenges, insert_game, create_connection, insert_users

#connection = sqlite3.connect("hoggame.db")

#cursor = connection.cursor()

app = Flask(__name__)

#html = '<h1>Welcome to my awesome application</h1>, <a href="/about">About</a><h1>'
#leaderboard = [('player A', 450), ('player B', 250)]


#	return dict(leaderboard)
#def get_leaderboard():
	#"""Query the database and return the leaderboard"""
	#query= "select from database ..."
	#return dict(leaderboard)

@app.route('/api/hog/user', methods = ['POST'])
def add_user():
    req_data = request.get_json()
    if len (req_data.keys())!=3:
        return "number of arguments is incorrect"
    elif ('name') and ('mail') and ('pwd') in req_data:
        insert_users(req_data['name'], req_data['mail'],req_data['pwd'])
        return " {} is added to the database ".format(req_data['name'])
    return ("failed because the field of the request are wrong")


@app.route('/api/hog/leaderboard')
def getleaderboard():
    """Return the list of thinketeers along with their respective scores
    """
    return jsonify(leaderboard())


@app.route('/api/hog/challenges', methods = ['POST'])
def who_challenge ():
    """ in the body of the request: we define who get challenged by whom 
    """
    try:
        req_data = request.get_json()
    except:
        return Response("{'message':'1'}", status=400, mimetype='application/json')
    #validate the number of request's fields

    if len (req_data.keys())!=3:
        return "Number of arguments is incorrect"
    elif ('player1_id') and ('player2_id') and ('status') in req_data:
        try:
            assert type(req_data["player1_id"]) == type(2)
        except:
            return 'the type of the fields is not integer'
        try: 
            assert type(req_data["player2_id"]) == type(2)
        except:
            return 'the type of the fields is not integer'
        try:
            assert (req_data["status"]) == "accept" or (req_data["status"]) =="refuse"
        except:
            return 'the value of status is not correct'
        try:
            insert_challenges(req_data["player1_id"], req_data["player2_id"], req_data["status"])
        except:
            return"the insersation is failed"
        return 'The player {} is challenging the player {}'.format(req_data["player1_id"], req_data["player2_id"])
        


@app.route('/api/hog/challenges/<int:challenge_id>', methods=['POST'])
def challenge(challenge_id):
    """In the body of the request you defined either you accept or decline the challenge
    """
    req_data = request.get_json()
    if len (req_data.keys())!=1:
        return "number of arguments is incorrect"
    elif ('status') in req_data:
        try:
            assert (req_data["status"]) == 'accept' or (req_data["status"]) == 'refuse'
        except:
            return 'the value of status is not correct'
        update_challenges(request.args.get('challenge_id'), req_data['status'] )
        return 'The updated status is {}'.format(req_data['status'])
    
    return ("request fields are wrong")


@app.route('/api/hog/game', methods=['POST'])
def game():
    req_data = request.get_json()
    #challenge_id, player1_id, player2_id, score0, score1
    if len (req_data.keys())!=5:
        return "number of arguments is incorrect"
    elif ('player1_id') and ('player2_id') and ('score0') and ('score1') and ('challenge_id') in req_data:
        try:
            assert type(req_data["player1_id"]) == type(2)
        except:
            return 'the type of the player1_id is not integer'
        try: 
            assert type(req_data["player2_id"]) == type(2)
        except:
            return 'the type of the player2_id is not integer'
        try:
            assert type(req_data["score0"]) == type(2)
        except:
            return 'the type of score0 is not integer'
        try: 
            assert type(req_data["score1"]) == type(2)
        except:
            return 'the type of score1 is not integer'
        try:
            assert type(req_data["challenge_id"]) == type(2)
        except:
            return 'the value of challenge_id is integer'

        insert_game (req_data['player1_id'],req_data['player2_id'],req_data['score0'],req_data['score1'],
        req_data['challenge_id'])
        return 'Game over! {}"s score is {} and {}"s score is {}'.format(req_data['player1_id'],
        req_data['score0'],req_data['player2_id'], req_data['score1'])

    return ("failed because the field of the request are wrong")


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=3000)