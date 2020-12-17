import json
import socket

from flask import Flask, request, render_template, redirect, session
from random import randint
from datetime import datetime
from flask.json import jsonify

from system.objects.message import Message, User
from system.objects.server import Server, Room

KEY = "tsrgeh4bdgfs654s6d5g4156bf56d878f4gss5f4sd"

app = Flask("Vegetables")
app.secret_key = KEY
app.config['SESSION_TYPE'] = 'filesystem'

servers = [Server(0, "Vegetable Official", [], [Room(0, "General", [Message(User(-1, "Vegetables"), "Welcome on Vegetable! We don't know who you are, but you are NICE with people, we know this.", "System", "")]), Room(1, "Discussion", [])])]
names = None
too_long_messages = []

@app.route("/")
def index():
    return render_template("index.html", servers=servers)


@app.route("/chat", methods=["GET"])
def chat():
    define_user_name()
    server, room = get_server_room_by_id(request.args['sid'], request.args['rid'])
    
    if room == None:
        return redirect("/notfound")
    
    server.add_user(User(0, session['name']))
    return render_template("room.html", server=server, room=room)
        

@app.route("/chat", methods=["POST"])
def send_message():
    server, room = get_server_room_by_id(request.args['sid'], request.args['rid'])
    message = Message(User(0, session["name"]), request.form["text"], f"{datetime.now().hour:02}:{datetime.now().minute:02}")
        
    if len(message.content) > 0:
        if len(message.content) <= 250:
            room.send_message(message)
        else:
            too_long_messages.append(message)
            room.send_message(
                Message(
                    session["name"], "[Message trop long]",
                    f"{datetime.now().hour:02}:{datetime.now().minute:02}",
                    f"/message/{len(too_long_messages) - 1}")
                )
                
    return redirect(f"/chat?sid={server.ID}&rid={room.ID}&l={len(room.messages)}")

@app.route("/message/<ID>")
def display_message(ID):
    return render_template("msg.html", message=too_long_messages[int(ID)])

@app.route("/api/get_room")
def get_room():
    server, room = get_server_room_by_id(request.args['sid'], request.args['rid'])
    return jsonify(room.get_messages(int(request.args["l"])))

#region Methods

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

def import_config():
    global names
    
    with open("system/resources/vegetables.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        names = data['names']

#endregion

#region Session modification
   
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

#endregion

import_config()
app.run(host=socket.gethostbyname(socket.gethostname()), port=2002)
