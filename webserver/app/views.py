from flask import render_template, flash, redirect, request
from app import app
from .models import User
import json


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('POST requested')
        game_status = request.json
        print(json.dumps(game_status))
    player = {'name': 'Miguel'}  # fake user
    games = [
        {
            'player': {'name': 'John'},
            'timestamp': 'Yesterday'
        },
        {
            'player': {'name': 'Susan'},
            'timestamp': 'Today'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           player=player,
                           games=games)
