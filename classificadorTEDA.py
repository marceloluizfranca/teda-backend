# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:28:59 2017

@author: RodrigoS
"""
from numpy import linalg as LA
from numpy import transpose as tp

class TEDA(object):
    
    def __init__(self, mu=0.0, var=0.0):
        self.mu = mu #média
        self.var = var #variância
        
        #the list to keep the cluster TEDA is
        #S = {[x y z] [x1 y1 zi] ...}
        #x = number of points of the cluster1
        #y = mean
        #z = variance
        
        #Two Cluster empty
        self.S = [[[], [0,0], 0], [[],[0,0],0]] 
        
    def addPoint(self, x, k, m):
        
        if k == 1:
            self.mu = x #Proprio ponto
            self.var = LA.norm(x)**2 #Distancia Euclidiana
            ksi = 2 #Valor da Zeta(T ou E)
        else:
            #algebrian to multply list for number
#            a = float((k-1))/k
#            b = [a * l for l in self.mu]
#            c = float(1)/k
#            d = [c * z for z in x]
#            e = b + d
#            f = zip(b,d)
#            h = [sum(g) for g in f] 
            #self.mu = (a * b) + (c * d)#            
#            zip([a * l for l in self.mu],[c * z for z in x])
#            [sum(g) for g in zip([a * l for l in self.mu],[c * z for z in x])]

            
            #self.mu = float(k-1)/k * float(self.mu) + float(1/k) * float(x)
            self.mu = [sum(c) for c in zip([(float((k-1))/k) * a for a in self.mu],[(float(1)/k) * b for b in x])]
            #LA.norm([x1 - x2 for (x1,x2) in zip(x,self.mu)])
            self.var = float(k - 1)/k * self.var + float(1/(k - 1)) * (LA.norm([a - b for (a,b) in zip(x,self.mu)])**2)
            
      
            #KSI TEM QUE SER UM NÚMERO
            x1 = [a - b for (a,b) in zip(self.mu,x)]
            x2 = [c * d for (c,d) in zip(x1,tp(x1))]
            x2 = sum(x2)
            x3 = (float(1)/k) + x2
            
            #ksi = (1/k) + ((obj.mu - x) * (obj.mu - x)') / (k * obj.var);          
            ksi = x3 / (k * self.var)
        
        
        
        zeta = float(ksi)/2
        
        thr = float((m**2 + 1))/(2*k)
        if (zeta > thr):
            f = 1
        else:
            f = 0
            
        
        #the list to keep the cluster TEDA is
        #S = {[x y z] [x1 y1 zi] ...}
        #x = number of points of the cluster1
        #y = mean
        #z = variance
        
        if (k == 1):
            self.S = [[x, self.mu, self.var], [[],[0,0],0]]
        else:
            if f == 0:
                self.S[0][0] = x
                self.S[0][1] = self.mu
                self.S[0][2] = self.var
            else:
                self.S[1][0] = x
                self.S[1][1] = self.mu
                self.S[1][2] = self.var
                    
        return zeta, thr, f
                
