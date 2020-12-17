from flask import Flask, request, render_template, redirect, session
from objects.chat_object import Room, Message, User, Server
from random import randint
from datetime import datetime
from flask.json import jsonify

KEY = "ert65g4v1ert65g1sdqf46cvsdrgfb54bsgdf6475dsgfb78bsb698b"

app = Flask("SupRChat")
app.secret_key = KEY
app.config['SESSION_TYPE'] = 'filesystem'

servers = [Server(0, "Vegetable Official", [], [Room(0, "General", []), Room(1, "Tests", [])])]

names = ["Fraise", "Framboise", "Pomme", "Pêche",
         "Poire", "Mangue", "Mandarine", "Abricot",
         "Mirabelle", "Reine claude", "Cérise", "Raisin",
         "Figue", "Passion", "Annanas", "Banane",
         "Clémentine", "Groseille", "Courge", "Courgette",
         "Melon", "Pastèque", "Litchi", "Tomate", "Haricot",
         "Navet", "Carotte", "Radis", "Blé", "Maïs"]

too_long_messages = []

@app.route("/")
def index():
    return redirect("/chat/0")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    define_user_name()
    server, room = get_server_room_by_id(request.args['sid'], request.args['rid'])
    print(server, room)
    
    if room == None:
        return redirect("/notfound")
    
    if request.method == "GET":
        server.add_user(User(0, session['name']))
        return render_template("room.html", server=server, room=room)
    elif request.method == "POST":
        message = Message(User(0, session["name"]), request.form["text"], f"{datetime.now().hour:02}:{datetime.now().minute:02}")
        
        if len(message.content) > 0:
            if len(message.content) <= 250:
                room.send_message(message)
            else:
                too_long_messages.append(message)
                room.send_message(Message(session["name"], "[Message trop long]", f"{datetime.now().hour:02}:{datetime.now().minute:02}", f"/message/{len(too_long_messages) - 1}"))
                
        return redirect(f"/chat?sid={server.ID}&rid={room.ID}")

@app.route("/message/<ID>")
def display_message(ID):
    return render_template("msg.html", message=too_long_messages[int(ID)])

@app.route("/api/room")
def get_room():
    server, room = get_server_room_by_id(request.args['server_id'], request.args['room_id'])
    return jsonify(room.to_dict())

def get_server_room_by_id(server_id, room_id):
    global servers
    
    for s in servers:
        if s.ID == int(server_id):
            for r in s.rooms:
                if r.ID == int(room_id):
                    return s, r
            
            return s, None
    
    return None, None

def define_user_name():
    if not 'name' in session:
        modify_session('name', names[randint(0, len(names) - 1)])
        
def modify_session(var_name = '', var_value = None, is_list = False):
    if var_name != '' and var_value != None:
        if not is_list:
            session[var_name] = var_value
        else:
            session[var_name].append(var_value)

    session.modified = True

def delete_var(var_name = ''):
    if var_name != '':
        session.pop(var_name, None)

app.run(host="192.168.1.24", port=2002)
