import socket
import threading
import time

# Verrou pour protéger les listes partagées
verrou = threading.Lock()

def scanner_reseau(ip, port, timeout, success, echecs):
    try:
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanner.settimeout(timeout)
        resultat = scanner.connect_ex((ip, port))   # ✅ scanner.connect_ex
        scanner.close()

        with verrou:                                 # ✅ protection partagée
            if resultat == 0:                        # ✅ 0 = port ouvert
                succes = f"{port:>5} [OUVERT]"
                success.append(port)
                print(succes)
            else:
                echecs.append(port)

    except Exception as e:
        with verrou:
            echecs.append(port)

def scanner_port(ip, debut, fin, timeout=1):
    success = []
    echecs  = []
    threads = []                                     # ✅ stocker les threads

    print(f"Scan de {ip} -- ports {debut} à {fin}")
    print("-" * 40)

    debut_scan = time.time()

    for port in range(debut, fin + 1):
        thread = threading.Thread(
            target = scanner_reseau,
            args   = (ip, port, timeout, success, echecs),  # ✅ passer les listes
            daemon = True
        )
        thread.start()
        threads.append(thread)                       # ✅ stocker

    for t in threads:                                # ✅ attendre tous
        t.join()

    fin_scan = time.time()
    durée    = fin_scan - debut_scan

    return sorted(success), len(echecs), durée       # ✅ trié par numéro

if __name__ == '__main__':
    ip    = "127.0.0.1"
    debut = 1001
    fin   = 3000

    ports_ouverts, nb_echecs, durée = scanner_port(ip, debut, fin)

    print("-" * 40)
    print(f"Ports ouverts  : {ports_ouverts}")
    print(f"Ports fermés   : {nb_echecs}")
    print(f"Durée          : {durée:.2f}s")