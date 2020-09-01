from scipy.integrate import odeint
from scipy import sin, cos
from matplotlib.pylab import *
from datetime import datetime


a = 2.

def eulerint(solucion_odeint,z0,t,Nsub):    #Funcion hecha en clases
    Nt = len(t)
    Ndim = len(array(z0))
    z = zeros((Nt,Ndim))
    
    z[0,:] = z0
    
    for i in range(1,Nt):
        t_anterior = t[i-1]
        dt = (t[i] - t[i-1]) / Nsub
        z_temp = z[i-1,:]
        for k in range(Nsub):
            z_temp +=  dt * solucion_odeint(z_temp, t_anterior+k*dt)
        z[i,:] = z_temp
        
    return z

kg = 1
m = 1*kg
f = 1 #Hz
e = 0.2
w = 2 * pi * f
k = m * w**2
c = 2 * e * w * m

def dy(z,t):                                # Función para zp
    zp = array([z[1] ,  -( 2 * ( c / (2 * m)) * z[1] ) - ( z[0] * (w**2) ) ])
    return zp




def zp(z,t):            #funcion hecha en clases
    
    return z*a



z0 =array( [1. , 1.] )
t = linspace(0 , 10. , 1000.)



z_odeint = odeint(dy, z0, t)

real = 1. * exp(-c*t/(2))*cos(w*t)
 

plot(t,real, color = "black", label = "Real", linewidth = 2)
plot(t,z_odeint[:,0], color = "royalblue", label = "Odeint")




colores = ["mediumseagreen" , "red" , "darkorange"]
subdivisiones = [1 , 10 , 100]

for a in range(3):
    x = subdivisiones[a]
    z_euler = eulerint(dy, z0, t, Nsub = subdivisiones[a])
    plot(t , z_euler[:,0] , color = colores[a], label = f" Euler con subdivision {subdivisiones[a]}")
    
    
legend()
show()




