import requests
import pandas as pd

def scraper_population():
    # Tentative 1 : Worldometers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        reponse = requests.get(
            'https://www.worldometers.info/world-population/africa-population',
            headers=headers,
            timeout=10
        )
        
        if reponse.status_code == 200:
            df = pd.read_html(reponse.text)[0]
            df.to_csv('population_afrique.csv', index=False)
            print("✅ RÉUSSI (Worldometers)")
            print(f"   Fichier : population_afrique.csv")
            print(f"   Lignes : {len(df)}")
            return df
        else:
            print(f"⚠️ Worldometers échoue (HTTP {reponse.status_code})")
            
    except Exception as e:
        print(f"⚠️ Worldometers échoue : {e}")
    
    # Tentative 2 : Wikipedia
    print("🔄 Tentative avec Wikipedia...")
    
    try:
        df = pd.read_html('https://en.wikipedia.org/wiki/List_of_African_countries_by_population')[0]
        df.to_csv('population_afrique.csv', index=False)
        print("✅ RÉUSSI (Wikipedia)")
        print(f"   Fichier : population_afrique.csv")
        print(f"   Lignes : {len(df)}")
        return df
        
    except Exception as e:
        print(f"❌ ÉCHEC TOTAL : {e}")
        return None

# Exécution
resultat = scraper_population()