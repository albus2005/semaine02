import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

reponse = requests.get(
    'https://en.wikipedia.org/wiki/List_of_African_countries_by_population',
    headers=headers
)


soup = BeautifulSoup(reponse.text, 'html.parser')

# Étape 4 : trouver tous les tableaux de la page
tableaux = pd.read_html(reponse.text)
df = tableaux[0]
print(df.head())