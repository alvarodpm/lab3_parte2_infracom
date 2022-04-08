import socket
import threading

# NOTA: LA IP DEBE MANDARSE COMO PARAMETRO
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 16384


def thread_client(soc_client, address):
    global UDP_PORT_NO
    UDP_PORT_NO += 1
    print("address:",address)
    with open("./archivos/test.txt", "rb") as f:
        while True:
            # leer los bytes del archivo
            data_read = f.read(BUFFER_SIZE)

            if not data_read:
                break

            # Enviar el paquete por el socket UDP
            soc_client.sendto(data_read, address)

    soc_client.sendto(b"Archivo enviado completamente", address)
    print("Terminé de enviar todo el archivo")

    # Cerrar la conexion del socket
    soc_client.close()



while True:
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    print("Esperando conexión de un cliente")
    msg, address = serverSock.recvfrom(1024)
    print("Un cliente se conectó")
    threading.Thread(target=thread_client, args=(
        serverSock, address)).start()
    print(UDP_PORT_NO)
