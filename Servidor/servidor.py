import socket
import threading
import os
import datetime
import time

# NOTA: LA IP DEBE MANDARSE COMO PARAMETRO
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
BUFFER_SIZE = 16384
datos_envios = []

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
bytes_archivo = ""

if(num_archivo == 1):
    nombre_archivo = '100MB.txt'
    bytes_archivo = "104857600"
elif(num_archivo == 2):
    nombre_archivo = '250MB.txt'
    bytes_archivo = "262144000"
elif(num_archivo == 3):
    nombre_archivo = "test.txt"
    bytes_archivo = "26"

#Número de threads ejecutandose
cant_threads = 0

def thread_client(soc_client, address, num_cliente):
    
    global cant_threads
    print("address: ",address)
    time_start = datetime.datetime.now()
    bytes_enviados = 0
    with open("./archivos/" + nombre_archivo , "rb") as f:
        while True:
            # leer los bytes del archivo
            data_read = f.read(BUFFER_SIZE)
            if not data_read:
                break
            # Enviar el paquete por el socket UDP
            soc_client.sendto(data_read, address)
            bytes_enviados += len(data_read)
    time_end = datetime.datetime.now()
    time_spent = time_end - time_start
    soc_client.sendto(b"Archivo enviado completamente", address)
    datos_envios.append({"tiempo_transferencia":time_spent, "num_cliente": num_cliente, "bytes_enviados":bytes_enviados})
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
        serverSock, address, ThreadCountWhile)).start()
    print("Número del Thread: " + str(ThreadCountWhile) + " puerto: " + str(UDP_PORT_NO))
    ThreadCountWhile +=1
    UDP_PORT_NO += 1

def ingresar_cliente_a_logs(archivo, num_cliente, nombre_archivo, bytes_archivo, bytes_enviados, tiempo_transferencia):
    archivo.write("----------------Cliente {}----------------\n".format(str(num_cliente)))
    archivo.write("Nombre del archivo enviado: " + str(nombre_archivo) + "\n")
    archivo.write("Cantidad de bytes del archivo: " + str(bytes_archivo) + "\n")
    archivo.write("Cantidad de bytes enviados: " + str(bytes_enviados) + "\n")
    archivo.write("Tiempo de transferencia: " + str(tiempo_transferencia) + "\n")

fecha = datetime.datetime.now()
nombre_archivo_logs = "{}-{}-{}-{}-{}-{}-{}-{}-log.txt".format(str(fecha.year), str(fecha.month), str(fecha.day), str(fecha.hour), str(fecha.minute), str(fecha.second), str(fecha.microsecond), str(cant_clientes))
archivo = open("../Logs/Servidor/{}".format(nombre_archivo_logs), "w")

while len(datos_envios) < cant_clientes:
    time.sleep((cant_clientes - len(datos_envios)) * 3)

for e in datos_envios:
    ingresar_cliente_a_logs(archivo, e["num_cliente"], nombre_archivo, bytes_archivo, e["bytes_enviados"], e["tiempo_transferencia"])

archivo.close()
