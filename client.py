import socket
import os

#constants
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
try:
  client_socket.connect((SERVER_HOST, SERVER_PORT))  
  print(f"[+] Connected to server at {SERVER_HOST}:{SERVER_PORT}")
except Exception as e:
    print("Could not connect to server:", e)
    exit(1)

# Menu for client options
def client_menu():
   while True:
       print("\nOptions:")
       print("1. Send a file")
       print("2. Request a file")
       print("3. View available files on server")
       print("4. Exit")
       choice = input("Choose an option: ")
       try:
           
          if choice == '1':
             client_socket.send("SEND".encode())
             send_file()
          elif choice == '2':
             client_socket.send("RECEIVE".encode())
             receive_file()
          elif choice == '3':
             client_socket.send("VIEW".encode())
             view_files()
          elif choice == '4':
             client_socket.close
             break
          else:
             print("Invalid choice. Try again.")
       except ConnectionAbortedError:
            print("Connection lost. Please reconnect.")
            break
       except Exception as e:
            print("An error occurred:", e)
            break
           
# Function to send a file to the server
def send_file():
     filename = input("Enter the filename to send: ")
     if os.path.isfile(filename):
        file_size = os.path.getsize(filename)
        client_socket.send(f"{filename}{SEPARATOR}{file_size}".encode())
        with open(filename, "rb") as file:
            while True:
                bytes_read = file.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        print(f"[+] File {filename} sent to the server.")
     else:
         print("File not found.")

         
# Function to receive a file from the server

def receive_file():
    filename = input("Enter the filename to request: ")
    try:
     client_socket.send(filename.encode())
     response = client_socket.recv(BUFFER_SIZE).decode()
     if "ERROR" not in response:
        filename, file_size = response.split(SEPARATOR)
        file_size = int(file_size)
        with open(f"downloaded_{filename}", "wb") as file:
            bytes_received = 0
            while bytes_received < file_size:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
                bytes_received += len(data)
        print(f"[+] File {filename} downloaded as downloaded_{filename}.")
     else:
       print(response)
    except ConnectionAbortedError as e:
        print("Error: Connection was aborted by the host machine.")
        print(e)
    except Exception as e:
        print("An unexpected error occurred while receiving the file:", e)
       
# Function to view available files on the server
def view_files():
 try:
    files_list = client_socket.recv(BUFFER_SIZE).decode()
    print("\nAvailable files on server:")
    print(files_list)
 except ConnectionAbortedError as e:
        print("Error: Connection was aborted while viewing files.")
        print(e)
 except Exception as e:
        print("An error occurred while retrieving file list:", e)
#start client menu
client_menu()
client_socket.close()
