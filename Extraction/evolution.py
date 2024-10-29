from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://pokemondb.net/evolution'
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')
    infocard_divs = body.findAll('div', class_='infocard-filter-block')
    evolutions = []
    for entry in infocard_divs:
        evolution_chain = [pokemon.strip() for pokemon in entry.text.strip().split('#') if pokemon.strip()]

        evolution_chain_1 = evolution_chain[0] if len(evolution_chain) > 0 else None
        evolution_chain_2 = evolution_chain[1] if len(evolution_chain) > 1 else None
        evolution_chain_3 = evolution_chain[2] if len(evolution_chain) > 2 else None
        evolutions.append([evolution_chain_1,evolution_chain_2,evolution_chain_3])

    df = pd.DataFrame(evolutions)
    df.columns = ['Evo_1','Evo_2','Evo_3']
    print(df)