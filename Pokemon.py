import random

class Pokemon_Character:
    type_advantage = {
        'Fire': {'strong_against':['Grass'], 'weak_against': ['Water']},
        'Water': {'strong_against': ['Fire'], 'weak_against': ['Electric','Grass']},
        'Grass': {'strong_against': ['Water'], 'weak_against': ['Fire','Electric']},
        'Electric': {'strong_against': ['Water','Fire'], 'weak_against': ['Grass']}
    }

    def __init__(self,name,level,health,attack,defence,pokemon_type,abilities) -> None:
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence
        self.max_health = health
        self.level = level
        self.pokemon_type = pokemon_type
        self.is_alive = True
        self.xp = 0
        self.xp_to_level = 10
        self.abilities = []

    def use_ability(self, target, selected_ability):
        base_damage = self.attack
        
        if target.pokemon_type in self.type_advantage[self.pokemon_type]['strong_against']:
            print(f"{self.name} is strong against {target.name}")
            base_damage *= 1.5
        else:
            print(f"{self.name} is weak against {target.name}")
            base_damage *= 0.5
        
        damage_modifier = selected_ability['damage_modifier']
        total_damage = int(base_damage * damage_modifier)

        print(f"{self.name} uses {selected_ability['name']} on {target.name}. It deals {total_damage} damage!")
        target.health -= total_damage
        target.health = max(0, target.health)
