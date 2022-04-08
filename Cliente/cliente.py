import socket
import threading
import os
import datetime
import time

UDP_IP_ADDRESS = input("Ingrese la IP del equipo donde se encuentra el servidor UDP: ")
UDP_PORT_NO = 6789
BUFFER_SIZE = 65536
datos_envios = []

cant_clientes = int(input("Número de clientes a conectar (Máximo 25): "))
cant_T_global = 0

def print_files():
    files_server = os.listdir('../Servidor/archivos/')
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



def thread_cliente(clientSock, address):
    global cant_T_global
    cant_T_global +=1
    clientSock.sendto(b"Transmitir", address)
    print("Empieza a recibir el cliente " + str(cant_T_global))
    bytes_recibidos = 0
    time_start = datetime.datetime.now()
    with open('./archivos_recibidos/'+ "Cliente" + str(cant_T_global) + "-Prueba" + str(cant_clientes) + ".txt", "wb") as f:
            while True:
                bytes_read, address = clientSock.recvfrom(BUFFER_SIZE)
                if(bytes_read == b"Archivo enviado completamente"):
                    break
                else:
                    bytes_recibidos += len(bytes_read)
                    f.write(bytes_read)
            print("Salí del loop")
    time_end = datetime.datetime.now()
    time_spent = time_end - time_start
    clientSock.close()
    print("Cerré el socket {}".format(str(cant_T_global)))
    datos_envios.append({"tiempo_transferencia":time_spent, "num_cliente": cant_T_global, "bytes_recibidos":bytes_recibidos})

cant_threads = 0
while cant_threads < cant_clientes:
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (UDP_IP_ADDRESS, UDP_PORT_NO)
    threading.Thread(target=thread_cliente, args=(clientSock, server_address, )).start()
    UDP_PORT_NO +=1
    time.sleep(1)
    cant_threads += 1

def ingresar_cliente_a_logs(archivo, num_cliente, nombre_archivo, bytes_archivo, bytes_recibidos, tiempo_transferencia):
    print("Voy a escribir algo :)")
    archivo.write("----------------Cliente {}----------------\n".format(str(num_cliente)))
    archivo.write("Nombre del archivo enviado: " + str(nombre_archivo) + "\n")
    archivo.write("Cantidad de bytes del archivo: " + str(bytes_archivo) + "\n")
    archivo.write("Cantidad de bytes recibidos: " + str(bytes_recibidos) + "\n")
    archivo.write("Tiempo de transferencia: " + str(tiempo_transferencia) + "\n")

fecha = datetime.datetime.now()
nombre_archivo_logs = "{}-{}-{}-{}-{}-{}-{}-{}-log.txt".format(str(fecha.year), str(fecha.month), str(fecha.day), str(fecha.hour), str(fecha.minute), str(fecha.second), str(fecha.microsecond), str(cant_clientes))
archivo = open("../Logs/Cliente/{}".format(nombre_archivo_logs), "w")
print(archivo)
while len(datos_envios) < cant_clientes:
    time.sleep((cant_clientes - len(datos_envios)) * 3)

print(datos_envios)
for e in datos_envios:
    ingresar_cliente_a_logs(archivo, e["num_cliente"], nombre_archivo, bytes_archivo, e["bytes_recibidos"], e["tiempo_transferencia"])

archivo.close()