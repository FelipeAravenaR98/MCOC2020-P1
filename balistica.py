import scipy as sp
from scipy.integrate import odeint
from matplotlib import pyplot as plt

ro = 1.225 
cd = 0.47
cm = 0.01
inch = 2.54*cm
D = 8.5*inch
r=D/2
A = sp.pi*r**2

m=15.

CD = 0.5*ro*cd*A
g=9.81

#funcion a integrar

def bala(z,t):   
    zp = sp.zeros(4)
    
    zp[0]=z[2]
    zp[1]=z[3]
    
    v=z[2:4]
    v[0] = v[0] - V
    v2=sp.dot(v,v)
    vnorm=sp.sqrt(v2)
    FD=-CD * v2 * (v/vnorm)
    zp[2]==FD[0]/m
    zp[3]=FD[1]/m-g
    
    return zp

V=[0,10.0,20.0]

for a in V:
    V=a
    t = sp.linspace(0,30,1001)
    
    vi=100*1000./3600.
    
    z0=sp.array([0,0,vi,vi]) #velocidad en x e y = 0
    
    sol=odeint(bala,z0,t)
    
    x = sol[:,0]
    y = sol[:,1]
    
    plt.figure(1)
    plt.axis([0,160,0,50])
    plt.plot(x,y,label= f"V = {a} m/s")
    
plt.legend()
plt.grid(True)
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title('Trayectoria para distintos vientos')
plt.show



