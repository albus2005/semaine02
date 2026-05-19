# SERVEUR MULTITHREAD ROBUSTE

#importation
import socket
import struct 
import threading 
import os
import signal
import time
from datetime import datetime
maintenant = datetime.now()
print(maintenant.strftime("%Y-%m-%d %H:%M:%S"))
#logeur 
def logger(pseudo, message):
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = f"{horodatage} | {pseudo} | {message}\n"

    with open("chat_log.txt", "a") as f:
        f.write(ligne)
    print(ligne.strip())
#gestionnaire des signaux 
def gestionnaire_sigterm(signum, frame):
    print("\n[SIGTERM reçu] Nettoyage en cours...")
    # fermer les connexions, sauvegarder les données
    exit(0)

def gestionnaire_sigint(signum, frame):
    print("\n[Ctrl+C] Arrêt propre...")
    exit(0)

# Enregistrer les gestionnaires
signal.signal(signal.SIGTERM, gestionnaire_sigterm)
signal.signal(signal.SIGINT,  gestionnaire_sigint)

print(f"SERVEUR démarré sur (PID: {os.getpid()})")
print("Envoie SIGTERM pour arrêter proprement")


#fonction pour envoyer des données 
'''
Fonction : Envoyer les Message a tous
envoyer_donnee(conn, message, verrou, clients, expediteur=None) :
    donnees = message.encoder()
    longeur = struct.pack('!I', len(donnees))
    avec verrou :
        Pour pseudo, connexion dans clients.Items() :
        Si le pseudo != expediteur :
            Essayer :
                conn.envoyerTout(longeur+donnees)
            En cas d'erreur :
                Écrire ('Erreur Inconnu ')
'''
def envoyer_donnee(conn, message, verrou, clients, expediteur) :
    donnees = message.encode()
    longueur = struct.pack("!I", len(donnees))
    with verrou:
        for pseudo, connexion in clients.items():
            if pseudo != expediteur:
                connexion.sendall(longueur+donnees)
                
                    #print("Erreur dans l'envoi!")
    
#fonction pour recevoir des donnees 
# NOTE : Bloque ici. Changer approche. C'est le servzur qui initie la conversation des que le cloent se connecte 
def recevoir_donnees(conn) :
    #recevior la tzille des données avant de les unpack 
    longueur_donnees = conn.recv(4)
    #print(f"La longueur du message : {longueur_donnees.decode("utf-8")}")
    if not longueur_donnees :
        return None 
    longueur = struct.unpack("!I", longueur_donnees)[0]
    donnees = b""
    while len(donnees) < longueur :
        morceau = conn.recv(min(1024, (longueur - len(donnees))))         #Aquoi sert cette ligne?
        if not morceau :
            return None        #que se passe t ik dans un programme quand une fonction retourne None? et None == Nulle?
        donnees +=morceau
    return donnees.decode("utf-8")
'''
fonction : Gestion de clients
Tant que Vrai :
    message = recevoir_donnees(conn)
    Si message == '/clore' :
        Ecrire("Connexion close")
        Arrêter 
    Sinon :
        envoyer_donnee(conn, message, verrou, clients )
    FinSi
FinTantQue
'''
#gestion client
# ✅ CORRECT
def gerer_client(conn, adresse, pseudo, verrou, clients):
    try:
        while True:
            message = recevoir_donnees(conn)
            if not message or message == '/clore':
                break
            logger(pseudo, message)
            broadcaster(message, verrou, clients, pseudo)
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        with verrou:
            clients.pop(pseudo, None)    # retirer de la liste
        conn.close()
        print(f"[-] {pseudo} déconnecté")
        broadcaster(f"{pseudo} a quitté le chat", verrou, clients, None)

#fonction pour demarer le serveur 
def demarer_serveur(ip, port) :
    #creation du socket
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #allumage du serveur 
    serveur.bind((ip, port))
    serveur.listen(10)
    #Pour verifier dans la console
    print(f"[*] SERVEUR ALLUMÉ: {ip}:{port}")
    print("[*] Serveur en écoute....")

    verrou = threading.Lock()
    clients = {}
    while True :
        conn, adresse = serveur.accept()          #OSError: [Errno 9] Bad file descriptor
        pseudo = conn.recv(1024).decode("utf-8")
        with verrou :
            clients[pseudo] = conn
            print(clients)
        thread_client = threading.Thread(target = gerer_client, args = (conn, adresse, pseudo, verrou, clients), daemon = True)
        #thread.daemon = True         #c'est quelle type de variables ?
        thread_client.start()
        print(f"[*] Client Actif : {threading.active_count() - 1}")
        print(f"{pseudo} est connecté.")
        
    conn.close()
    serveur.close()
    
    
if __name__ == "__main__" :
    demarer_serveur("0.0.0.0",  9000)
    