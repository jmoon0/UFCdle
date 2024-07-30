import pandas as pd
import requests
from io import StringIO

def scrape_fighter_roster(): 
    url = 'https://en.wikipedia.org/wiki/List_of_current_UFC_fighters'
    response = requests.get(url)
    response.raise_for_status()  
    tables = pd.read_html(StringIO(response.text))

    fighters = []
    
    #tables 7-14 men's, 15-18 women's divisions (remember Python range upper limit argument is < and not <=)
    #Currently only scraping men's divisions
    for x in range(7,15):
        table = tables[x]
        if 'Name' in table.columns:
            fighters.extend(table['Name'].to_list())
    
    return fighters

def scrape_released_fighters():
    url = 'https://en.wikipedia.org/wiki/List_of_current_UFC_fighters'
    response = requests.get(url)
    response.raise_for_status()  
    tables = pd.read_html(StringIO(response.text))

    released_fighters = tables[0]['Name'].to_list()
    return released_fighters