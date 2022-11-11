import numpy as np
from array import *
import control
from scipy.optimize import minimize
from Fop import *

def ParametryzacjaRegulatora(T,Samp):
    D = len(Samp)
    T = list(T)
    for i in range (0,D-1):
        T[i] = round(T[i],1)
    k = (Samp[D-1]-Samp[0])
    X = [k,5,5]
    k,T,T0 = minimize(err,X,args=(T,Samp)).x
    return [T0, T, k]

def foptd(t, K=1, tau=1, tau_d=0):
    tau_d = max(0,tau_d)
    tau = max(0,tau)
    return np.array([K*(1-np.exp(-(t-tau_d)/tau)) if t >= tau_d else 0 for t in t])

def err(X,t,y):
    K,tau,tau_d = X
    z = foptd(t,K,tau,tau_d)
    iae = sum(abs(z-y))*(max(t)-min(t))/len(t)
    return iae

def NastawyRegulatora(T0,T):
    Tp = 0.1 * T
    Tp = round(Tp,1)
    Hc = 2
    Hw = np.floor(T0/Tp + 1)
    Hp = np.around(T/Tp + T0/Tp)
    Hd = np.around((3*T)/Tp + T0/Tp)
    x = 0.0146/(1+(T0/T))
    k= 0.85
    alfa = x*(np.power(k,2)*Hp) 
    return Hc,Hw,Hp,Hd,alfa