import random
import time
import csv
from Pokemon import Pokemon_Character

inventory = {'Standard Pokeball': 3, 'Small Potion': 1}
stored_pokemon = []

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

def choose_pokemon(pokemon_list):    
    starter_pokemon = [pokemon for pokemon in pokemon_list if pokemon.name in ['Charmander', 'Pikachu', 'Squirtle']]
    
    if starter_pokemon:
        print('Choose your Pokémon:')
        for idx, pokemon in enumerate(starter_pokemon, start=1):
            print(f"{idx}: {pokemon.name}")

    while True:
        try:
            option = int(input('Enter the number you wish to capture: '))
            if 1 <= option <= len(starter_pokemon):
                selected_pokemon = starter_pokemon[option - 1]
                print(f'You have selected {selected_pokemon.name}')
                stored_pokemon.append(selected_pokemon)
                return selected_pokemon 
            else:
                print("Invalid option, please choose 1, 2, or 3.")
        except ValueError:
            print("Invalid input, please enter a number.")

def choose_opponent(pokemon_list, player_pokemon):
    opponent_options = [pokemon for pokemon in pokemon_list if pokemon != player_pokemon]
    
    if not opponent_options:
        print("No available Pokémon for the opponent.")
        return None
    
    opponent = random.choice(opponent_options)
    print(f'The opponent has selected {opponent.name}.')
    return opponent

def display_health_bar(pokemon):
    bar_length = 20
    health_ratio = pokemon.health / pokemon.max_health
    filled_length = int(bar_length * health_ratio)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f"{pokemon.name}: |{bar}| {pokemon.health}/{pokemon.max_health}")

def player_ability_menu(player_pokemon, opponent_pokemon,type_advantage,type_disadvantage):
    abilities = player_pokemon.abilities
    for idx, ability in enumerate(abilities, start=1):
        print(f"{idx}: {ability}")
    try:
        choose_ability = int(input('Choose Your Ability: '))
            
        if 1 <= choose_ability <= len(abilities):
            selected_ability = abilities[choose_ability - 1]
                
            player_pokemon.use_ability(opponent_pokemon, selected_ability,type_advantage,type_disadvantage)
            display_health_bar(player_pokemon)
                
            if opponent_pokemon.health <= 0:
                print(f"{opponent_pokemon.name} has fainted!")
                return True
        else:
            print("Invalid choice, please select a valid ability.")
        
    except ValueError:
        print("Invalid input, please enter a number.")

    return False

def opponent_ability_menu(opponent_pokemon, player_pokemon,type_advantage,type_disadvantage):
    abilities = opponent_pokemon.abilities
    choose_ability = random.randint(1, len(abilities))
    selected_ability = abilities[choose_ability - 1]   
    opponent_pokemon.use_ability(player_pokemon,selected_ability,type_advantage,type_disadvantage)
    display_health_bar(opponent_pokemon)

    if player_pokemon.health <= 0:
                print(f"{player_pokemon.name} has fainted!")
                return True

    return False

def attack_menu(player_pokemon, opponent_pokemon,type_advantage, type_disadvantage):
    while player_pokemon.health > 0 and opponent_pokemon.health > 0:
        print("\nYour options:")
        menu = ['Attack', 'Use Item', 'Catch with Pokeball', 'Run']
        for idx, option in enumerate(menu, start=1):
            print(f"{idx}: {option}")
        choose = int(input("Enter your option: "))        

        if choose == 1:
            if player_pokemon.health > 0:
                if player_ability_menu(player_pokemon, opponent_pokemon,type_advantage,type_disadvantage):
                    break
            if opponent_pokemon.health > 0:
                if opponent_ability_menu(opponent_pokemon, player_pokemon,type_advantage,type_disadvantage):
                    break
        elif choose == 2:
            use_item(player_pokemon)
            if opponent_pokemon.health > 0:
                opponent_ability_menu(opponent_pokemon, player_pokemon,type_advantage,type_disadvantage)
        elif choose == 3:
            if catch_pokemon(opponent_pokemon):
                break  
            if opponent_pokemon.health > 0:
                opponent_ability_menu(opponent_pokemon, player_pokemon,type_advantage,type_disadvantage)
        elif choose == 4:
            print("You ran away from the battle!")
            break
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
        print(f"{idx}: {option}")    
    choice = int(input("What would you like to use? "))
    
    if choice == 1:
        for idx, item in enumerate(heal_items.keys(), start=1):
            print(f"{idx}. {item} (x{inventory[item]})")  # Show available quantities
        selected_item = int(input("Enter your item number: "))
        
        if selected_item in [1, 2, 3]:
            item_name = list(heal_items.keys())[selected_item - 1]
            if inventory[item_name] > 0:  # Check if the item is available
                heal_amount = heal_items[item_name]['health_increase']
                print(f'You used {item_name}, healing {heal_amount} HP.')
                pokemon.health = min(pokemon.health + heal_amount, pokemon.max_health)
                inventory[item_name] -= 1  # Deduct the item from inventory
                print(f'{pokemon.name} now has {pokemon.health}/{pokemon.max_health} HP.')
            else:
                print(f'You have no {item_name} left!')

def catch_pokemon(opponent_pokemon):
    if inventory['Standard Pokeball'] > 0:  # Check for available Pokéballs
        if opponent_pokemon.health < 20:  
            catch_rate = random.randint(1, 100)
            if catch_rate <= 50:  
                print(f'You caught {opponent_pokemon.name}!')
                stored_pokemon.append(opponent_pokemon)
                inventory['Standard Pokeball'] -= 1  # Deduct the Pokéball from inventory
                return True
            else:
                print(f'{opponent_pokemon.name} escaped!')
        else:
            print(f'{opponent_pokemon.name} is too strong to catch. Weaken it more!')
    else:
        print('No Pokéballs in inventory')

class Game:
    def run(self):
        pokemon_list = load_pokemon_csv('Pokemon_data.csv')
        type_advantage, type_disadvantage = Pokemon_Character.load_type_advantages('Effective_Against.csv','Not_Effective_Against.csv')
        # Choose the player's Pokémon
        selected_pokemon = choose_pokemon(pokemon_list)
        # Choose the opponent's Pokémon
        opponent_pokemon = choose_opponent(pokemon_list, selected_pokemon)
        # Fight each other
        if opponent_pokemon:
            attack_menu(selected_pokemon, opponent_pokemon, type_advantage, type_disadvantage)

if __name__ == "__main__":
    game = Game()
    game.run()
