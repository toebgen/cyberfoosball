from flask import render_template, flash, redirect
from app import app
from .models import User


@app.route('/')
@app.route('/index')
def index():
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
