from colorama import init, Fore, Back, Style
import pygame
import os

def play_sound(pickup):
    try:
        sound_file = os.path.join("sounds", f"{pickup}.wav")
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
    except:
        pass  # Silently fail if sound file not found 
class GameEngine:
    def __init__(self):
        self.locations = {}
        self.characters = {}
        self.items = {}
        self.player_location = None
        self.player_inventory = []
        self.game_running = True
        pygame.mixer.init()

    def add_location(self, location):
        self.locations[location.name] = location
        if self.player_location is None:
            self.player_location = location.name

    def add_character(self, character):
        self.characters[character.name] = character

    def add_item(self, item):
        self.items[item.name] = item

    def move_player(self, direction):
        current_location = self.locations[self.player_location]
        if direction in current_location.connections:
            self.player_location = current_location.connections[direction]
            self.look()
            return True
        else:
            print(f"You can't go {direction} from here.")
            return False

    def look(self):
        location = self.locations[self.player_location]
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {location.name} ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}{location.description}")
        
        # Show characters
        for char_name, char in self.characters.items():
            if char.location == self.player_location:
                print(f"\n{char.ascii_art}")
                print(f"{Fore.YELLOW}You see {char.name} here.")
        
        # Show items
        for item_name, item in self.items.items():
            if item.location == self.player_location and not item.collected:
                print(f"{Fore.GREEN}There's a {item.name} here.")
        
        # Show available directions
        print(f"\n{Fore.MAGENTA}You can go: ", end="")
        directions = list(location.connections.keys())
        if directions:
            print(", ".join(directions))
        else:
            print("nowhere else from here.")


    def take_item(self, item_name):
        item_found = None
        for item in self.items.values():
            if item.name.lower() == item_name.lower() and item.location == self.player_location and not item.collected:
                item_found = item
                break
                
        if item_found:
            item_found.collected = True
            self.player_inventory.append(item_found.name)
            print(f"You picked up the {item_found.name}.")
            play_sound("pickup")  # Play sound effect
        else:
            print(f"There's no {item_name} here to take.")

    def show_inventory(self):
        if self.player_inventory:
            print("\nYour inventory:")
            for item in self.player_inventory:
                print(f"- {item}")
        else:
            print("\nYour inventory is empty.")

    def talk_to_character(self, character_name):
        char_found = None
        for char in self.characters.values():
            if char.name.lower() == character_name.lower() and char.location == self.player_location:
                char_found = char
                break
                
        if char_found:
            print(f"\n{char_found.ascii_art}")
            print(f"{char_found.name} says: \"{char_found.dialogue}\"")
            
            # Special dialogue if character wants an item and player has it
            if char_found.wants_item and char_found.wants_item in self.player_inventory:
                print(f"{char_found.name} notices you have the {char_found.wants_item}!")
                print(f"{char_found.name} says: \"{char_found.special_dialogue}\"")
                
                # If character gives a reward
                if char_found.gives_item:
                    print(f"{char_found.name} gives you a {char_found.gives_item}!")
                    self.player_inventory.append(char_found.gives_item)
                    char_found.gives_item = None  # Remove the gift to prevent multiple gifts
                
                # Remove the wanted item from inventory if it's consumed
                if char_found.consumes_item:
                    self.player_inventory.remove(char_found.wants_item)
                    print(f"You give the {char_found.wants_item} to {char_found.name}.")
        else:
            print(f"There's no one called {character_name} here.")

    def use_item(self, item_name):
        if item_name in self.player_inventory:
            location = self.locations[self.player_location]
            if location.special_item == item_name:
                print(location.special_event)
                if location.reveal_path:
                    direction, destination = location.reveal_path
                    location.connections[direction] = destination
                    print(f"You can now go {direction}!")
                return True
            else:
                print(f"Using the {item_name} here doesn't do anything special.")
        else:
            print(f"You don't have a {item_name} to use.")
        return False

    def process_command(self, command):
        cmd_parts = command.lower().split()
        if not cmd_parts:
            return
            
        action = cmd_parts[0]
        
        # Movement commands
        if action in ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
            direction = action[0]
            if direction == 'n':
                self.move_player('north')
            elif direction == 's':
                self.move_player('south')
            elif direction == 'e':
                self.move_player('east')
            elif direction == 'w':
                self.move_player('west')
            else:
                self.move_player(action)
                
        # Look command
        elif action == 'look':
            self.look()
            
        # Take command
        elif action == 'take' and len(cmd_parts) > 1:
            self.take_item(cmd_parts[1])
            
        # Inventory command
        elif action == 'inventory' or action == 'i':
            self.show_inventory()
            
        # Talk command
        elif action == 'talk' and len(cmd_parts) > 1:
            self.talk_to_character(cmd_parts[1])
            
        # Use command
        elif action == 'use' and len(cmd_parts) > 1:
            self.use_item(cmd_parts[1])
            
        # Help command
        elif action == 'help':
            self.show_help()
            
        # Quit command
        elif action == 'quit':
            confirm = input("Are you sure you want to quit? (y/n): ")
            if confirm.lower() == 'y':
                self.game_running = False
                
        else:
            print("I don't understand that command. Type 'help' for a list of commands.")   

    def show_help(self):
        print("\n=== COMMANDS ===")
        print("- north/south/east/west: Move in that direction (or just n/s/e/w)")
        print("- look: Look around your current location")
        print("- talk [character]: Talk to a character")
        print("- take [item]: Pick up an item")
        print("- use [item]: Use an item in your inventory")
        print("- inventory (or i): Show your inventory")
        print("- help: Show this help menu")
        print("- quit: Exit the game")

    def run(self):
        print("\n" + "="*60)
        print("Welcome to Woodland Whispers!")
        print("Type 'help' for a list of commands.")
        print("="*60 + "\n")
        
        self.look()
        
        while self.game_running:
            command = input("\n> ")
            self.process_command(command)
        