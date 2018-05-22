from flask import Flask, request, jsonify
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


@app.route('/api/hog/challenge', methods = ['POST'])
def who_challenge ():
    """ in the body of the request: we define who get challenged by whom 
    """
    req_data = request.get_json()
    #validate the number of request's fields 
    if len (req_data.keys())!=3:
        return "number of arguments is incorrect"
    elif ('player1_id') and ('player2_id') and ('status') in req_data:
        insert_challenges(req_data["player1_id"], req_data["player2_id"], req_data["status"])
        return 'The player {} is challenging the player {}'.format(req_data["player1_id"], req_data["player2_id"])
    
    return ("failed because the field of the request are wrong")


@app.route('/api/hog/challenges/<int:challenge_id>', methods=['POST'])
def challenge(challenge_id):
    """In the body of the request you defined either you accept or decline the challenge
    """
    req_data = request.get_json()
    if len (req_data.keys())!=1:
        return "number of arguments is incorrect"
    elif ('status') in req_data:
        #update_challenges(challenge_id, req_data['status'] )
        return '{} is {}ing the challenge {}'.format(req_data['player1_id'], req_data['decision'], challenge_id)
    return ("failed because the field of the request are wrong")


@app.route('/api/hog/game', methods=['POST'])
def game():
    req_data = request.get_json()
    #challenge_id, player1_id, player2_id, score0, score1
    if len (req_data.keys())!=5:
        return "number of arguments is incorrect"
    elif ('player1_id') and ('player2_id') and ('score0') and ('score1') and ('Challenge_id'):
        insert_game (req_data['player1_id'],req_data['player2_id'],req_data['score0'],req_data['score1'],
        req_data['challenge_id'])
        return 'Game over! {}"s score is {} and {}"s score is {}'.format(req_data['player1_id'],
        req_data['score0'],req_data['player2_id'], req_data['score1'] )
    return ("failed because the field of the request are wrong")




if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=3000)