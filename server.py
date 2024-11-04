
import socket
import threading
import os

# Constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# Function to handle client connections

def handle_client(client_socket, address):
    print(f"[+] Client {address} connected.")
    while True:
        try:
            command = client_socket.recv(BUFFER_SIZE).decode()
            if command == 'SEND':
                receive_file(client_socket)
            elif command == 'RECEIVE':
                send_file(client_socket)
            elif command == 'VIEW':
                send_file_list(client_socket)
            else:
                break
        except Exception as e:
            print(f"[!] Error: {e}")
            break
    client_socket.close()
    print(f"[-] Client {address} disconnected.")

    
# Function to send files to the client
def send_file(client_socket):
  try:
    filename = client_socket.recv(BUFFER_SIZE).decode()
    if os.path.isfile(filename):
        file_size = os.path.getsize(filename)
        client_socket.send(f"{filename}{SEPARATOR}{file_size}".encode())
        with open(filename, 'rb') as file:
            while True:
                bytes_read = file.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        print(f"[+] File {filename} sent to client.")
    else:
        client_socket.send("ERROR: File not found.".encode())
  except Exception as e:
        print(f"[!] Error sending file to client: {e}")

        
# Function to receive files from the client
def receive_file(client_socket):
  try:
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, file_size = received.split(SEPARATOR)
    file_size = int(file_size)
    with open(f"received_{filename}", "wb") as file:
        bytes_received = 0
        while bytes_received < file_size:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            file.write(data)
            bytes_received += len(data)
    print(f"[+]File {filename} received and saved as received_{filename}.")
  except Exception as e:
        print(f"[!] Error receiving file from client: {e}")
    
# Function to send a list of files to the client
def send_file_list(client_socket):
  try:
    files = os.listdir('.')
    files_list = "\n".join(files)
    client_socket.send(files_list.encode())
  except Exception as e:
        print(f"[!] Error receiving file from client: {e}")
    
# Accept client connections in a loop
while True:
  try:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
  except Exception as e:
        print(f"[!] Error accepting client connection: {e}")
