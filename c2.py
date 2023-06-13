import socket
import threading

direccion_servidor = ('localhost', 55555)

def receive_messages(cliente):
    while True:
        datos = cliente.recv(1024)
        if datos:
            print('->',datos.decode())
        else:
            cliente.close()
            break

def start_client():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(direccion_servidor)

    except ConnectionRefusedError:
        print('Error contacting server.')

    receive_thread = threading.Thread(target=receive_messages, args=(cliente,))
    receive_thread.start()

    while True:
        message = input('')
        cliente.send(message.encode())

start_client()
