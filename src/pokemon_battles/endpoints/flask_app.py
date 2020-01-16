from flask import Flask, render_template
from flask_socketio import SocketIO, send, join_room
import eventlet

from pokemon_battles import config

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*', message_queue=config.get_redis_uri())

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    print('Connected')
    send('Connected')


@socketio.on('join')
def on_join(message):
    print('Joining a room')
    join_room(message['room'])


@socketio.on('disconnect')
def test_disconnect():
    print('Disconnected')
    send('Disconnected')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    send('received message: ' + message)
