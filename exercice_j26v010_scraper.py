import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

try:
    df = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_African_countries_by_population',  # ← quote enlevée
        storage_options=headers
    )[0]
    
    df.to_csv('population_afrique.csv', index=False)
    print("✅ RÉUSSI")
    print(f"   Lignes : {len(df)}")
    
except Exception as e:
    print(f"❌ ÉCHEC : {e}")