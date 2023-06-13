import socket
import threading

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion_servidor = ('localhost', 55555)
servidor.bind(direccion_servidor)

servidor.listen(2)
print(f'Server running on {direccion_servidor[0]}:{direccion_servidor[1]}')
print('Waiting for connection...\n')


def connection():
    try:
        # aceptamos el cliente
        cliente, direccion_cliente = servidor.accept()
        print('connection stablished from:', direccion_cliente, '\n')

        respuesta = 'Connected to server.'
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
            print('\n-Client disconnected.')
            cliente.close()
            break

        if datos:
            print('->',datos.decode())
        else:
            cliente.close()
            break

cliente = connection()
recv_messages(cliente)
