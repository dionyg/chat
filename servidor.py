import socket
import threading
from colorama import Fore, Back, Style

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion_servidor = ('192.168.0.106', 55555)
servidor.bind(direccion_servidor)

servidor.listen(1)
print(Back.GREEN + Fore.BLACK + f'\nServer running on {direccion_servidor[0]} : {direccion_servidor[1]}' + Style.RESET_ALL)
print('Waiting for connection...\n')


def connection():
    try:
        # aceptamos el cliente
        #Utilizamos colorama para darle color al print de conexión establecida.
        cliente, direccion_cliente = servidor.accept()
        print(Back.LIGHTBLUE_EX + Fore.BLACK +'connection stablished from:', direccion_cliente, '\n' + Style.RESET_ALL)

        respuesta = Back.LIGHTBLUE_EX + Fore.BLACK + 'Connected to server.' + Style.RESET_ALL+  '\n'
        cliente.send(respuesta.encode())
        return cliente

    except:
        print('Error.')
    #salimos de la función.

def send_messages():
    while True:
        message = input('')
        if message != '':
            cliente.send(message.encode())


def recv_messages(cliente):

    send = threading.Thread(target=send_messages)
    send.start()

    while True:
        # Aquí es donde recibe los datos del cliente.
        try:
            datos = cliente.recv(1024)
        
        except ConnectionResetError:
            print(Back.RED + Fore.WHITE + '\n-Client disconnected.')
            cliente.close()
            break

        if datos:
            print('->',datos.decode())
        else:
            cliente.close()
            break

cliente = connection()
recv_messages(cliente)