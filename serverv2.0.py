from ctypes.wintypes import HDC
import socket
import struct
import numpy as np
from DMCV2 import *
from ParametryzacjaRegulatora import *
from FOPDT import *
import time

s = socket.socket()
host = socket.gethostname()
port = 1024
Tc=1
Samples =[]
Time = []
data=[]

s.bind(('',port))
s.listen()

while True:  
            c, addr = s.accept()
            print("Connection accepted from " + repr(addr[1]))
            data = c.recv(50000)
            #if(data != 0):
            size=len(data)/4.0
            size = int(size)
            Samples = struct.unpack('<{}f'.format(size),data)
            print(Samples)
            data = c.recv(50000)
            size=len(data)/4.0
            size = int(size)
            Time = struct.unpack('<{}f'.format(size),data)
            print(Time)
            vector = ParametryzacjaRegulatora(Time,Samples)
            print(vector[0])
            print(vector[1])
            print(vector[2])
            Tc=vector[1]*0.1
            Hc,Hw,Hp,Hd,alfa = NastawyRegulatora(vector[0],vector[1]) #Wrzucić globalne TC!!
            Sampless = FOPDT(vector[1],vector[0],vector[2]/2,int(Hp),int(Hd))
            print(Sampless)
            ke, Ku = DMC_reg(Sampless,int(Hc),int(Hw),int(Hp),int(Hd),alfa)
            Ku.append(ke[0])
            Ku.append(round(vector[1],1))
            #print(Ku)
            rsize=len(Ku)
                #print(rsize)
            rdata = struct.pack('<{}f'.format(rsize), *Ku)
            c.send(rdata)
            #c.close()
            
