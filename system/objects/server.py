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
        """
        Convert this server into a dict
        :returns dict
        """

        d = {'ID': self.ID, 'name': self.name, 'users': [], 'rooms': []}

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
        """
        Send a message in this room
        :params message: str
        :returns None
        """

        if len(self.messages) >= 300:
            self.messages.remove(self.messages[0])

        self.messages.append(message)

    def get_messages(self, length: int):
        """
        Get the new messages since last update
        :params length: int
        :returns list(dict)
        """

        new_messages = []

        for i in range(length, len(self.messages)):
            new_messages.append(self.messages[i].to_dict())

        return new_messages

    def to_dict(self):
        """
        Convert this room into a dict
        :returns dict
        """

        d = {'ID': self.ID, 'name': self.name, 'messages': []}

        for m in self.messages:
            d['messages'].append(m.to_dict())

        return d
