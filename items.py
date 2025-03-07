class Item:
    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description
        self.collected = False