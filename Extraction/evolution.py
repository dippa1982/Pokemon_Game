from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_evolutionary_line'
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', class_='roundy')

    evolutions = []
    
    for tbl in tables:
        rows = tbl.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            evolution_line = []
            for col in cols:
                links = col.find_all('a')
                for link in links:
                    evolution_line.append(link.get_text())
            if evolution_line:
                Evo_1 = evolution_line[1]
                Evo_2 = evolution_line[3] if len(evolution_line) > 3 else None
                Evo_3 = evolution_line[5] if len(evolution_line) > 5 else None
                evolutions.append([Evo_1, Evo_2, Evo_3])
    df = pd.DataFrame(evolutions)
    df.columns = ['Starter','First_Evo','Second_Evo']
    df.to_csv('Evo_data.csv')
        

else:
    print(f"Failed to retrieve data: {response.status_code}")
