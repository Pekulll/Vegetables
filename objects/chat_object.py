class Server():
    def __init__(self, ID, name, users, rooms):
        self.ID = ID
        self.name = name
        self.users = users
        self.rooms = rooms
        
    def add_user(self, user):
        if not user in self.users:
            self.users.append(user)
        
    def to_dict(self):
        d = {'ID':self.ID, 'name': self.name, 'users': [], 'rooms': []}
        
        for u in self.users:
            d['users'].append(u.to_dict())
        
        for r in self.rooms:
            d['rooms'].append(r.to_dict())
            
        return d

class Room:
    def __init__(self, ID, name, messages):
        self.ID = ID
        self.name = name
        self.messages = messages
            
    def send_message(self, message):
        if len(self.messages) >= 300:
            self.messages.remove(self.messages[0])
                
        self.messages.append(message)
            
    def __str__(self):
        return f"{self.name} at {self.ID}."
    
    def to_dict(self):
        d = {'ID':self.ID, 'name': self.name, 'messages': []}
        
        for m in self.messages:
            d['messages'].append(m.to_dict())
            
        return d
            
            
class Message:
    def __init__(self, sender, content, hour, url = ""):
        self.sender = sender
        self.content = content
        self.hour = hour
        self.url = url
        
    def to_dict(self):
        return {'sender': self.sender.to_dict(), 'content': self.content, 'hour': self.hour, 'url': self.url }
    
class User:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        
    def to_dict(self):
        return {'ID': self.ID, 'name': self.name }