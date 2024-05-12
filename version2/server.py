import socket
import threading
import sys

# Paramètres du serveur
HOST = 'localhost'
PORT = 12345
ADDR = (HOST, PORT)

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Liaison du socket à l'adresse du serveur
try:
    server_socket.bind(ADDR)
except socket.error as e:
    print("Bind failed. Error : " + str(e))
    sys.exit()

# Le serveur écoute les connexions entrantes
server_socket.listen(10)
print(f"Server listening on {HOST}:{PORT}")

# Liste pour garder une trace des clients connectés
clients = []

# Fonction pour gérer les connexions client
def client_thread(conn, addr):
    conn.send("Welcome to the Chess League Server!".encode('utf-8'))
    
    while True:
        try:
            data = conn.recv(2048)
            reply = 'Server output: ' + data.decode('utf-8')
            print(reply)
            if not data:
                print(f"Connection with {addr} ended")
                break
            broadcast(data, conn)
        except:
            continue


# Fonction pour diffuser les messages à tous les clients connectés
def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

# Fonction pour retirer les clients de la liste
def remove(connection):
    if connection in clients:
        clients.remove(connection)

# Boucle principale pour accepter les connexions
while True:
    conn, addr = server_socket.accept()
    clients.append(conn)
    print(f"Connected to {addr}")
    t = threading.Thread(target=client_thread, args=(conn, addr))
    t.start()

server_socket.close()