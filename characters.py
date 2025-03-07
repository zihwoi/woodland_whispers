from colorama import Fore

from game_engine import play_sound


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
        self.topics = {}  # Dictionary for conversation topics
        self.mood = "neutral"  # Character's mood
        self.met_before = False  # Whether player has met character

    def set_wants_item(self, item, special_dialogue, gives=None, consumes=True):
        self.wants_item = item
        self.special_dialogue = special_dialogue
        self.gives_item = gives
        self.consumes_item = consumes
        
    def add_topic(self, topic_name, response):
        self.topics[topic_name.lower()] = response
        

def talk_to_character(self, character_name):
    char_found = None
    for char in self.characters.values():
        if char.name.lower() == character_name.lower() and char.location == self.player_location:
            char_found = char
            break
            
    if char_found:
        print(f"\n{char_found.ascii_art}")
        
        # First meeting
        if not char_found.met_before:
            print(f"{Fore.YELLOW}{char_found.name} says: \"{char_found.dialogue}\"")
            char_found.met_before = True
            # Show available topics
            if char_found.topics:
                print(f"\nYou can ask {char_found.name} about: {', '.join(char_found.topics.keys())}")
            print("\nType 'ask [character] about [topic]' to learn more.")
        else:
            print(f"{Fore.YELLOW}{char_found.name} greets you again.")
            # Show available topics
            if char_found.topics:
                print(f"\nYou can ask {char_found.name} about: {', '.join(char_found.topics.keys())}")
        
        # Special dialogue if character wants an item and player has it
        if char_found.wants_item and char_found.wants_item in self.player_inventory:
            print(f"{Fore.GREEN}{char_found.name} notices you have the {char_found.wants_item}!")
            print(f"{Fore.YELLOW}{char_found.name} says: \"{char_found.special_dialogue}\"")
            
            # If character gives a reward
            if char_found.gives_item:
                print(f"{Fore.GREEN}{char_found.name} gives you a {char_found.gives_item}!")
                self.player_inventory.append(char_found.gives_item)
                char_found.gives_item = None  # Remove the gift to prevent multiple gifts
                play_sound("success")  # Play success sound
            
            # Remove the wanted item from inventory if it's consumed
            if char_found.consumes_item:
                self.player_inventory.remove(char_found.wants_item)
                print(f"{Fore.CYAN}You give the {char_found.wants_item} to {char_found.name}.")
    else:
        print(f"There's no one called {character_name} here.")
        
def ask_character_about(self, character_name, topic):
    char_found = None
    for char in self.characters.values():
        if char.name.lower() == character_name.lower() and char.location == self.player_location:
            char_found = char
            break
            
    if char_found:
        if topic.lower() in char_found.topics:
            print(f"\n{char_found.ascii_art}")
            print(f"{Fore.YELLOW}{char_found.name} says: \"{char_found.topics[topic.lower()]}\"")
        else:
            print(f"{Fore.YELLOW}{char_found.name} doesn't seem to know about {topic}.")
    else:
        print(f"There's no one called {character_name} here.")

def process_command(self, command):
    cmd_parts = command.lower().split()
    if not cmd_parts:
        return

    action = cmd_parts[0]

    # Movement commands (e.g., "go north")
    if action == "go" and len(cmd_parts) > 1:
        self.move_player(cmd_parts[1])

    # Pickup command (e.g., "take key")
    elif action in ["take", "pick"] and len(cmd_parts) > 1:
        self.pick_up_item(cmd_parts[1])

    # Drop command (e.g., "drop key")
    elif action == "drop" and len(cmd_parts) > 1:
        self.drop_item(cmd_parts[1])

    # Inventory check (e.g., "inventory")
    elif action in ["inventory", "inv"]:
        self.show_inventory()

    # Talking to a character (e.g., "talk rabbit")
    elif action == "talk" and len(cmd_parts) > 1:
        self.talk_to_character(cmd_parts[1])

    # Asking a character about a topic (e.g., "ask rabbit about fox")
    elif action == "ask" and len(cmd_parts) > 3 and cmd_parts[2] == "about":
        self.ask_character_about(cmd_parts[1], cmd_parts[3])

    # Using an item (e.g., "use key")
    elif action == "use" and len(cmd_parts) > 1:
        self.use_item(cmd_parts[1])

    # Look around (e.g., "look")
    elif action == "look":
        self.describe_location()

    # Help command (e.g., "help")
    elif action == "help":
        self.show_help()

    else:
        print(f"I don't understand the command: {command}")
