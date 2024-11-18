import random
import csv
import os
import time
from tkinter import Toplevel, Label, Button, Tk, messagebox
from Pokemon import Pokemon_Character

def load_pokemon_csv(filepath, app_context):
    pokemon_list = []
    with open(filepath, mode='r') as file:
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
            Spe = int(row['Spe'])
            move1 = row['Move1']
            move2 = row['Move2']
            move3 = row['Move3']
            move4 = row['Move4']

            if not any(pokemon.name == name for pokemon in pokemon_list):
                pokemon = Pokemon_Character(name, id, 1, health, attack, defence, type, SpA, SpD, Spe, move1, move2, move3, move4, app_context=app_context)
                pokemon_list.append(pokemon)
    return pokemon_list

class Game():
    def __init__(self, app_context) -> None:
        super().__init__()
        self.inventory = {
            'Pokeball': 5,
            'Potion': 5,
        }
        self.app_context = app_context
        self.stored_pokemon = []
        self.first_run = True
        self.pokemon_list = load_pokemon_csv('data/Pokemon_data.csv', self.app_context)
        self.type_advantage, self.type_disadvantage = Pokemon_Character.load_type_advantages(
            'data/Effective_Against.csv', 'data/Not_Effective_Against.csv'
        )
        self.selected_pokemon = None
        self.opponent_pokemon = None

    def select_pokemon(self, pokemon, window):
        """Select a starter Pokémon and close the selection window."""
        self.selected_pokemon = pokemon
        self.stored_pokemon.append(pokemon)
        window.destroy()
        self.app_context.txt_Box_3.insert("end", f"You selected {pokemon.name}!\n")

    def choose_opponent(self):
        self.opponent_pokemon = random.choice(self.pokemon_list)
        self.app_context.txt_Box_3.insert("end",f"\nA Wild {self.opponent_pokemon.name} has appeared!")
        return self.opponent_pokemon

    def update_health_bars(self, player_pokemon, opponent_pokemon):
        """Update the health bars of the player and opponent."""
        player_health_percentage = max(0, player_pokemon.health / player_pokemon.max_health) * 200
        opponent_health_percentage = max(0, opponent_pokemon.health / opponent_pokemon.max_health) * 200

        self.app_context.player_health_canvas.config(width=player_health_percentage)
        self.app_context.cpu_health_canvas.config(width=opponent_health_percentage)

    def display_moves(self, player_pokemon, opponent_pokemon):
        """Display available moves in the attack frame."""
        for widget in self.app_context.attack_Frame.winfo_children():
            widget.destroy()

        Label(self.app_context.attack_Frame, text="Select an attack:").pack(pady=5)
        for move in player_pokemon.abilities:
            if move:
                Button(
                    self.app_context.attack_Frame,
                    text=move,
                    command=lambda m=move: self.execute_move(player_pokemon, opponent_pokemon, m)
                ).pack(pady=5)

    def start_battle(self):
        """Set up the opponent and display available moves for battle."""
        if self.selected_pokemon:
            self.opponent_pokemon = self.choose_opponent()
            self.display_moves(self.selected_pokemon, self.opponent_pokemon)

    def execute_move(self, player_pokemon, opponent_pokemon, move):
        """Execute the selected move and update health bars."""
        # Player's move
        player_pokemon.use_ability(opponent_pokemon, move, self.type_advantage, self.type_disadvantage)
        self.update_health_bars(player_pokemon, opponent_pokemon)

        if opponent_pokemon.health <= 0:
            self.app_context.txt_Box_3.insert("end",f"\n{opponent_pokemon.name} has fainted!")
            new_opponent = self.choose_opponent()
            if new_opponent:
                self.opponent_pokemon = new_opponent
                self.update_health_bars(player_pokemon, self.opponent_pokemon)
                self.display_moves(player_pokemon, self.opponent_pokemon)
            return

        # Opponent's move
        opponent_move = random.choice(opponent_pokemon.abilities)
        opponent_pokemon.use_ability(player_pokemon, opponent_move, self.type_advantage, self.type_disadvantage)
        self.update_health_bars(player_pokemon, opponent_pokemon)

        if player_pokemon.health <= 0:
            self.app_context.txt_Box_3.insert("end",f"\n{player_pokemon.name} has fainted!")
            self.choose_new_pokemon()

    def choose_new_pokemon(self):
        """Prompt the player to select a new Pokémon if one is available."""
        if len(self.stored_pokemon) > 1:
            new_window = Toplevel(self.app_context)
            new_window.title("Choose New Pokémon")
            new_window.geometry("300x300")
            
            Label(new_window, text="Your Pokémon has fainted! Choose another:").pack(pady=10)
            for pokemon in self.stored_pokemon[1:]:  # Exclude the fainted Pokémon
                Button(
                    new_window,
                    text=pokemon.name,
                    command=lambda p=pokemon: self.select_new_pokemon(p, new_window)
                ).pack(pady=5)
        else:
            self.app_context.txt_Box_3.insert("end","\nAll your Pokémon have fainted! Game Over.")
            quit()

    def select_new_pokemon(self, pokemon, window):
        """Select a new Pokémon and continue the battle."""
        self.selected_pokemon = pokemon
        self.update_health_bars(self.selected_pokemon, self.opponent_pokemon)
        self.display_moves(self.selected_pokemon, self.opponent_pokemon)
        window.destroy()

    def use_inventory_item(self,item):
        if item == 'Potion':
            self.selected_pokemon.health = min(self.selected_pokemon.health + 20, self.selected_pokemon.max_health)
            self.inventory[item] -= 1
            print(self.inventory[item])
            self.app_context.txt_Box_3.insert("end","\nPotion used!\n You gained 20 health!")
        elif item == 'Pokeball':
            if self.opponent_pokemon:
                catch_rate = random.uniform(0, 1)
                if catch_rate > 0.5:
                    self.stored_pokemon.append(self.opponent_pokemon)
                    self.app_context.txt_Box_3.insert("end",f"\nYou caught {self.opponent_pokemon.name}!")
                else:
                    self.app_context.txt_Box_3.insert("end","\nCapture Failed", "The Pokémon broke free!")
            else:
                self.app_context.txt_Box_3.insert("end","\nNo Opponent", "There is no opponent to catch!")
        
        self.inventory.update({item: self.inventory[item]})