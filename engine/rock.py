import uuid

class Rock():
    def __init__(self):
        self.id = uuid.uuid4()
        self.x = 0
        self.y = 0

    def __dict__(self):
        return { 'type': 'ROCK', 'id': self.id, 'x': self.x, 'y': self.y }