import socket
import threading

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 16384

cant_clientes = 1

cant_threads = 0

def thread_cliente(clientSock):
    clientSock.connect((UDP_IP_ADDRESS, UDP_PORT_NO))

    with open('./archivos_recibidos/'+ "archivo", "wb") as f:
            while True:
                bytes_read, address = clientSock.recvfrom(BUFFER_SIZE)
                clientSock.settimeout(60)
                f.write(bytes_read)

while cant_threads < cant_clientes:

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    threading.Thread(target=thread_cliente, args=(Client, ClientUDP, server_address, )).start()

    cant_threads += 1
