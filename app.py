from boggle import Boggle
from flask import Flask, request, jsonify, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeholder'
app.debug = True

toolbar = DebugToolbarExtension(app)
boggle_game = None
boggle_board = None

@app.route('/')
def show_home():
    """ Show homepage"""
    global boggle_game
    boggle_game = Boggle()
    global boggle_board
    boggle_board = boggle_game.make_board()
    session['board'] = boggle_board
    return render_template('home.html', boggle_game=boggle_game, boggle_board=boggle_board)

@app.route('/submit-guess', methods=['POST'])
def process_guess():
    """ Determine validity of guess """
    global boggle_game
    guess = request.json['guess']
    res = dict()
    res['Result'] = boggle_game.check_valid_word(boggle_board,guess)
    return jsonify(res)
    
@app.route('/submit-score', methods=['POST'])
def process_score():
    """ Update user's high score and attempts """
    res = {
        'is_high_score': False
    }
    score = int(request.json['score'])
    high_score = session.get('high_score',0)
    if score > high_score:
        res['is_high_score'] = True
    session['attempts'] = session.get('attempts',0) + 1
    session['high_score'] = max(high_score,score)
    return jsonify(res)
