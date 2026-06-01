
import matplotlib.pyplot as plt  # ✅
import seaborn as sns
mois = ["Jan","Fév","Mar","Avr","Mai","Jun",
        "Jul","Aoû","Sep","Oct","Nov","Déc"]

cas_cholera = [120, 145, 200, 310, 420, 380,
               290, 260, 190, 150, 130, 110]

# Tracer une courbe
sns.barplot(x=mois, y=cas_cholera)
# Titre et axes
plt.title("  ÉVOLUTION DES CAS SUR 12 MOIS")
plt.xlabel("MOIS")
plt.ylabel("CAS DE CHOLERA ")

plt.savefig("bar_cholera.png")

