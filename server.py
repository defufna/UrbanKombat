import bottle
import os
import ud
import threading
import random

bottle.debug(True)

class SessionManager:
    def __init__(self):
        self.sessions = set()
        self.lock = threading.Lock()
    
    @ud.synchronized
    def create_session(self):
        id = 0
        while True:
            id = random.randrange(0, 2**128)
            if id not in self.sessions:
                break

        self.sessions.add(id)
        return id

    @ud.synchronized
    def __contains__(self, id):
        return id in self.sessions

games = ud.GameCollection()
sessions = SessionManager()

def session(func):
    def wrapper(*args, **kwargs):
        global sessions
        session = None
        cookie = bottle.request.get_cookie("session")
    
        if cookie and int(cookie) in sessions:
            session = int(cookie)
        
        if session is None:
            session = sessions.create_session()
            bottle.response.set_cookie("session", str(session), path="/")

        return func(session, *args, **kwargs)

    return wrapper

def get_game(func):
    def wrapper(session, id, *args, **kwargs):
        global games
        id = int(id, 16)

        game = games.try_get(id)

        if game is None:
            return bottle.abort(404, "This game does not exist on server")
        
        return func(session, game, *args, **kwargs)

    return wrapper


@bottle.route("/")
@bottle.view("create_game")
def create_game_form():
    return {}

import time

@bottle.get("/<id>")
@bottle.post("/<id>/create_char")
@session
@get_game
def create_char(session, game):
    start = time.time()
    try:
        player = game.try_get(session)
        if player is not None:
            return bottle.redirect("/{:x}/lobby".format(game.id))

        if bottle.request.method == "GET":            
            return bottle.template("create_char_page", game=game)
        
        if bottle.request.method == "POST":
            form = bottle.request.forms
            team = form.get("team")
            if team is None:
                return bottle.abort(500, "Missing team id")
            if team not in game.teams:
                return bottle.abort(500, "Invalid team")

            name = form.get("char_name")
            char_cls = form.get("cls")

            player = None

            try:
                player = game.create_player(name, char_cls, session, team)
            except ValueError as e:
                return bottle.abort(500, e.args[0])
        
            return bottle.redirect("/{:x}/lobby".format(game.id))
    finally:
        print(time.time() - start)


@bottle.post("/create")
@session
def create_game(session):
    global games
    form = bottle.request.forms
    game_name = form.get("game_name")
    name = form.get("char_name")
    char_cls = form.get("cls")
    game = None
    
    try:
        game = games.create_game(game_name, name, char_cls, session)
    except ValueError as e:
        return bottle.abort(500, e.args[0])
    
    return bottle.redirect("/{:x}/lobby".format(game.id))

@bottle.route("/<id>/lobby")
@bottle.view("lobby")
@session
@get_game
def lobby(session, game):
    player = game.try_get(session)
    state = game.state
    
    if player is None: 
        if state == ud.WAITING:
            return bottle.redirect("/{:x}".format(game.id))
        else:
            return bottle.abort(500, "This game has already started and can't be joined")

    if state != ud.WAITING:
        return bottle.redirect("/{:x}/map.cgi".format(game.id))

    state_str, ready, player_count = game.status
    return {"player":player, "game":game, 
            "state":state_str, "ready": ready, "player_count":player_count,
            "host":player is game.host,
            "server_name": "://".join(bottle.request.urlparts[:2])}

@bottle.route("/<id>/map.cgi", method=["GET", "POST"])
@bottle.view("map") 
@session
@get_game
def game(session, game):
    action = None
    target = None
    if bottle.request.method == "POST":
        if len(bottle.request.query) > 0:
            item = next((key for key in bottle.request.query.keys() if key.startswith("use")), None)
            if item is not None:
                action = ud.Action(ud.USE, item)
        elif "weapon" in bottle.request.forms:
            action = ud.Action(ud.ATTACK, bottle.request.forms["weapon"])
        
        if "target" in bottle.request.forms:
            target = bottle.request.forms["target"]
    
    try:
        result = game.do(session, action, target)
        if result.finished:
            return bottle.redirect("report")
        else:
            return result.template_dict
    except ValueError as e:
        return bottle.abort(500, e.args[0])    


@bottle.route("/<id>/report")
@bottle.view("report")
@session
@get_game
def report(session, game):
    if game.state != ud.FINISHED:
        return bottle.abort(500, "This game is not finished")

    result = {"name":game.name}

    player = game.try_get(session)

    status = game.victory_status
    title = None

    if status.result == ud.DRAW:
        title = "It was a draw"
    elif player is not None:
        assert status.result == ud.VICTORY
        title = "You have {}.".format("won" if player.team == status.team else "lost")
    else:
        title = "Team {} has won".format(status.team)

    result['title'] = title
    result["events"] = [event.format_spectator() for event in game.events]
    return result

@bottle.post("/<id>/ready")
@session
@get_game
def ready(session, game):
    try:
        game.player_ready(session)
    except ValueError as e:
        return bottle.abort(500, e.args[0])

    return bottle.redirect("lobby")

@bottle.post("/<id>/kick")
@session
@get_game
def kick(session, game):
    if "player_id" not in bottle.request.forms:
        return bottle.abort(500, "Player to kick is not specified")

    player_id = bottle.request.forms["player_id"]
    try:
        game.player_kick(session, player_id)
    except ValueError as e:
        return bottle.abort(500, e.args[0])

    return bottle.redirect("lobby")

@bottle.get("/<id>/status")
@session
@get_game
def status(session, game):
    bottle.response.content_type = "application/json"
    status = game.status
    return "[\"{}\", {}, {}]".format(*status)

@bottle.error(404)
@bottle.error(500)
@bottle.view("error")
def display_error(error):
    return {"request":bottle.request, "e":error, "DEBUG":bottle.DEBUG} 

@bottle.route("/static/<filename>")
def serve_static(filename):
    return bottle.static_file(filename, root=os.path.abspath("./static"))

def main():
    bottle.run(host="0.0.0.0")

if __name__ == "__main__":
    main()
