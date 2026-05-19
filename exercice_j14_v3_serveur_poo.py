import socket
import threading
import struct
import signal
import os
from datetime import datetime

class Serveur:
    def __init__(self, hote, port):
        self.hote = hote
        self.port = port
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serveur.bind((self.hote, self.port))
        self.serveur.listen(10)
        
        self.__clients = {}          # dictionnaire privé {pseudo: connexion}
        self.__verrou = threading.Lock()
        self.en_marche = True
        
        # Enregistrer les gestionnaires de signaux
        signal.signal(signal.SIGTERM, self.gestionnaire_sigterm)
        signal.signal(signal.SIGINT, self.gestionnaire_sigint)
        
        print(f"[SERVEUR] démarré avec PID: {os.getpid()}")
        print("Envoie SIGTERM pour arrêter proprement")
    
    # ========== GESTIONNAIRES DE SIGNAUX ==========
    def gestionnaire_sigterm(self, signum, frame):
        print("\n[SIGTERM reçu] Nettoyage en cours...")
        self.fermer_proprement()
    
    def gestionnaire_sigint(self, signum, frame):
        print("\n[Ctrl+C] Arrêt propre...")
        self.fermer_proprement()
    
    def fermer_proprement(self):
        self.en_marche = False
        self.fermer_conn()
        exit(0)
    
    # ========== LOGGER ==========
    def logger(self, pseudo, message):
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ligne = f"{horodatage} | {pseudo} | {message}\n"
        try:
            with open("chat_log.txt", "a") as f:
                f.write(ligne)
        except:
            pass
        print(ligne.strip())
    
    # ========== PROPERTY POUR LES CLIENTS ==========
    @property
    def clients(self):
        with self.__verrou:
            return self.__clients.copy()
    
    def ajouter_client(self, pseudo, connexion):
        with self.__verrou:
            self.__clients[pseudo] = connexion
    
    def retirer_client(self, pseudo):
        with self.__verrou:
            return self.__clients.pop(pseudo, None)
    
    # ========== ENVOI ET RÉCEPTION ==========
    def envoyer_a_tous(self, message, expediteur=None):
        donnees = message.encode("utf-8")
        longueur = struct.pack("!I", len(donnees))
        
        with self.__verrou:
            for pseudo, conn in self.__clients.items():
                if pseudo != expediteur:
                    try:
                        conn.sendall(longueur + donnees)
                    except:
                        pass
    
    def recevoir_message(self, conn):
        try:
            longueur_donnees = conn.recv(4)
            if not longueur_donnees:
                return None
            longueur = struct.unpack("!I", longueur_donnees)[0]
            donnees = b""
            while len(donnees) < longueur:
                morceau = conn.recv(min(1024, longueur - len(donnees)))
                if not morceau:
                    return None
                donnees += morceau
            return donnees.decode("utf-8")
        except:
            return None
    
    # ========== GESTION D'UN CLIENT ==========
    def gerer_client(self, conn, adresse, pseudo):
        print(f"[+] {pseudo} connecté depuis {adresse}")
        self.envoyer_a_tous(f"{pseudo} a rejoint le chat", expediteur=pseudo)
        self.logger("SYSTEME", f"{pseudo} a rejoint le chat")
        
        try:
            while self.en_marche:
                message = self.recevoir_message(conn)
                if not message or message == '/clore':
                    break
                
                # Logger le message
                self.logger(pseudo, message)
                
                # Diffuser à tous
                self.envoyer_a_tous(f"{pseudo} > {message}", expediteur=pseudo)
        except:
            pass
        finally:
            self.retirer_client(pseudo)
            conn.close()
            print(f"[-] {pseudo} déconnecté")
            self.envoyer_a_tous(f"{pseudo} a quitté le chat")
            self.logger("SYSTEME", f"{pseudo} a quitté le chat")
    
    # ========== BOUCLE PRINCIPALE ==========
    def ecouter(self):
        print(f"Serveur en écoute sur {self.hote}:{self.port}")
        
        try:
            while self.en_marche:
                conn, adresse = self.serveur.accept()
                pseudo = conn.recv(1024).decode("utf-8")
                self.ajouter_client(pseudo, conn)
                
                thread_client = threading.Thread(
                    target=self.gerer_client,
                    args=(conn, adresse, pseudo),
                    daemon=True
                )
                thread_client.start()
                print(f"[*] Clients actifs : {len(self.clients)}")
        except:
            pass
        finally:
            self.fermer_conn()
    
    # ========== FERMETURE ==========
    def fermer_conn(self):
        print("Fermeture du serveur...")
        with self.__verrou:
            for conn in self.__clients.values():
                try:
                    conn.close()
                except:
                    pass
            self.__clients.clear()
        try:
            self.serveur.close()
        except:
            pass
        print("Serveur fermé.")
    
    # ========== STR ==========
    def __str__(self):
        return f"Serveur en ecoute sur {self.hote}:{self.port} - Clients: {len(self.clients)}"


# ========== LANCEMENT ==========
if __name__ == "__main__":
    s = Serveur('0.0.0.0', 9000)
    print(s)
    s.ecouter()