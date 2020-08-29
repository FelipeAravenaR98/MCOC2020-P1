import scipy as sp
from scipy.integrate import odeint
from scipy import sin, cos
import matplotlib.pylab as plt
from datetime import datetime

# Parámetros de la tierra

G = 6.674e-11                   # Unidad [Nm2 / Kg2]
mt = 5.972e24                 # Unidad [Kg]
om = 7.27e-5                 # Unidad [rad / s] 
atmosfera =  6451000



rtierra = 6371000
rtotal = 7071000                

ti = "2020-08-07T22:59:42.000000"
ti = ti.split("T")
ti = "{} {}".format(ti[0],ti[1])
ti = datetime.strptime(ti, '%Y-%m-%d %H:%M:%S.%f')

tf = "2020-08-09T00:59:42.000000"
tf = tf.split("T")
tf = "{} {}".format(tf[0],tf[1])
tf = datetime.strptime(tf, '%Y-%m-%d %H:%M:%S.%f')

deltaT = (tf-ti).total_seconds()

# Los datos son los siguientes

#<TAI>TAI=2020-08-07T23:00:19.000000</TAI>
#<UTC>UTC=2020-08-07T22:59:42.000000</UTC>
#<UT1>UT1=2020-08-07T22:59:41.796956</UT1>
#<Absolute_Orbit>+33807</Absolute_Orbit>
#<X unit="m">-1300354.318621</X>
#<Y unit="m">1000042.793928</Y>
#<Z unit="m">6872663.396330</Z>
#<VX unit="m/s">-1692.331483</VX>
#<VY unit="m/s">7262.981572</VY>
#<VZ unit="m/s">-1374.216961</VZ>

x_i = -1300354.318621
y_i = 1000042.793928
z_i = 6872663.396330
vx_i = -1692.331483 
vy_i = 7262.981572                     
vz_i = -1374.216961

#<X unit="m">-2034623.889145</X>
#<Y unit="m">-5920783.955308</Y>
#<Z unit="m">3289503.706424</Z>
#<VX unit="m/s">-449.399307</VX>
#<VY unit="m/s">3809.729180</VY>
#<VZ unit="m/s">6556.395258</VZ>

x_f = 1757541.908660
y_f = 6851804.667799
z_f = 209566.915093
vx_f = 1591.064635
vy_f = -171.465449
vz_f = -7426.871314

t = sp.linspace(0, deltaT, 9361)
z0 = sp.array([x_i, y_i, z_i, vx_i, vy_i, vz_i]) 


def satelite(z,t):   #z = [x,y,vx,vy]
    zp = sp.zeros(6)
    c = sp.cos(om*t)
    s = sp.sin(om*t)
    R = sp.array([
      [c,s,0],
      [-s,c,0],
      [0,0,1]])
    
    Rp =om* (sp.array([
      [-s,c,0],
      [-c,-s,0],
     [ 0,0,0]]))
    
    Rpp = (om**2)* (sp.array([
        [-c,-s,0],
        [s,-c,0],
        [0,0,0]]))
    
    z1 = z[0:3]
    z2 = z[3:6]
    
    r2 = sp.dot(z1,z1)
    r = sp.sqrt(r2)
    
    Fg = (-G*mt/r**2)- (R@(z1/r))
    
    zp[0:3] = z2
    zp[3:6] = R.T@(Fg-(2*(Rp@z2) + (Rpp@z1)))
    return zp

sol = odeint(satelite,z0,t)

x = sol[:,0:3]

pos_final = sp.array([x_f, y_f, z_f, vx_f, vy_f, vz_f]) - sol[-1]

vector=[]
for el in range(len(pos_final)-3):
    vector.append(pos_final[el])
    
print (sp.sqrt((vector[0]**2) + (vector[1]**2) + (vector[2]**2) )) 
    
    
    
    
    
    
    
    
    
    
    
    
