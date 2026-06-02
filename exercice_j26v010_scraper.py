import requests
from bs4 import BeautifulSoup
import pandas as pd

# Étape 1 : récupérer le HTML
reponse = requests.get('https://en.wikipedia.org/wiki/List_of_African_countries_by_population')

# Étape 2 : parser le HTML
soup = BeautifulSoup(reponse.text, 'html.parser')

# Étape 3 : trouver le tableau
tableau = soup.find('table')

# Étape 4 : lire avec Pandas
df = pd.read_html(str(tableau))
print(df[0])