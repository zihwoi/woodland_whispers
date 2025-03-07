class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = {}  # e.g., {'north': 'Forest', 'south': 'Village'}
        self.special_item = None  # Item that can be used here
        self.special_event = None  # What happens when special item is used
        self.reveal_path = None  # (direction, destination) revealed after using special item

    def add_connection(self, direction, location):
        self.connections[direction] = location

    def set_special_interaction(self, item, event_text, reveal=(None, None)):
        self.special_item = item
        self.special_event = event_text
        self.reveal_path = reveal