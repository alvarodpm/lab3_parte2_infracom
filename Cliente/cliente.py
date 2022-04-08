import socket
import threading
import os

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 65536

cant_clientes = int(input("Número de clientes a conectar (Máximo 25): "))
cant_T_global = -1

def thread_cliente(clientSock, address):
    global cant_T_global
    cant_T_global +=1
    clientSock.sendto(b"Transmitir", address)
    print("Empieza a recibir el cliente " + str(cant_T_global))
    with open('./archivos_recibidos/'+ "Cliente" + str(cant_T_global) + "-Prueba" + str(cant_clientes) + ".txt", "wb") as f:
            while True:
                bytes_read, address = clientSock.recvfrom(BUFFER_SIZE)
                # print(bytes_read)
                # print(bytes_read.decode())
                if(bytes_read == b"Archivo enviado completamente"):
                    break
                else:
                    f.write(bytes_read)
            print("Salí del loop")
    clientSock.close()
    print("Cerré el socket")

cant_threads = 0
while cant_threads < cant_clientes:
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (UDP_IP_ADDRESS, UDP_PORT_NO)
    threading.Thread(target=thread_cliente, args=(clientSock, server_address, )).start()
    cant_threads += 1
