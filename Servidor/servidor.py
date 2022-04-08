import socket
import threading

# NOTA: LA IP DEBE MANDARSE COMO PARAMETRO
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 16384


def thread_client(soc_client):
    global UDP_PORT_NO
    try:
        print("Antes del exception")
        print(soc_client)
        print(soc_client.recvfrom(1024))
        msg, address = soc_client.recvfrom(1024)
        print("Address:")
        print(address)
    except Exception as e:
        print("Hey, un error")
        print(e)
    UDP_PORT_NO += 1
    print("address:",address)
    with open("./archivos/100MB.txt", "rb") as f:
        while True:
            # leer los bytes del archivo
            data_read = f.read(BUFFER_SIZE)

            if not data_read:
                break

            # Enviar el paquete por el socket UDP
            soc_client.sendto(data_read, address)

    # Cerrar la conexion del socket
    soc_client.close()



while True:
    print("Escuchando clientes")
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    print("hey1")
    msg, address = serverSock.recvfrom(1024)
    print("hey2")
    threading.Thread(target=thread_client, args=(
        serverSock,)).start()
    print(UDP_PORT_NO)
