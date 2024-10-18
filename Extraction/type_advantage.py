import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def find_advantage_pages():
    url = 'https://pokemondb.net/type/'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    type_links = []
    a_tags = soup.find_all('a', class_='type-icon')
    for link in a_tags:
        type_links.append('https://pokemondb.net' + link['href'])
    return type_links

def split_combined_types(advantages):
    # Use regex to split combined types like "RockSteel" into ["Rock", "Steel"]
    separated = re.sub(r'([a-z])([A-Z])', r'\1 \2', advantages)
    return separated.split()  # Split into list of advantages

def scrape_effective_advantages(type_url):
    response = requests.get(type_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    advantage_section = soup.find('div', class_='grid-col')
    find_advantages = advantage_section.find_all('p', class_='type-fx-list')
    
    if find_advantages:
        # Extract the text for effective advantages
        effective_against = find_advantages[0].get_text(strip=True)
        advantage_list = split_combined_types(effective_against)
        # Strip extra whitespace
        return [adv.strip() for adv in advantage_list]
    return []

def scrape_not_effective_advantages(type_url):
    response = requests.get(type_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    advantage_section = soup.find('div', class_='grid-col')
    find_advantages = advantage_section.find_all('p', class_='type-fx-list')
    
    if find_advantages:
        # Extract the text for not effective advantages
        not_effective_against = find_advantages[1].get_text(strip=True)
        advantage_list = split_combined_types(not_effective_against)
        # Strip extra whitespace
        return [adv.strip() for adv in advantage_list]
    return []

def main():
    links = find_advantage_pages()
    all_advantages = {}
    all_none_advantages = {}

    for link in links:
        type_name = link.split('/')[-1]
        advantages = scrape_effective_advantages(link)
        none_advantages = scrape_not_effective_advantages(link)
        all_advantages[type_name] = advantages
        all_none_advantages[type_name] = none_advantages

    # Create DataFrames from the dictionaries
    df_effective = pd.DataFrame.from_dict(all_advantages, orient='index')
    df_none = pd.DataFrame.from_dict(all_none_advantages, orient='index')

    # Rename columns for effective advantages
    max_advantages = df_effective.shape[1]
    df_effective.columns = [f'Effective_Advantage_{i+1}' for i in range(max_advantages)]

    # Rename columns for not effective advantages
    max_none_advantages = df_none.shape[1]
    df_none.columns = [f'Not_Effective_Advantage_{i+1}' for i in range(max_none_advantages)]

    # Reset index to include the Pokémon type as a column
    df_effective.reset_index(inplace=True)
    df_effective.rename(columns={'index': 'Type'}, inplace=True)

    df_none.reset_index(inplace=True)
    df_none.rename(columns={'index': 'Type'}, inplace=True)

    # Fill NaN values with empty strings for better formatting
    df_effective.fillna('', inplace=True)
    df_none.fillna('', inplace=True)

    # Save to separate CSV files
    df_effective.to_csv('Effective_Against.csv', index=False)
    df_none.to_csv('Not_Effective_Against.csv', index=False)

    print("CSV files have been saved!")

main()
