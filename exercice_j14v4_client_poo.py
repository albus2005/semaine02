import socket
import threading
import struct

class Client:
    def __init__(self, hote, port):
        self.hote = hote
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pseudo = None
        self.connecte = False
    
    def connecter_client(self):
        self.client.connect((self.hote, self.port))
        self.pseudo = input("Entrez votre pseudo > ")
        self.client.send(self.pseudo.encode())
        self.connecte = True
        print(f"[{self.pseudo}] connecté au chat")
        
        # Démarrer le thread réception
        thread_recevoir = threading.Thread(target=self.recevoir_en_boucle, daemon=True)
        thread_recevoir.start()
        
        # Boucle d'envoi
        while self.connecte:
            message = input("[MOI] > ")
            if message == '/clore':
                self.envoyer_message(message)
                break
            self.envoyer_message(message)
        
        self.fermer_client()
        
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
    
    def envoyer_message(self, message):
        if not self.connecte:
            return
        donnees = message.encode("utf-8")
        longueur = struct.pack("!I", len(donnees))
        try:
            self.client.sendall(longueur + donnees)
        except:
            pass
    
    def recevoir_message(self):
        try:
            longueur_donnees = self.client.recv(4)
            if not longueur_donnees:
                return None
            longueur = struct.unpack("!I", longueur_donnees)[0]
            donnees = b""
            while len(donnees) < longueur:
                morceau = self.client.recv(min(1024, longueur - len(donnees)))
                if not morceau:
                    return None
                donnees += morceau
            return donnees.decode("utf-8")
        except:
            return None
    
    def recevoir_en_boucle(self):
        while self.connecte:
            message = self.recevoir_message()
            if not message:
                break
            print(f"\n[*] {message}")
            print("[MOI] > ", end="", flush=True)
    
    def fermer_client(self):
        self.connecte = False
        try:
            self.client.close()
        except:
            pass
        print("Client déconnecté.")
    
    def __str__(self):
        return f"Client connecté sur {self.hote}:{self.port} - Pseudo: {self.pseudo}"


if __name__ == "__main__":
    c = Client('127.0.0.1', 9000)  # localhost pour le client
    print(c)
    c.connecter_client()