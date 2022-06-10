from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    game_info = {"gameId": game_id, "board": game.board}

    return jsonify(game_info)

@app.post("/api/score-word")
def score_word():
    """Takes a json{game ID, word}, checks if a legal word, returns json"""
    word = request.json['word'].upper()
    print(word)

    game_id = request.json['game_id']
    game = games[game_id]
    print(game.word_list)

    if not game.is_word_in_word_list(word) or not game.is_word_not_a_dup(word):
        return jsonify({"result": "not-word"})
    elif not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "ok"})