import matplotlib.pyplot as plt

mois = ["Jan","Fév","Mar","Avr","Mai","Jun",
        "Jul","Aoû","Sep","Oct","Nov","Déc"]

cas_cholera = [120, 145, 200, 310, 420, 380,
               290, 260, 190, 150, 130, 110]

# Tracer une courbe
plt.plot(mois, cas_cholera)

# Titre et axes
plt.title("  ÉVOLUTION DES CAS SUR 12 MOIS")
plt.xlabel("MOIS")
plt.ylabel("CAS DE CHOLERA ")

# Marquer le pic en rouge
pic = max(cas_cholera)
plt.axhline(y=pic, color='red', linestyle='--', label="Pic critique")

# Afficher la légende
plt.legend()

# Afficher
#plt.show()
plt.savefig("cholera_bukavu.png")