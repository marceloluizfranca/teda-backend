import netflow
import socket, struct
import time
import collections
import math
import numpy as np
import requests

import classificadorTEDA as cltd
import matplotlib.pyplot as plt
import matplotlib.style as stl
import matplotlib.ticker as ticker

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 2055))

#TEDA Parameters
m = 0.5 #TEDA Adjustment Variable most likely at the threshold
k = 1
teda = cltd.TEDA() #Loading TEDA class
interval = 1 # time in seconds

#Variables for TEDA result
zeta = []
threshold = []
falhateda = []

#Temporary variables
param01 = []
param02 = []

def calc_entropy(data):
    #Calculate entropy according to "Mining Anomalies Using Traffic Feature Distributions"
    counter = collections.Counter(str(data))
    S = sum(counter.values())
    H = []
    for j in counter.values():
        H.append(j/float(S)*math.log(j/float(S),2))
    H = -sum(H)
    return H

def return_IP(raw):
    return socket.inet_ntoa(struct.pack('!L', raw))

start = time.time()
stop = time.time() + 1200
flag = []

while True: # (time.time() < stop) :
    
    payload, client = sock.recvfrom(1464)  # 4096 is experimental, tested with 1464 
    p = netflow.parse_packet(payload)  # Test result: <ExportPacket v5 with 30 records>
    flag.append(p.header.timestamp)

    if flag[-1] - flag[0] < interval:
    
        for flow in p.flows:

            ### Possible fields
            #flow.SRC_AS
            #flow.DST_AS
            #flow.SRC_PORT
            #flow.DST_PORT
            #flow.IN_OCTETS
            #flow.IN_PACKETS
            #flow.IPV4_SRC_ADDR
            #flow.IPV4_DST_ADDR
            #flow.PROTO
            #flow.TCP_FLAGS

            param01.append(flow.SRC_PORT)
            param02.append(flow.DST_PORT)

    else:

        x = [ calc_entropy(param01), calc_entropy(param02)]
        tempzeta,tempthr,tempf = teda.addPoint(x,k,m)
        zeta.append(tempzeta)
        threshold.append(tempthr)
        falhateda.append(tempf)
        k = k + 1
        flag = []    
        param01 = []
        param02 = []
        print(f'Zeta: {tempzeta} - Threshold: {tempthr} - PORT_SRC_ENTROPY: {x[0]} - PORT_DST_ENTROPY: {x[1]}')
        resp = requests.get(f'http://localhost:3000/graph/{tempzeta}/{tempthr}')

        """
        #Plot Zeta e Threshold
        plt.yscale('log')
        plt.locator_params(axis='x', nbins=10)
        plt.plot(zeta, label="zeta")
        plt.plot(threshold, label="threshold")
        plt.legend(loc='upper right', shadow=True)
        plt.title(f'TEDA - Realtime')
        plt.xlabel(f'time in seconds')
        plt.ylabel(f'entropy')
        plt.grid(linestyle='-', linewidth='0.5')
        plt.draw()
        plt.pause(0.001)
        plt.clf()
        
        

#Plot Zeta e Threshold
plt.yscale('log')
plt.locator_params(axis='x', nbins=10)
plt.plot(zeta, label="zeta")
plt.plot(threshold, label="threshold")
plt.legend(loc='upper right', shadow=True)
plt.title(f'TEDA - Realtime')
plt.xlabel(f'time in seconds')
plt.ylabel(f'entropy')
plt.grid(linestyle='-', linewidth='0.5')
#plt.draw()
plt.show()
#plt.pause(0.001)
plt.clf()
"""
