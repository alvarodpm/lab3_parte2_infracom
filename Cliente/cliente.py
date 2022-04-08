import socket
import threading

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 16384

cant_clientes = 1

cant_threads = 0


def thread_cliente(clientSock, address):

    clientSock.sendto(b"Transmitir", address)

    # f = open('./archivos_recibidos/' + "archivo.txt", "wb")
    # while True:
    #     try:
    #         bytes_read, address = clientSock.recvfrom(BUFFER_SIZE)
    #     except socket.timeout as e:
    #         print(e)
    #         break
    #     print(bytes_read)
    #     print(bytes_read.decode())
    #     if(bytes_read):
    #         print("Sigo en el loop")
    #         f.write(bytes_read)
    #     else:
    #         print("No más looops")
    #         break
    # print("Salí del loop")
    with open('./archivos_recibidos/'+ "archivo.txt", "wb") as f:
            while True:
                bytes_read, address = clientSock.recvfrom(BUFFER_SIZE)
                print(bytes_read)
                print(bytes_read.decode())
                if(bytes_read == b"Archivo enviado completamente"):
                    break
                else:
                    f.write(bytes_read)
            print("Salí del loop")
    clientSock.close()
    print("Cerré el socket")

while cant_threads < cant_clientes:

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (UDP_IP_ADDRESS, UDP_PORT_NO)

    threading.Thread(target=thread_cliente, args=(clientSock, server_address, )).start()

    cant_threads += 1
