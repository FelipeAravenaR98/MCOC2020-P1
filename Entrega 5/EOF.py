import xml
import xml.etree.ElementTree as ET
from numpy import zeros
import datetime as dt
from matplotlib.pylab import *
from scipy.integrate import odeint
from sys import argv


#https://docs.python.org/3/library/xml.etree.elementtree.html

def utc2time(utc, ut1, EOF_datetime_format = "%Y-%m-%dT%H:%M:%S.%f"):
	t1 = dt.datetime.strptime(ut1,EOF_datetime_format)
	t2 = dt.datetime.strptime(utc,EOF_datetime_format)
	return (t2 - t1).total_seconds()


def leer_eof(fname):
	tree = ET.parse(fname)
	root = tree.getroot()

	Data_Block = root.find("Data_Block")		
	List_of_OSVs = Data_Block.find("List_of_OSVs")

	count = int(List_of_OSVs.attrib["count"])

	t = zeros(count)
	x = zeros(count)
	y = zeros(count)
	z = zeros(count)
	vx = zeros(count)
	vy = zeros(count)
	vz = zeros(count)

	set_ut1 = False
	for i, osv in enumerate(List_of_OSVs):
		UTC = osv.find("UTC").text[4:]
		
		x[i] = osv.find("X").text   #conversion de string a double es implicita
		y[i] = osv.find("Y").text
		z[i] = osv.find("Z").text
		vx[i] = osv.find("VX").text
		vy[i] = osv.find("VY").text
		vz[i] = osv.find("VZ").text

		if not set_ut1:
			ut1 = UTC
			set_ut1 = True

		t[i] = utc2time(UTC, ut1)

	return t, x, y, z, vx, vy, vz
"""
-----------------------------------------------------------------
            HASTA ACÁ LLEGA EL CODIGO ENTREGADO
-----------------------------------------------------------------
"""

nombre_eof = argv[1]        "S1A_OPER_AUX_POEORB_OPOD_20200828T121249_V20200807T225942_20200809T005942.EOF"
t, x, y, z, vx, vy, vz = leer_eof(nombre_eof)

z0 = array([x[0], y[0], z[0], vx[0], vy[0], vz[0]]) #Condicion inicial
zf = array([x[-1], y[-1], z[-1], vx[-1], vy[-1], vz[-1]]) #Condicion final

# Para hacer la prediccion


# Parámetros de la tierra
km = 1000.
km3 = (km)**3
km5 = (km)**5
km6 = (km)**6
G = 6.674e-11                   # Unidad [Nm2 / Kg2]
mt = 5.972e24                 # Unidad [Kg]
om = -7.2921150e-5                # Unidad [rad / s] 
atmosfera =  6451000
mu = 398600.440*km3
rtierra = 6371*km
rtotal = 7071*km

zp = zeros(6)
def zpunto(z,t):
    c = cos(om*t)
    s = sin(om*t)
    R = array([
      [c,s,0],
      [-s,c,0],
      [0,0,1]])
    
    Rp =om* (array([
      [-s,c,0],
      [-c,-s,0],
     [ 0,0,0]]))
    
    Rpp = (om**2)* (array([
        [-c,-s,0],
        [s,-c,0],
        [0,0,0]]))
    
    z1 = z[0:3]
    z2 = z[3:6]
    
    r2 = dot(z1,z1)
    r = sqrt(r2)
    
    Fg = (-G*mt/r**2)* (R@(z1/r))
    
    zp[0:3] = z2
    zp[3:6] = R.T@(Fg-(2*(Rp@z2) + (Rpp@z1)))
    return zp

def eulerint(zp, z0, t, Nsub = 1):
    Nt = len(t)
    Ndim = len(array([z0]))
    
    z = zeros((Nt, 6))
    
    z[0,:] = z0
    
    for i in range(1,Nt):
        t_anterior = t[i-1]
        dt = (t[i]-t[i-1]) / Nsub
        z_temp = z[i-1, : ].copy()
        for a in range(Nsub):
            z_temp +=  dt * zp(z_temp,t_anterior + a * dt)
        z[i,:] = z_temp
            
    return z 


sol_odeint = odeint(zpunto,z0,t)
sol_eulerint = eulerint(zpunto, z0, t, Nsub = 1)

pos_final =zf - sol_odeint[-1]

#aca lo que hare es comparar en todos los tiempos la posicion real con la predicha que obtuve con odeint
#en el vector delta tendre las distancias entre la posicion real y la predicha. Este vector lo quiero 
#graficar en funcion del tiempo porque es el grafico pedido

vector_delta = []
for a in range(len(t)):
    pos_actual = array([x[a], y[a], z[a], vx[a], vy[a], vz[a]])
    diferencia = pos_actual-sol_odeint[a]

#ahora obtengo solo los 3 primeros valores porque son los de posicion y el resto son de velocidad q no me importan
    vector=[] 
    for el in range(len(diferencia)-3):
        vector.append(diferencia[el])
        
    vector_delta.append(sqrt((vector[0]**2) + (vector[1]**2) + (vector[2]**2) ))



#Acá hago lo mismo que antes pero para el caso de eulerint
    
vector_delta2 = []
for a in range(len(t)):
    pos_actual = array([x[a], y[a], z[a], vx[a], vy[a], vz[a]])
    diferencia = pos_actual-sol_eulerint[a]   

#ahora obtengo solo los 3 primeros valores porque son los de posicion y el resto son de velocidad q no me importan
    vector=[] 
    for el in range(len(diferencia)-3):
        vector.append(diferencia[el])
        
    vector_delta2.append(sqrt((vector[0]**2) + (vector[1]**2) + (vector[2]**2) ))


#Ahora obtendre el vector de la diferencia entre eulerint y odeint.

vector_diferencia = []
for a in range(len(t)):
    pos_actual = array([x[a], y[a], z[a], vx[a], vy[a], vz[a]])
    diferencia = sol_odeint[a]-sol_eulerint[a]   

#ahora obtengo solo los 3 primeros valores porque son los de posicion y el resto son de velocidad q no me importan
    vector=[] 
    for el in range(len(diferencia)-3):
        vector.append(diferencia[el])
        
    vector_diferencia.append(sqrt((vector[0]**2) + (vector[1]**2) + (vector[2]**2) ))






#Acá implementaré las correcciones de J2 y J3

J2 = 1.75553e10*km5  # Unidad [km5 / s2]
J3= -2.61913e11*km6 # Unidad [km6 / s2]

#Fx_j2 =
#Fy_j2 =
#Fz_j2 =
#
#Fx_j3 =
#Fy_j3 =
#Fz_j3 =

#copiare la funcion zpunto y la modificare para no cambiar la anterior

zp2 = zeros(6)
def zpunto_correccion(z,t):
    c = cos(om*t)
    s = sin(om*t)
    R = array([
      [c,s,0],
      [-s,c,0],
      [0,0,1]])
    
    Rp =om* (array([
      [-s,c,0],
      [-c,-s,0],
     [ 0,0,0]]))
    
    Rpp = (om**2)* (array([
        [-c,-s,0],
        [s,-c,0],
        [0,0,0]]))
    
    
    x = z[0:3] 
    xp = z[3:6] 
    
    r2 = dot(x,x)
    r = sqrt(r2)
    xs = R@x
    rnorm = xs/r
    Fg = -mu/r**2 * rnorm
    
    
    z2 = xs[2]**2
    rd = xs[0]**2 + xs[1]**2
    FJ2 = J2*xs / r**7
    FJ2[0] = FJ2[0] * (6*z2 - 1.5*rd)
    FJ2[1] = FJ2[1] * (6*z2 - 1.5*rd)
    FJ2[2] = FJ2[2] * (3*z2 - 4.5*rd)
    
    FJ3 = zeros(3)
    FJ3[0] = J3 * xs[0]*xs[2] / r**9 * (10*z2 - 7.5*rd)
    FJ3[1] = J3 * xs[1]*xs[2] / r**9 * (10*z2 - 7.5*rd)
    FJ3[2] = J3                       / r**9 * (4*z2 *(z2 - 3*rd) + 1.5*rd**2)
    
    Fg = (-G*mt/r**2)* (R@(x/r))
    
    zp2[0:3] = xp
    zp2[3:6] = R.T@(Fg +FJ2 + FJ3 - (2*(Rp@xp) + (Rpp@x)))
    return zp2

#Aca divido los vectores de diferencia para deajrlos en km
vector_delta = array(vector_delta)/1000
vector_delta2 = array(vector_delta2)/1000


#aca grafico la posicion real del satelite en funcion del tiempo en cada eje. 
figure()
title("Posicion")
subplot(3,1,1)
title("Posicion")
plt.ylabel("X (KM)")
plot(t/3600.,x/1000.)
plot(t/3600.,sol_odeint[:,0]/1000)
subplot(3,1,2)
plt.ylabel("Y (KM)")
plot(t/3600.,y/1000.)
plot(t/3600.,sol_odeint[:,1]/1000)
subplot(3,1,3)
plt.ylabel("Z (KM)")
plt.xlabel("Tiempo,t (horas)")
plot(t/3600.,z/1000.)
plot(t/3600.,sol_odeint[:,2]/1000)


#Aca grafico la diferencia entre la posicion real y predicha de odeint
figure()
title("Odeint")
plt.xlabel("Tiempo,t (horas)")
plt.ylabel("Deriva,δ (KM)")
plt.ylabel("Y (m)")
plot(t/3600.,vector_delta,)


#Aca grafico la diferencia entre la posicion real y predicha de eulerint
figure()
title("Eulerint")
plt.xlabel("Tiempo,t (horas)")
plt.ylabel("Deriva,δ (KM)")
plot(t/3600.,vector_delta2)



#Acá grafico la diferencia entre la posición real y la predicha con la corrección

sol_correccion = odeint(zpunto_correccion,z0,t)

vector_delta3 = []
for a in range(len(t)):
    pos_actual = array([x[a], y[a], z[a], vx[a], vy[a], vz[a]])
    diferencia = pos_actual-sol_correccion[a]

    vector=[] 
    for el in range(len(diferencia)-3):
        vector.append(diferencia[el])
        
    vector_delta3.append(sqrt((vector[0]**2) + (vector[1]**2) + (vector[2]**2) ))


vector_delta3 = array(vector_delta3)/1000
vector_diferencia = array(vector_diferencia)/1000

figure()
title("Correccion")
plt.xlabel("Tiempo,t (horas)")
plt.ylabel("Deriva,δ (KM)")
plot(t/3600.,vector_delta3)


figure()
title("Eulerint vs Odeint")
plt.xlabel("Tiempo,t (horas)")
plt.ylabel("Deriva,δ (KM)")
plot(t/3600.,vector_diferencia)



figure()
subplot(3,1,1)
title("Posicion con la Correccion")

plt.ylabel("X (KM)")
plot(t/3600.,x/1000.)
plot(t/3600.,sol_correccion[:,0]/1000)
subplot(3,1,2)
plt.ylabel("Y (KM)")
plot(t/3600.,y/1000.)
plot(t/3600.,sol_correccion[:,1]/1000)
subplot(3,1,3)
plt.ylabel("Z (KM)")
plt.xlabel("Tiempo,t (horas)")
plot(t/3600.,z/1000.)
plot(t/3600.,sol_correccion[:,2]/1000)

show()





#%USERPROFILE%\AppData\Local\Microsoft\WindowsApps









