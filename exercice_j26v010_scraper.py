import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

reponse = requests.get(
    'https://www.worldometers.info/world-population/africa-population',
    headers=headers
)

# Lecture directe du HTML (pas besoin de BeautifulSoup si tu utilises pd.read_html)
tableaux = pd.read_html(reponse.text)
df = tableaux[0]

print(df.head())