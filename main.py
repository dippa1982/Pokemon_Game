import random
import time
import os
import csv
import sys
from Pokemon import Pokemon_Character

inventory = {
            #Pokeballs
            'Pokeball': 3,
            #Potions  
            'Small Potion': 1, 
            'Medium Potion': 0, 
            'Large Potion': 0
            }

def clear_screen():
    os.system('cls')

def print_letter_by_letter(text, delay=0.05):
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)
    print()
        
def load_pokemon_csv(filepath):
    pokemon_list = []
    with open(filepath,mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Pokemon']
            id = row['Nat']
            type = row['Type I']
            health = int(row['HP'])
            attack = int(row['Atk'])
            defence = int(row['Def'])
            SpA = int(row['SpA'])
            SpD = int(row['SpD'])
            SpE = int(row['Spe'])
            move1 = row['Move1']
            move2 = row['Move2']
            move3 = row['Move3']
            move4 = row['Move4'] 
            
            if not any(pokemon.name == name for pokemon in pokemon_list):
                pokemon = Pokemon_Character(name,id,1,health,attack,defence,type,SpA,SpD,SpE,move1,move2,move3,move4)
                pokemon_list.append(pokemon)
    return pokemon_list

def print_player_details(player_pokemon):
    details = (
        f"Name: {player_pokemon.name}\n"
        f"Type: {player_pokemon.type}\n"
        f"Level: {player_pokemon.level}\n"
        f"Health: {player_pokemon.health}\n"
        f"Attack: {player_pokemon.attack}\n"
        f"Defence: {player_pokemon.defence}\n"
        f"Special Attack: {player_pokemon.SpA}\n"
        f"Special Defence: {player_pokemon.SpD}\n"
    )
    return details

def choose_pokemon(pokemon_list):    
    starter_pokemon = [pokemon for pokemon in pokemon_list if pokemon.name in ['Charmander', 'Pikachu', 'Squirtle']]
    
    if starter_pokemon:
        clear_screen()
        print_letter_by_letter('Choose your Pokémon:')
        for idx, pokemon in enumerate(starter_pokemon, start=1):
            print_letter_by_letter(f"{idx}: {pokemon.name}: {pokemon.type}")

    while True:
        try:
            option = int(input('Enter the number you wish to capture: '))
            if 1 <= option <= len(starter_pokemon):
                selected_pokemon = starter_pokemon[option - 1]
                clear_screen()
                details = print_player_details(selected_pokemon)
                print_letter_by_letter(details)
                return selected_pokemon 
            else:
                print("Invalid option, please choose 1, 2, or 3.")
        except ValueError:
            print("Invalid input, please enter a number.")

def choose_starter_opponent(starter_pokemon):
    while True:
        opponent_name = random.choice(starter_pokemon)
        for pokemon in game.pokemon_list:
            if pokemon.name == opponent_name:
                print_letter_by_letter(f"A wild {pokemon.name} appeared!")
                details = print_player_details(pokemon)
                print_letter_by_letter(details)
                return pokemon

def display_health_bar(pokemon):
    bar_length = 20
    health_ratio = pokemon.health / pokemon.max_health
    filled_length = int(bar_length * health_ratio)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f"{pokemon.name}: |{bar}| {pokemon.health}/{pokemon.max_health}")

def player_ability_menu(player_pokemon, opponent_pokemon,type_advantage,type_disadvantage):
    abilities = player_pokemon.abilities
    for idx, ability in enumerate(abilities, start=1):
        print_letter_by_letter(f"{idx}: {ability}")
    try:
        choose_ability = int(input('Choose Your Ability: '))
            
        if 1 <= choose_ability <= len(abilities):
            selected_ability = abilities[choose_ability - 1]
                
            player_pokemon.use_ability(opponent_pokemon, selected_ability,type_advantage,type_disadvantage)
            display_health_bar(opponent_pokemon)
                
            if opponent_pokemon.health <= 0:
                print_letter_by_letter(f"{opponent_pokemon.name} has fainted!")
        else:
            print("Invalid choice, please select a valid ability.")
        
    except ValueError:
        print("Invalid input, please enter a number.")

    return False

def opponent_ability_menu(opponent_pokemon, player_pokemon, type_advantage, type_disadvantage):
    abilities = opponent_pokemon.abilities
    choose_ability = random.randint(1, len(abilities))
    selected_ability = abilities[choose_ability - 1]
    opponent_pokemon.use_ability(player_pokemon, selected_ability, type_advantage, type_disadvantage)
    display_health_bar(player_pokemon)

    if player_pokemon.health <= 0:
        print_letter_by_letter(f"{player_pokemon.name} has fainted!")
        if player_pokemon in game.stored_pokemon:
            game.stored_pokemon.remove(player_pokemon)
        if len(game.stored_pokemon) < 1:
            print_letter_by_letter("No More Pokemon, Game Over")
            return True
        return False

def attack_menu(player_pokemon, opponent_pokemon, type_advantage, type_disadvantage, starter_pokemon):
    while player_pokemon.health > 0:
        print_letter_by_letter("\nYour options:")
        menu = ['Attack', 'Check Stored Pokemon', 'Use Item', 'Catch with Pokeball', 'Run']
        for idx, option in enumerate(menu, start=1):
            print_letter_by_letter(f"{idx}: {option}")
        choose = int(input("Enter your option: "))
        
        if choose == 1:
            if player_pokemon.health > 0:
                clear_screen()
                print_letter_by_letter("Your options:")
                player_ability_menu(player_pokemon, opponent_pokemon, type_advantage, type_disadvantage)
                if opponent_pokemon.health <= 0:
                    player_pokemon.xp += random.randint(10,50)
                    print_letter_by_letter(f"{player_pokemon.name} gained {player_pokemon.xp} XP!")
                    if player_pokemon.xp >= player_pokemon.xp_to_level:
                        player_pokemon.level_up()
                        print_letter_by_letter(f"{player_pokemon.name} has leveled up to level {player_pokemon.level}!")
                        print_letter_by_letter(f"{player_pokemon.name}'s stats have increased!")
                        print_letter_by_letter(f"Health: {player_pokemon.max_health}")
                        print_letter_by_letter(f"Attack: {player_pokemon.attack}")
                        print_letter_by_letter(f"Defence: {player_pokemon.defence}")
                        print_letter_by_letter(f"Special Attack: {player_pokemon.SpA}")
                        print_letter_by_letter(f"Special Defence: {player_pokemon.SpD}")
                    new_opponent = choose_starter_opponent(starter_pokemon)
                    if new_opponent:
                        opponent_pokemon = new_opponent
                        attack_menu(player_pokemon, opponent_pokemon, type_advantage, type_disadvantage, starter_pokemon)
                    else:
                        print_letter_by_letter("No more opponents left. You win!")
                        return
                if opponent_pokemon and opponent_pokemon.health > 0:
                    opponent_ability_menu(opponent_pokemon, player_pokemon, type_advantage, type_disadvantage)

        elif choose == 2:
            check_stored_pokemon()
        
        elif choose == 3:
            clear_screen()
            use_item(player_pokemon)
            if opponent_pokemon.health > 0:
                opponent_ability_menu(opponent_pokemon, player_pokemon, type_advantage, type_disadvantage)
        
        elif choose == 4:
            clear_screen()
            if catch_pokemon(opponent_pokemon):
                return True
            if opponent_pokemon.health > 0:
                opponent_ability_menu(opponent_pokemon, player_pokemon, type_advantage, type_disadvantage)
        
        elif choose == 5:
            clear_screen()
            print_letter_by_letter("You ran away from the battle!")
            new_opponent = choose_starter_opponent(starter_pokemon)
            if new_opponent:
                opponent_pokemon = new_opponent
        else:
            print("Invalid choice, try again.")

def use_item(pokemon):
    heal_items = {
        'Small Potion': {'cost': 50, 'health_increase': 20},
        'Medium Potion': {'cost': 100, 'health_increase': 50},
        'Large Potion': {'cost': 200, 'health_increase': 100}
    }
    
    menu = ['Potion']
    for idx, option in enumerate(menu, start=1):
        print_letter_by_letter(f"{idx}: {option}")    
    choice = int(input("What would you like to use? "))
    
    if choice == 1:
        for idx, item in enumerate(heal_items.keys(), start=1):
            print_letter_by_letter(f"{idx}. {item} (x{inventory[item]})")  # Show available quantities
        selected_item = int(input("Enter your item number: "))
        
        if selected_item in [1, 2, 3]:
            item_name = list(heal_items.keys())[selected_item - 1]
            if inventory[item_name] > 0:
                heal_amount = heal_items[item_name]['health_increase']
                print_letter_by_letter(f'You used {item_name}, healing {heal_amount} HP.')
                pokemon.health = min(pokemon.health + heal_amount, pokemon.max_health)
                inventory[item_name] -= 1  # Deduct the item from inventory
                print_letter_by_letter(f'{pokemon.name} now has {pokemon.health}/{pokemon.max_health} HP.')
            else:
                print_letter_by_letter(f'You have no {item_name} left!')

def catch_pokemon(opponent_pokemon):
    if inventory['Pokeball'] > 0:  # Check for available Pokéballs
        if opponent_pokemon.health < 20:  
            catch_rate = random.randint(1, 100)
            if catch_rate <= 50:  
                print_letter_by_letter(f'You caught {opponent_pokemon.name}!')
                game.stored_pokemon.append(opponent_pokemon)
                inventory['Pokeball'] -= 1  # Deduct the Pokéball from inventory
                return True
            else:
                print_letter_by_letter(f'{opponent_pokemon.name} escaped!')
        else:
            print_letter_by_letter(f'{opponent_pokemon.name} is too strong to catch. Weaken it more!')
    else:
        print_letter_by_letter('No Pokéballs in inventory')

def check_stored_pokemon():
    clear_screen()
    print_letter_by_letter('Your Stored Pokemon are: ')
    for pokemon in game.stored_pokemon:
        print_letter_by_letter(f"{pokemon.name}: {pokemon.type}")

class Game:
    def __init__(self):
        self.stored_pokemon = []
        self.first_run = True
        self.pokemon_list = load_pokemon_csv('data/Pokemon_data.csv')

    def run(self):
        if self.first_run:
            selected_pokemon = choose_pokemon(self.pokemon_list)
            self.stored_pokemon.append(selected_pokemon)
            self.first_run = False
        else:
            selected_pokemon = self.stored_pokemon[0]
        #Check if level up
        if selected_pokemon.xp > 100:
            selected_pokemon.level_up()
        #Load type advantages
        type_advantage, type_disadvantage = Pokemon_Character.load_type_advantages('data/Effective_Against.csv','data/Not_Effective_Against.csv')
        #Load Evo Data
        evolution_data = 'data\Evo_data.csv'
        starter_pokemon, first_evo, second_evo = Pokemon_Character.evolution_data(evolution_data)
        if not starter_pokemon:
            print("No starter Pokémon found in the data file.")
            return
        # Choose the opponent's Pokémon
        if selected_pokemon.level < 10:
            opponent_pokemon = choose_starter_opponent(starter_pokemon)
        elif selected_pokemon.level >= 10 and selected_pokemon.level < 20:
            opponent_pokemon = choose_starter_opponent(first_evo)
        elif selected_pokemon.level >= 20:
            opponent_pokemon = choose_starter_opponent(second_evo)
        # Fight each other
        if opponent_pokemon:
            attack_menu(selected_pokemon, opponent_pokemon, type_advantage, type_disadvantage, starter_pokemon)

if __name__ == "__main__":
    running = True
    game = Game()
    while running:
        running = game.run()
