from game_engine import GameEngine
from locations import Location
from characters import Character
from items import Item
import ascii_art
import time

from colorama import init, Fore, Back, Style
init(autoreset=True)  # Initialize colorama


def setup_game():
    game = GameEngine()
    
    # Create locations
    forest_clearing = Location("Forest Clearing", 
                             "A peaceful clearing surrounded by tall trees. Sunlight filters through the leaves.")
    old_oak = Location("Old Oak", 
                     "An ancient oak tree with gnarled roots. It seems to have a mysterious presence.")
    stream = Location("Babbling Stream", 
                    "A clear stream flows gently over smooth stones. The water sparkles in the light.")
    berry_bush = Location("Berry Bushes", 
                        "Bushes full of ripe berries. They look delicious!")
    hidden_grove = Location("Hidden Grove", 
                          "A secluded grove hidden away from the regular forest paths. Magic seems to linger here.")
    
    # Connect locations
    forest_clearing.add_connection("north", "Old Oak")
    forest_clearing.add_connection("east", "Babbling Stream")
    forest_clearing.add_connection("west", "Berry Bushes")
    
    old_oak.add_connection("south", "Forest Clearing")
    stream.add_connection("west", "Forest Clearing")
    berry_bush.add_connection("east", "Forest Clearing")
    
    # Set special interaction (use key at the old oak)
    old_oak.set_special_interaction("key", 
                                  "You insert the key into a small, previously unseen keyhole in the oak's trunk. " +
                                  "With a gentle click, a section of bark slides away, revealing a hidden path!", 
                                  ("north", "Hidden Grove"))
    
    hidden_grove.add_connection("south", "Old Oak")
    
    # Add locations to game
    for location in [forest_clearing, old_oak, stream, berry_bush, hidden_grove]:
        game.add_location(location)
    
    # Create characters
    rabbit = Character("Rabbit", "Forest Clearing", ascii_art.RABBIT, 
                      "Hello there! I'm looking for my special carrot. Have you seen it?")
    rabbit.set_wants_item("carrot", "Oh thank you! That's my special carrot! " +
                        "I heard the Owl talking about a key hidden by the stream...", None, True)
    
    fox = Character("Fox", "Berry Bushes", ascii_art.FOX, 
                  "These berries are quite tasty. I've been collecting them all day.")
    fox.set_wants_item("berries", "Thank you for the berries! Here, I found this shiny key earlier.", 
                     "key", True)
    
    owl = Character("Owl", "Old Oak", ascii_art.OWL, 
                  "Hoot! I've lived in this forest for 100 years. I know all its secrets.")
    
    squirrel = Character("Squirrel", "Hidden Grove", ascii_art.SQUIRREL, 
                       "You found my secret grove! Not many visitors make it here.")
    squirrel.set_wants_item("acorn", "An acorn! Thank you kind traveler. " +
                          "You've helped all the woodland creatures today. You win!", None, True)
    
    # Add characters to game
    for character in [rabbit, fox, owl, squirrel]:
        game.add_character(character)
    
    # Create items
    carrot = Item("carrot", "Babbling Stream", "A bright orange carrot. Looks delicious!")
    berries = Item("berries", "Berry Bushes", "A handful of juicy forest berries.")
    acorn = Item("acorn", "Old Oak", "A perfect acorn that fell from the old oak tree.")
    
    # Add items to game
    for item in [carrot, berries, acorn]:
        game.add_item(item)
    
    return game

def main():
    print(ascii_art.TITLE)
    print("\nA text adventure with woodland creatures")
    print("\nYou find yourself in a mystical forest where the animals can speak.")
    print("Help the woodland creatures solve their problems to win the game!")
    
    time.sleep(2)
    
    game = setup_game()
    game.run()
    
    print(ascii_art.GAME_OVER)
    print("\nThanks for playing Woodland Whispers!")
    print("A text adventure created with Python")

if __name__ == "__main__":
    main()

