import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd

pokemon_dict = {}

def extract_moves():
    url = 'https://pokemondb.net/move/all'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='data-table')
    rows = table.find_all('tr')
    move_data = []
    for row in rows:
        a_tag = row.find('a', class_='ent-name')
        b_tag = row.find('a', class_='type-icon')
        c_tag = row.find_all('td', class_='cell-num')
        if a_tag and b_tag and c_tag:
            move_name = a_tag['title'].replace('View details for ','')
            move_type = b_tag.text
            move_power = c_tag[0].text
            move_acc = c_tag[1].text
            move_data.append((move_name, move_type, move_power))
    return move_data

import requests
from bs4 import BeautifulSoup

def extract_evolution_data():
    url = 'https://m.bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_evolutionary_line'
    
    try:
        # Make a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Parse the HTML content
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Prepare a list to hold rows of evolution data
        evolutions = []

        # Find the tables containing the evolutionary lines
        tables = soup.find_all('table', class_='roundy')

        for table in tables:
            rows = table.find_all('tr')  # Find all rows in the table
            for row in rows:
                cells = row.find_all('td')  # Find all cells in the row
                if cells:  # Check if the row has cells
                    # Extract Pokémon names from the cells
                    evolution_line = [cell.get_text(strip=True) for cell in cells]
                    evolutions.append(evolution_line)  # Add the evolution line to the list

        return evolutions

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []

# Example usage
evolution_data = extract_evolution_data()

# Print the extracted evolution data
for line in evolution_data:
    print(" -> ".join(line))


def extract_pokemon():
    url = 'https://pokemondb.net/pokedex/all'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='data-table')
    pokemon_list = []
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            name_data = row.find('a', class_='ent-name')
            type_data = row.find('a', class_='type-icon')
            hp_data = row.find_all('td', class_='cell-num')[2]
            attack_data = row.find_all('td', class_='cell-num')[3]
            defence_data = row.find_all('td', class_='cell-num')[4]
            poke_name = name_data.text.strip()
            poke_type = type_data.text.strip()
            poke_hp = hp_data.text.strip()
            poke_attack = attack_data.text.strip()
            poke_defence = defence_data.text.strip()
            pokemon_list.append({'Name': poke_name, 'Type': poke_type, 'Health': poke_hp,'Attack': poke_attack, 'Defence': poke_defence})
            print({'Name': poke_name, 'Type': poke_type, 'Health': poke_hp, 'Attack': poke_attack, 'Defence': poke_defence})
    return pokemon_list

def to_csv(move_data, pokemon_list):
    df_pokemon = pd.DataFrame(pokemon_list, columns=['Name', 'Type', 'Health', 'Attack', 'Defence'])
    df_moves = pd.DataFrame(move_data, columns=['Move Name', 'Move Type', 'Move Power'])
    df_pokemon.to_csv('Pokemon.csv')
    df_moves.to_csv('Moves.csv')

def Evo_to_csv(evole_list):
    df_evolve = pd.DataFrame(evole_list[1:], columns=['First_evolution', 'Second_evolution','Third_evolution','Forth_Evolution','Firth_Evolution','Sixth_Evolution','Seventh_Evolution','Eighth_Evolution'])
    df_evolve.to_csv('Evolution.csv')

def pokemon_with_moves():
    pokemon_df = pd.read_csv('Pokemon.csv')
    moves_df = pd.read_csv('Moves.csv')
    moves_by_type = {}
    for index, row in moves_df.iterrows():
        move_type = row['Move Type']
        move_name = row['Move Name']
        if move_type in moves_by_type:
            moves_by_type[move_type].append(move_name)
        else:
            moves_by_type[move_type] = [move_name]

    for index, row in pokemon_df.iterrows():
        poke_name = row['Name']
        poke_type = row['Type']
        if poke_type in moves_by_type:
            pokemon_df.at[index, 'Moves'] = ','.join(moves_by_type[poke_type])
        else:
            pokemon_df.at[index, 'Moves'] = 'No moves of this type'
    pokemon_df.to_csv('Pokemon_with_moves.csv', index=False)
    print('File saved with moves')

pokemon_dict = extract_pokemon()
move_dic = extract_moves()
to_csv(move_dic,pokemon_dict)
pokemon_with_moves()