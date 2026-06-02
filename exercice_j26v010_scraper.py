import requests
from bs4 import BeautifulSoup
import pandas as pd

reponse = requests.get('https://en.wikipedia.org/wiki/List_of_African_countries_by_population')
soup = BeautifulSoup(reponse.text, 'html.parser')

# Méthode simple et rapide
df = pd.read_html(reponse.text)[0]
print(df.head())

# Ou méthode précise
tableau = soup.find('table')
df = pd.read_html(str(tableau))[0]
print(df.head())