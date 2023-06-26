import socket
import threading
from colorama import Fore, Back, Style
from cryptography.fernet import Fernet
#---------------------------------------------------

clave = Fernet.generate_key()
cipher_suite = Fernet(clave)

direccion_servidor = ('localhost', 55555)

def receive_messages(cliente):
    while True:
        datos = cliente.recv(1024)
        
        if datos:
            desencriptado = fernet_object.decrypt(datos).decode()
            print(Fore.MAGENTA + '->' + Style.RESET_ALL,desencriptado)
        else:
            print('')
            cliente.close()
            break

def start_client():
    global fernet_object
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(direccion_servidor)
        print(Back.LIGHTBLUE_EX + Fore.BLACK + 'Connected to server.' + Style.RESET_ALL+  '\n')
        llave = cliente.recv(1024)
        fernet_object = Fernet(llave)
        cliente.send(clave)

    except ConnectionRefusedError:
        print('Error contacting server.')

    receive_thread = threading.Thread(target=receive_messages, args=(cliente,))
    receive_thread.start()

    while True:
        message = input('')
        if message != '':
            encriptado = cipher_suite.encrypt(message.encode())
            cliente.send(encriptado)

start_client()