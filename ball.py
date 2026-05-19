import random
import time
import os

# Dimensions aléatoires entre les limites
LARGEUR = 20
HAUTEUR = 20

print(f"🌲 Création d'une forêt de {HAUTEUR} x {LARGEUR}...")
time.sleep(1)

# États
ARBRE = 0
FEU = 1
CENDRE = 2

# Création forêt dense (90% arbres)
grille = [[ARBRE if random.random() < 0.9 else CENDRE for _ in range(LARGEUR)] for _ in range(HAUTEUR)]

def compter_voisins_feu(grille, x, y):
    """Compte le nombre de voisins en feu"""
    feux_voisins = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < LARGEUR and 0 <= ny < HAUTEUR:
                if grille[ny][nx] == FEU:
                    feux_voisins += 1
    return feux_voisins

def propagation_feu():
    nouvelle = [ligne[:] for ligne in grille]
    nouveau_feux = 0
    
    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            if grille[y][x] == FEU:
                # Le feu brûle et devient cendre
                nouvelle[y][x] = CENDRE
                
                # Propagation aux arbres voisins (aléatoire)
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < LARGEUR and 0 <= ny < HAUTEUR:
                            if grille[ny][nx] == ARBRE:
                                # Plus de voisins en feu = plus de chance
                                voisins_feu = compter_voisins_feu(grille, nx, ny)
                                # Probabilité de prendre feu (plus aléatoire)
                                if random.random() < (0.3 + voisins_feu * 0.15):
                                    nouvelle[ny][nx] = FEU
                                    nouveau_feux += 1
            
            elif grille[y][x] == ARBRE:
                # Feu spontané (rare)
                if random.random() < 0.005:  # 0.5% de chance
                    nouvelle[y][x] = FEU
                    nouveau_feux += 1
    
    return nouvelle, nouveau_feux

# Allumer plusieurs feux initiaux
print("🔥 Allumage des feux...")
nb_feu_init = random.randint(3, 8)
for _ in range(nb_feu_init):
    x = random.randint(0, LARGEUR-1)
    y = random.randint(0, HAUTEUR-1)
    grille[y][x] = FEU

generation = 0
pause = 0.15  # Plus rapide pour grande grille

try:
    while True:
        os.system('clear')
        
        # Compteurs
        arbres = 0
        feux = 0
        cendres = 0
        
        # Affichage simplifié pour performance
        print(f"{'='*60}")
        print(f"🔥 SIMULATION FEU DE FORÊT 🌲")
        print(f"📏 Dimensions: {HAUTEUR} x {LARGEUR}")
        print(f"{'='*30}")
        
        # Affichage avec symboles simples pour rapidité
        for ligne in grille:
            aff_ligne = ""
            for cellule in ligne:
                if cellule == ARBRE:
                    aff_ligne += "🌲"
                    arbres += 1
                elif cellule == FEU:
                    aff_ligne += "🔥"
                    feux += 1
                else:
                    aff_ligne += "⬛"
                    cendres += 1
            print(aff_ligne)
        
        print(f"{'='*60}")
        print(f"🌲 Arbres: {arbres}   🔥 Feux: {feux}   ⬛ Cendres: {cendres}")
        print(f"📊 Génération: {generation}   🎯 Pourcentage brûlé: {(cendres/(HAUTEUR*LARGEUR))*100:.1f}%")
        
        # Barre de progression
        progression = int((cendres/(HAUTEUR*LARGEUR)) * 40)
        print("🔥 Progression:")
        print(f"[{'█'*progression}{'░'*(40-progression)}]")
        
        if feux == 0:
            print(f"\n✅ Tous les feux sont éteints!")
            print(f"🏁 Simulation terminée après {generation} générations")
            print(f"📊 Surface brûlée: {(cendres/(HAUTEUR*LARGEUR))*100:.1f}%")
            break
        
        grille, nouveau_feux = propagation_feu()
        generation += 1
        
        # Ajustement dynamique de la vitesse
        if feux > 100:
            time.sleep(pause * 0.7)
        else:
            time.sleep(pause)
        
except KeyboardInterrupt:
    print(f"\n\n⏸️ Simulation arrêtée à la génération {generation}")
    arbres_fin = sum(ligne.count(ARBRE) for ligne in grille)
    print(f"🌲 Arbres restants: {arbres_fin}")