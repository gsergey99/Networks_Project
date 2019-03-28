#!/usr/bin/python3.7
import struct
import pickle
import sys
from socket import *

def read(sock,unpacked_code,port):
    block=0
    f=open(unpacked_code[1],'rb') #ABRIMOS EL ARCHIVO QUE EL CLIENTE HABIA MANDADO 
    while True:
        recieve=False
        try:
            block=block+1 #incrementamos el block number por cada mensaje que el servidor envía
            
            if not recieve: 
                sent_bytes=f.read(512)
                sock.sendto(struct.pack(f'=2H{len(sent_bytes)}p',3,block,sent_bytes ('',port))) #MANDAMOS LA ESTRUCTURA DEL LOS DATOS QUE LEEMOS DEL FICHERO
                msg, client=sock.recvfrom(512) #EL SERVIDOR RESCIBE EL ACK DEL CLIENTE
            else:
                sock.sendto(struct.pack(f'=2H{len(sent_bytes)}p',3,block-1,sent_bytes ('',port))) #MANDAMOS DE NUEVO EL PAQUETE PARA QUE LO PUEDA RECIBIR EL CLIENTE
        except sock.timeout:
            recieve=True
        except IOError:
            message='FILE NOT FOUND'
            sock.sendto(struct.pack(f'=2H{len(message)}pH',5,1,message,0) ('',port))
            sock.close()    ##en el caso de error se tendría que mandar un mensaje que contenga los siguiente y pot supuesto cerrar el SERVIDOR

        finally:
            sock.close()

def write(sock,unpacked_code,port):
    block=0
    f=open(unpacked_code[1],'wb')
    sock.sendto(struct.pack('=HB',4,block ('',port)))
    acknowledgment=False
    while True:
        try:
            
            if not acknowledgment:
                msg,client=sock.recvfrom(516)
                unpacked_data = struct.unpack(f'Hp{len(msg)-4}s',msg)
                write(unpacked_data[2])
                sock.sendto(struct.pack('=HB',4,unpacked_data[2]) ('',port))
            else:
                sock.sendto(struct.pack('=HB',4,unpacked_data[2]-1) ('',port))
        except sock.timeout:
            acknowledgment=True
        except IOError:
            message='FILE NOT FOUND'
            sock.sendto(struct.pack(f'=2H{len(message)}pB',5,2,message,0)('',port))
            sock.close()



def main(*args,**kwargs):

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(20)
    sock.bind(('',int(sys.argv[1])))
    msg, client =sock.recvfrom(516) #RECIBIMOS EL PAQUETE QUE EL SERVIDOR MANDA, LA CANTIDAD DE DATOS TIENE QUE SER EL APROPIADO PARA QUE NO HAYA RESTRICCIONES
    unpacked_code = struct.unpack(f"!H{len(msg)-12}sB{len('netascii')}sB",msg)
    if(unpacked_code[0]==1):
        read(sock,unpacked_code,int(sys.argv[1]))
    if(unpacked_code[0]==2):
        write(sock,unpacked_code,int(sys.argv[1]))


if __name__ == '__main__':
    try:
      sys.exit(main())
    except KeyboardInterrupt:
      pass
