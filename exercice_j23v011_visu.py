import matplotlib.pyplot as plt

mois = ["Jan","Fév","Mar","Avr","Mai","Jun",
        "Jul","Aoû","Sep","Oct","Nov","Déc"]

cas_cholera = [120, 145, 200, 310, 420, 380,
               290, 260, 190, 150, 130, 110]
cas_malaria = [200, 210, 190, 180, 160, 140,
               130, 120, 150, 180, 200, 220]
# Tracer une courbe
plt.plot(mois, cas_cholera, color = 'blue', label = 'cholera')
plt.plot(mois, cas_malaria, color = 'orange', label = 'malaria')

# Titre et axes
plt.title("  ÉVOLUTION DES CAS SUR 12 MOIS")
plt.xlabel("MOIS")
plt.ylabel("CAS DE CHOLERA & CAS DE MALARIA ")


# Marquer le pic en rouge
pic1 = max(cas_cholera)
plt.axhline(y=pic1, color='red', linestyle='--', label="Pic critique choléra")
pic2= max(cas_malaria)
plt.axhline(y=pic2, color='black', linestyle='--', label="Pic critique malaria")
# Afficher la légende
plt.legend()

# Afficher
#plt.show()
plt.savefig("cholera&malaria_bukavu.png")