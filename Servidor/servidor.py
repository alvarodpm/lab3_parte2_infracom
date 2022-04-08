import socket
import threading
import os

# NOTA: LA IP DEBE MANDARSE COMO PARAMETRO
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 16384

#Número de clientes a conectar
cant_clientes = int(input("Número de clientes a conectar (Máximo 25): "))

def print_files():
    files_server = os.listdir('./archivos/')
    print("Los archivos que estan disponibles en el servidor son:")
    for i in range (len(files_server)):
        print(str(i+1) + ". " + files_server[i])

print_files()
num_archivo = int(input("Seleccione el archivo a enviar: "))
nombre_archivo = ''

if(num_archivo == 1):
    nombre_archivo = '100MB.txt'
elif(num_archivo == 2):
    nombre_archivo = 'test.txt'

#Número de threads ejecutandose
cant_threads = 0

def thread_client(soc_client, address):
    
    global cant_threads
    print("address: ",address)
    with open("./archivos/" + nombre_archivo , "rb") as f:
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

#Contador del número de Threads local para el While
ThreadCountWhile = 1

while ThreadCountWhile <= cant_clientes:
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    print("Esperando conexión de un cliente")
    msg, address = serverSock.recvfrom(1024)
    print("Un cliente se conectó")
    threading.Thread(target=thread_client, args=(
        serverSock, address)).start()
    print("Número del Thread: " + str(ThreadCountWhile) + " puerto: " + str(UDP_PORT_NO))
    ThreadCountWhile +=1
    UDP_PORT_NO += 1
