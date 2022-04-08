import socket
import threading

# NOTA: LA IP DEBE MANDARSE COMO PARAMETRO
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

BUFFER_SIZE = 16384


def thread_client(soc_client, address):
    with open("100MB.txt", "rb") as f:
        while True:
            # leer los bytes del archivo
            data_read = f.read(BUFFER_SIZE)

            if not data_read:
                break

            # Enviar el paquete por el socket UDP
            soc_client.sendto(data_read, address)

    # Cerrar la conexion del socket
    soc_client.close()



serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

while True:
    (clientsocket, address) = serverSock.accept()
    threading.Thread(target=thread_client, args=(
        clientsocket, address)).start()
