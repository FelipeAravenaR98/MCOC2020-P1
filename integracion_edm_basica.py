import scipy as sp
from scipy.integrate import odeint
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


#parámetros

r = 6371000 #m
xi=700000 #m posicion inicial en el eje x
G=6.67*10**(-11) #(N*m**2)/(kg**2)
om=7.27*10**(-5) #rad/seg
mt=5.97*10**24 #kg
atm = 80000 #m


#funcion a integrar

def satelite(z,t):   #z = [x,y,vx,vy]
    
    θ = (om*t)
    c = ((G*mt)/(r**3))
    
    R   = sp.array([[    np.cos(θ)      ,   -np.sin(θ)         ],
                    [    np.sin(θ)      ,    np.cos(θ)         ]])
    
    
    Rp2  = sp.array([[    -np.sin(θ)      ,    -np.cos(θ)       ],
                         [     np.cos(θ)      ,    -np.sin(θ)       ]])
    
    Rpp = sp.array([      [    -np.cos(θ)      ,    np.sin(θ)         ] 
                    ,     [    -np.sin(θ)      ,   -np.cos(θ)         ]   ])
    
    z1 = sp.array([z[0],z[1]])
    z2 = sp.array([z[2],z[3]])
    
    t1 =-(c*z1) #termino 1
    t2= ((R.T)@((om**2)*Rpp)@(z1)) + ((R.T)@(om*2*Rp2)@(z2)) #termino 2
    
    z2p = t1-t2
    
    zp = sp.zeros(4)
    
    zp[0:2]=z[2:4]
    zp[2] = z2p[0] 
    zp[3] = z2p[1]
    
    return zp


t =  sp.linspace(0, 10800 , 10001) #10800 son 2 orbitas completas aprox.

V=[7493.01] # velocidad minima por tanteo
for a in V:
  
    vi=a  #m/s
        
    z0=sp.array([xi+r,0,0,vi]) # #z = [x,y,vx,vy]
        
    sol=odeint(satelite,z0,t)
        
    x = sol[:,0]
    y = sol[:,1]
    
    
        
    velocidad = plt.plot(x,y,label= f"V = {a} m/s")
    


atmosfera=plt.Circle((0,0),r+atm,color='r',label="atmósfera") #Grafica la atmosfera
plt.gcf().gca().add_artist(atmosfera)

Tierra=plt.Circle((0,0),r,color='g',label="Planeta Gol") #Grafica la tierra 
plt.gcf().gca().add_artist(Tierra)
    

plt.plot([0,0],[0,-r - atm],"k")
radios=plt.plot([0,-r-atm],[0,0],"k",label="radio de la tierra y atmosfera")
plt.grid(True)



plt.legend()
plt.legend(loc="upper left", bbox_to_anchor=(0.5, 1.15), ncol=2)


# where some data has already been plotted to ax
handles, labels = ax.get_legend_handles_labels()

# manually define a new patch 
patch1 = mpatches.Patch(color='green', label='Planeta Gol')
patch2 = mpatches.Patch(color='red', label='atmosfera')

# handles is a list, so append manual patch
handles.append(patch1) 
handles.append(patch2)
# plot the legend
plt.legend(handles=handles, loc="best", bbox_to_anchor=(1, 1.15), ncol=3)




plt.grid(True)
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title('Trayectoria Satelite')
plt.show





