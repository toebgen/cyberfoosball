from flask import render_template, flash, redirect, request, jsonify
from app import app
from .models import User
import json

game_status = {
    "home_defense": "none",
    "home_offense": "none",
    "guest_defense": "none",
    "guest_offense": "none",
    "home_goals": 0,
    "guest_goals": 0
}


@app.route('/', methods=['GET'])
def index():
    print('index() here we are')
    if not game_status:
        print('game_status has not been set yet!')
        return render_template('index.html',
                               title='Game status')
    else:
        return render_template('index.html',
                               title='Game status',
                               game_status=game_status)


@app.route('/status_update', methods=['GET', 'POST'])
# Is used by raspberry to deliver new status, as well as by web site to
# request new status
def update_status():
    global game_status
    if request.method == 'POST':
        print('POST requested')
        game_status = request.json
        print(json.dumps(game_status))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print('received some numbers:')
    print('a:%i' % a)
    print('b:%i' % b)
    return jsonify(result=a + b)


@app.route('/_periodic_update')
def periodic_update():
    i = request.args.get('i', 0, type=int)
    print('received an i: %i' % i)
    print(json.dumps(game_status))
    return jsonify(game_status)
