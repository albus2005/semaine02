import matplotlib.pyplot as plt

# Paramètres
N     = 1_000_000
beta  = 0.1
gamma = 0.05
duree = 160

# Conditions initiales
S = 999_990
I = 10
R = 0

# Listes pour sauvegarder
historique_S = [S]
historique_I = [I]
historique_R = [R]
'''
Nouveaux infectés  = beta × S × I / N
Nouveaux guéris    = gamma × I

S demain = S aujourd'hui - nouveaux infectés
I demain = I aujourd'hui + nouveaux infectés - nouveaux guéris
R demain = R aujourd'hui + nouveaux guéris
'''
# Boucle sur les jours
for jour in range(duree):
    # Calculs
    nouveaux_infectes = beta * S * I / N
    nouveaux_gueris   =gamma * I
    
    # Mise à jour
    S = S - nouveaux_infectes
    I = I + nouveaux_infectes - nouveaux_gueris
    R = R + nouveaux_gueris
    
    # Sauvegarde
    historique_S.append(S)
    historique_I.append(I)
    historique_R.append(R)

# Visualisation
jours = list(range(duree + 1))
plt.plot(jours, historique_S, color='blue', label='Susceptibles')
plt.plot(jours, historique_I, color='red', label='Infectés')
plt.plot(jours, historique_R, color='green', label='Guéris')
plt.title('S. I. R')
plt.xlabel('DUREE')
plt.ylabel('CAS')
plt.legend()
plt.savefig("sir_bukavu.png")