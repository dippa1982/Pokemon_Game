import random

raw_dmg = 0
pokemon_atk = 84
pokemon_df = 95
raw_dmg = ((pokemon_atk / pokemon_df) * 25) * 0.5

final_dmg = round(raw_dmg * (random.randint(80,120)) / 100)
print(final_dmg)