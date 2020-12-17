class Message:
    def __init__(self, sender, content, hour, url=""):
        self.sender = sender
        self.content = content
        self.hour = hour
        self.url = url

    def to_dict(self):
        """
        Convert this message into a dict
        :returns dict
        """

        return {'sender': self.sender.to_dict(), 'content': self.content, 'hour': self.hour, 'url': self.url}


class User:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

    def to_dict(self):
        """
        Convert this user into a dict
        :returns dict
        """

        return {'ID': self.ID, 'name': self.name}
