
#importation
import socket
import struct 
import os
import signal
import time
import threading

#gestion des signaux 
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

print(f"[CLIENT] démarré sur (PID: {os.getpid()})")
print("Envoie SIGTERM pour arrêter proprement")


#fonction pour envoyer des données 
def envoyer_donnee(client, message) :
    donnees = message.encode("utf-8")
    longueur = struct.pack("!I", len(donnees))
    client.sendall(longueur+donnees)
#fonction pour recevoir des donnees    
def recevoir_donnee(conn) :
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
        reponse = donnees.decode("utf-8")
        print(reponse)

def demarrer_client(ip, port) :
    pseudo = input("Entrez un pseudo > ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    #envoyer le pseudo 
    client.send(pseudo.encode())
    print(f"[{pseudo}] connecté a [*]")
    thread_recevoir = threading.Thread(target = recevoir_donnee, args = (client), daemon = True)
    thread_recevoir.start()
    while True :
        message = input("[MOI] > ")
        thread_envoyer = threading.Thread(target = envoyer_donnee, args = (client, message), daemon = True)
        thread_envoyer.start()
        if message == '/clore' :
            break
    client.close()

if __name__ == '__main__' :
    demarrer_client("0.0.0.0",  9000)



