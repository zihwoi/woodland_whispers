class Character:
    def __init__(self, name, location, ascii_art, dialogue):
        self.name = name
        self.location = location
        self.ascii_art = ascii_art
        self.dialogue = dialogue
        self.wants_item = None
        self.special_dialogue = ""
        self.gives_item = None
        self.consumes_item = False

    def set_wants_item(self, item, special_dialogue, gives=None, consumes=True):
        self.wants_item = item
        self.special_dialogue = special_dialogue
        self.gives_item = gives
        self.consumes_item = consumes