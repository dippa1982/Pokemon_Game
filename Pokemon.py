import random
import csv

class Pokemon_Character:
    def __init__(self, name, id, level, health, attack, defence, type, SpA, SpD, Spe, move1, move2, move3, move4) -> None:
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

    def use_ability(self, target, selected_ability, type_advantage, type_disadvantage):
        base_damage = self.attack
        if target.type in type_advantage.get(self.type, {}).get('strong_against', []):
            print(f"{self.name} is strong against {target.name}")
            base_damage *= 2
        elif target.type in type_disadvantage.get(self.type, {}).get('weak_against', []):
            print(f"{self.name} is weak against {target.name}")
            base_damage *= 0.5
        
        # Final damage calculation
        random_damage = random.randint(1,50)
        total_damage = int(base_damage - target.defence + random_damage)
        if total_damage < 0:
            total_damage = 0
        if total_damage >= target.health:
            total_damage = target.health
        print(f"{self.name} uses {selected_ability} on {target.name}. It deals {total_damage} damage!")
        
        target.health -= total_damage
        print(f"{target.name}'s remaining health: {target.health}/{target.max_health}")

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
