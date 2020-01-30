from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, send, join_room
import eventlet

from pokemon_battles import config
from pokemon_battles.domain import commands
from pokemon_battles.service_layer import messagebus, unit_of_work

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*', message_queue=config.get_redis_uri())

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_team', methods=['POST'])
def add_team():
    cmd = commands.AddTeam(request.json['name'])
    uow = unit_of_work.UnitOfWork()
    messagebus.handle(cmd, uow)
    return jsonify({'status': 'OK'}), 201


@app.route('/add_pokemon', methods=['POST'])
def add_pokemon():
    cmd = commands.AddPokemonToTeam(
        request.json['team_name'],
        request.json['nickname'],
        request.json['species'],
        request.json['level'],
        request.json['moves'],
    )
    uow = unit_of_work.UnitOfWork()
    messagebus.handle(cmd, uow)
    return jsonify({'status': 'OK'}), 200


@app.route('/host_battle', methods=['POST'])
def host_battle():
    cmd = commands.HostBattle(
        request.json['team_name'],
    )
    uow = unit_of_work.UnitOfWork()
    battle_ref = messagebus.handle(cmd, uow)
    return jsonify({'battle_ref': battle_ref}), 201


@app.route('/join_battle', methods=['POST'])
def join_battle():
    cmd = commands.JoinBattle(
        request.json['battle_ref'],
        request.json['team_name'],
    )
    uow = unit_of_work.UnitOfWork()
    battle_ref = messagebus.handle(cmd, uow)
    return jsonify({'status': 'OK'}), 200


@app.route('/battle/<ref>', methods=['GET'])
def get_battle(ref):
    uow = unit_of_work.UnitOfWork()
    with uow:
        battle = uow.battles.get(ref)
    return jsonify(battle.to_dict()), 200


@app.route('/battle/<ref>/actions', methods=['GET'])
def get_actions(ref):
    uow = unit_of_work.UnitOfWork()
    player = request.args.get('player')
    with uow:
        battle = uow.battles.get(ref)

    moves = battle.get_possible_moves(player)
    pokemons = battle.get_inactive_pokemons(player)
    return jsonify({'moves': moves, 'pokemons': pokemons}), 200


@app.route('/register_a_move', methods=['POST'])
def register_a_move():
    cmd = commands.RegisterUseMove(
        request.json['battle_ref'],
        request.json['player'],
        request.json['move_name'],
    )
    uow = unit_of_work.UnitOfWork()
    battle_ref = messagebus.handle(cmd, uow)
    return jsonify({'status': 'OK'}), 200


@app.route('/register_a_pokemon_change', methods=['POST'])
def register_a_pokemon_change():
    cmd = commands.RegisterChangePokemon(
        request.json['battle_ref'],
        request.json['player'],
        request.json['pokemon_nickname'],
    )
    uow = unit_of_work.UnitOfWork()
    battle_ref = messagebus.handle(cmd, uow)
    return jsonify({'status': 'OK'}), 200


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
