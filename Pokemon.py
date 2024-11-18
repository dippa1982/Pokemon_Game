import random
import csv
import time

class Pokemon_Character:
    def __init__(self, name, id, level, health, attack, defence, type, SpA, SpD, Spe, move1, move2, move3, move4, effect=None, app_context=None) -> None:
        self.name = name
        self.id = id
        self.health = health
        self.attack = attack
        self.defence = defence
        self.max_health = health
        self.level = level
        self.type = type
        self.SpA = SpA
        self.SpD = SpD
        self.Spe = Spe
        self.is_alive = True
        self.xp = 0
        self.xp_to_level = 10
        self.abilities = [move1, move2, move3, move4]
        self.effect = effect
        self.app_context = app_context

    def use_ability(self, target, selected_ability, type_advantage, type_disadvantage):
        raw_dmg = 0
        raw_dmg = ((self.attack / target.defence) * 25)

        if target.type in type_advantage.get(self.type, {}).get('strong_against', []):
            self.app_context.txt_Box_3.insert("end", f"{self.name} is strong against {target.name}\n")
            raw_dmg *= 2
        elif target.type in type_disadvantage.get(self.type, {}).get('weak_against', []):
            self.app_context.txt_Box_3.insert("end", f"{self.name} is weak against {target.name}\n")
            raw_dmg *= 0.5
        elif target.type == self.type:
            self.app_context.txt_Box_3.insert("end", f"{self.name} and {target.name} have the same type!\n")
            raw_dmg *= 1.5
        
        modifier = raw_dmg  * random.uniform(0.85, 1.0)
        final_dmg = round(((2*self.level / 5 + 2) * (self.attack) / (target.defence * 50) / 50 + 2) * modifier)
        self.app_context.txt_Box_3.insert("end", f"\n{self.name} uses {selected_ability} on {target.name}. It deals {final_dmg} damage!\n")
        time.sleep(1)

        target.health -= final_dmg
        if final_dmg > target.health:
            target.health = 0
            target.is_alive = False
        self.app_context.txt_Box_3.insert("end", f"\n{target.name}'s remaining health: {target.health}/{target.max_health}\n")
        time.sleep(1)

    @staticmethod
    def load_type_advantages(advantage_filename, disadvantage_filename):
        type_advantage = {}
        type_disadvantage = {}

        # Load advantages
        with open(advantage_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                poke_type = row['Type']
                advantages = [row.get(f'Effective_Advantage_{i}') for i in range(1, 8)]
                advantages = [adv for adv in advantages if adv]
                type_advantage[poke_type] = {'strong_against': advantages}

        # Load disadvantages
        with open(disadvantage_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                poke_type = row['Type']
                disadvantages = [row.get(f'Not_Effective_Advantage_{i}') for i in range(1, 6)]
                disadvantages = [dis for dis in disadvantages if dis]
                type_disadvantage[poke_type] = {'weak_against': disadvantages}

        return type_advantage, type_disadvantage
    
    @staticmethod
    def evolution_data(filepath):
        starter_pokemon = []
        first_evo = []
        second_evo = []
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                starter = row['Starter']
                first_evolution = row['First_Evo']
                second_evolution = row['Second_Evo']
                starter_pokemon.append(starter)
                first_evo.append(first_evolution)
                second_evo.append(second_evolution)
        return starter_pokemon, first_evo, second_evo
    
    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_to_level += 10
        self.max_health += 10
        self.health = self.max_health
        self.attack += 1
        self.defence += 1
        self.SpA += 1
        self.SpD += 1
        self.Spe += 1

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= self.xp_to_level:
            self.level_up()