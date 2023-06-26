import socket
import threading
from colorama import Fore, Back, Style
from cryptography.fernet import Fernet
#---------------------------------------------------

clave = Fernet.generate_key()
cipher_suite = Fernet(clave)

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion_servidor = ('localhost', 55555)
servidor.bind(direccion_servidor)

servidor.listen(1)
print(Back.GREEN + Fore.BLACK + f'\nServer running on {direccion_servidor[0]} : {direccion_servidor[1]}' + Style.RESET_ALL)
print('Waiting for connection...\n')


def connection():
    global cliente
    global fernet_object
    try:
        # aceptamos el cliente
        #Utilizamos colorama para darle color al print de conexión establecida.
        cliente, direccion_cliente = servidor.accept()
        print(Back.LIGHTBLUE_EX + Fore.BLACK +'connection stablished from:', direccion_cliente, '\n' + Style.RESET_ALL)
        cliente.send(clave)
        llave = cliente.recv(1024)
        fernet_object = Fernet(llave)

    except:
        pass
    #salimos de la función.

def send_messages():
    while True:
        message = input('')
        if message != '':
            encriptado = cipher_suite.encrypt(message.encode())
            cliente.send(encriptado)

def recv_messages():
    send = threading.Thread(target=send_messages)
    send.start()

    while True:
        # Aquí es donde recibe los datos del cliente.
        try:
            datos = cliente.recv(1024)
        
        except:
            msg = '\n' + Back.RED + Fore.BLACK + 'Server has close.' + Style.RESET_ALL + '\n'
            encr = cipher_suite.encrypt(msg.encode())
            cliente.sendall(encr)
            cliente.close()
            break

        if datos:
            desencriptado = fernet_object.decrypt(datos).decode()
            print(Fore.MAGENTA + '->' + Style.RESET_ALL,desencriptado)
        else:
            cliente.close()
            break

connection()
recv_messages()